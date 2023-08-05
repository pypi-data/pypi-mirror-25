# Copyright 2015 Cloudbase Solutions Srl
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import errno
import os

from eventlet import patcher
from nova.i18n import _, _LE  # noqa
from oslo_log import log as logging

from hyperv.nova import constants
from hyperv.nova import ioutils
from hyperv.nova import vmutils

threading = patcher.original('threading')
time = patcher.original('time')

LOG = logging.getLogger(__name__)


class NamedPipeHandler(object):
    """Handles asyncronous I/O operations on a specified named pipe."""

    _MAX_LOG_ROTATE_RETRIES = 5

    def __init__(self, pipe_name, input_queue=None, output_queue=None,
                 connect_event=None, log_file=None):
        self._pipe_name = pipe_name
        self._input_queue = input_queue
        self._output_queue = output_queue
        self._log_file_path = log_file

        self._connect_event = connect_event
        self._stopped = threading.Event()
        self._workers = []
        self._pipe_handle = None

        self._ioutils = ioutils.IOUtils()

        self._setup_io_structures()

    def start(self):
        try:
            self._open_pipe()

            if self._log_file_path:
                self._log_file_handle = open(self._log_file_path, 'ab', 1)

            jobs = [self._read_from_pipe]
            if (self._input_queue and self._connect_event):
                jobs.append(self._write_to_pipe)

            for job in jobs:
                worker = threading.Thread(target=job)
                worker.setDaemon(True)
                worker.start()
                self._workers.append(worker)
        except Exception as err:
            msg = (_("Named pipe handler failed to initialize. "
                     "Pipe Name: %(pipe_name)s "
                     "Error: %(err)s") %
                   {'pipe_name': self._pipe_name,
                    'err': err})
            LOG.error(msg)
            self.stop()
            raise vmutils.HyperVException(msg)

    def stop(self):
        self._stopped.set()
        self._cancel_io()

        for worker in self._workers:
            worker_running = (worker.is_alive() and
                              worker is not threading.current_thread())
            if worker_running:
                worker.join()

        self._close_pipe()
        if self._log_file_handle:
            self._log_file_handle.close()

    def _setup_io_structures(self):
        self._r_buffer = self._ioutils.get_buffer(
            constants.SERIAL_CONSOLE_BUFFER_SIZE)
        self._w_buffer = self._ioutils.get_buffer(
            constants.SERIAL_CONSOLE_BUFFER_SIZE)

        self._r_overlapped = self._ioutils.get_new_overlapped_structure()
        self._w_overlapped = self._ioutils.get_new_overlapped_structure()

        self._r_completion_routine = self._ioutils.get_completion_routine(
            self._read_callback)
        self._w_completion_routine = self._ioutils.get_completion_routine()

        self._log_file_handle = None

    def _open_pipe(self):
        """Opens a named pipe in overlapped mode for asyncronous I/O."""
        self._ioutils.wait_named_pipe(self._pipe_name)

        self._pipe_handle = self._ioutils.open(
            self._pipe_name,
            desired_access=(ioutils.GENERIC_READ | ioutils.GENERIC_WRITE),
            share_mode=(ioutils.FILE_SHARE_READ | ioutils.FILE_SHARE_WRITE),
            creation_disposition=ioutils.OPEN_EXISTING,
            flags_and_attributes=ioutils.FILE_FLAG_OVERLAPPED)

    def _close_pipe(self):
        if self._pipe_handle:
            self._ioutils.close_handle(self._pipe_handle)
            self._pipe_handle = None

    def _cancel_io(self):
        if self._pipe_handle:
            self._ioutils.set_event(self._r_overlapped.hEvent)
            self._ioutils.set_event(self._w_overlapped.hEvent)
            self._ioutils.cancel_io(self._pipe_handle)

    def _read_from_pipe(self):
        self._start_io_worker(self._ioutils.read,
                              self._r_buffer,
                              self._r_overlapped,
                              self._r_completion_routine)

    def _write_to_pipe(self):
        self._start_io_worker(self._ioutils.write,
                              self._w_buffer,
                              self._w_overlapped,
                              self._w_completion_routine,
                              self._get_data_to_write)

    def _start_io_worker(self, func, buff, overlapped_structure,
                         completion_routine, buff_update_func=None):
        try:
            while not self._stopped.isSet():
                if buff_update_func:
                    num_bytes = buff_update_func()
                    if not num_bytes:
                        continue
                else:
                    num_bytes = len(buff)

                func(self._pipe_handle, buff, num_bytes,
                     overlapped_structure, completion_routine)
        except Exception:
            self._stopped.set()

    def _read_callback(self, num_bytes):
        data = self._ioutils.get_buffer_data(self._r_buffer,
                                             num_bytes)
        if self._output_queue:
            self._output_queue.put(data)

        if self._log_file_handle:
            self._write_to_log(data)

    def _get_data_to_write(self):
        while not (self._stopped.isSet() or self._connect_event.isSet()):
            time.sleep(1)

        data = self._input_queue.get()
        if data:
            self._ioutils.write_buffer_data(self._w_buffer, data)
            return len(data)
        return 0

    def _write_to_log(self, data):
        if self._stopped.isSet():
            return

        try:
            log_size = self._log_file_handle.tell() + len(data)
            if (log_size >= constants.MAX_CONSOLE_LOG_FILE_SIZE):
                self._rotate_logs()
            self._log_file_handle.write(data)
        except Exception:
            self._stopped.set()

    def _rotate_logs(self):
        self._log_file_handle.flush()
        self._log_file_handle.close()

        log_archive_path = self._log_file_path + '.1'

        if os.path.exists(log_archive_path):
            self._retry_if_file_in_use(os.remove,
                                       log_archive_path)

        self._retry_if_file_in_use(os.rename,
                                   self._log_file_path,
                                   log_archive_path)

        self._log_file_handle = open(
            self._log_file_path, 'ab', 1)

    def _retry_if_file_in_use(self, f, *args, **kwargs):
        # The log files might be in use if the console log is requested
        # while a log rotation is attempted.
        retry_count = 0
        while True:
            try:
                return f(*args, **kwargs)
            except WindowsError as err:
                if (err.errno == errno.EACCES and
                        retry_count < self._MAX_LOG_ROTATE_RETRIES):
                    retry_count += 1
                    time.sleep(1)
                else:
                    raise
