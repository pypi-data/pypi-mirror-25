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
import mock
from six.moves import builtins

from hyperv.nova import constants
from hyperv.nova import namedpipe
from hyperv.nova import vmutils
from hyperv.tests.unit import test_base


class NamedPipeTestCase(test_base.HyperVBaseTestCase):
    _FAKE_LOG_PATH = 'fake_log_path'

    @mock.patch.object(namedpipe.NamedPipeHandler, '_setup_io_structures')
    def setUp(self, mock_setup_structures):
        super(NamedPipeTestCase, self).setUp()

        self._mock_input_queue = mock.Mock()
        self._mock_output_queue = mock.Mock()
        self._mock_client_connected = mock.Mock()

        threading_patcher = mock.patch.object(namedpipe, 'threading')
        threading_patcher.start()
        self.addCleanup(threading_patcher.stop)

        self._handler = namedpipe.NamedPipeHandler(
            mock.sentinel.pipe_name,
            self._mock_input_queue,
            self._mock_output_queue,
            self._mock_client_connected,
            self._FAKE_LOG_PATH)
        self._handler._ioutils = mock.Mock()

    def _mock_setup_pipe_handler(self):
        self._handler._log_file_handle = mock.Mock()
        self._handler._pipe_handle = mock.sentinel.pipe_handle
        self._handler._workers = [mock.Mock(), mock.Mock()]
        self._handler._r_buffer = mock.Mock()
        self._handler._w_buffer = mock.Mock()
        self._handler._r_overlapped = mock.Mock()
        self._handler._w_overlapped = mock.Mock()
        self._handler._r_completion_routine = mock.Mock()
        self._handler._w_completion_routine = mock.Mock()

    @mock.patch.object(builtins, 'open')
    @mock.patch.object(namedpipe.NamedPipeHandler, '_open_pipe')
    def test_start_pipe_handler(self, mock_open_pipe, mock_open):
        self._handler.start()

        mock_open_pipe.assert_called_once_with()
        mock_open.assert_called_once_with(self._FAKE_LOG_PATH, 'ab', 1)
        self.assertEqual(mock_open.return_value,
                         self._handler._log_file_handle)

        thread = namedpipe.threading.Thread
        thread.assert_has_calls(
            [mock.call(target=self._handler._read_from_pipe),
             mock.call().setDaemon(True),
             mock.call().start(),
             mock.call(target=self._handler._write_to_pipe),
             mock.call().setDaemon(True),
             mock.call().start()])

    @mock.patch.object(namedpipe.NamedPipeHandler, 'stop')
    @mock.patch.object(namedpipe.NamedPipeHandler, '_open_pipe')
    def test_start_pipe_handler_exception(self, mock_open_pipe,
                                          mock_stop_handler):
        mock_open_pipe.side_effect = Exception

        self.assertRaises(vmutils.HyperVException,
                          self._handler.start)

        mock_stop_handler.assert_called_once_with()

    @mock.patch.object(namedpipe.NamedPipeHandler, '_close_pipe')
    def test_stop_pipe_handler(self, mock_close_pipe):
        self._mock_setup_pipe_handler()

        self._handler.stop()

        self._handler._stopped.set.assert_called_once_with()
        mock_close_pipe.assert_called_once_with()
        self._handler._log_file_handle.close.assert_called_once_with()

        self._handler._ioutils.set_event.assert_has_calls(
            [mock.call(self._handler._r_overlapped.hEvent),
             mock.call(self._handler._w_overlapped.hEvent)])
        self._handler._ioutils.cancel_io.assert_called_once_with(
            mock.sentinel.pipe_handle)

        for worker in self._handler._workers:
            worker.join.assert_called_once_with()

    def _test_start_io_worker(self, buff_update_func=None, exception=None):
        self._handler._stopped.isSet.side_effect = [False, True]
        self._handler._pipe_handle = mock.sentinel.pipe_handle
        self._handler.stop = mock.Mock()

        io_func = mock.Mock(side_effect=exception)
        fake_buffer = 'fake_buffer'

        self._handler._start_io_worker(io_func, fake_buffer,
                                       mock.sentinel.overlapped_structure,
                                       mock.sentinel.completion_routine,
                                       buff_update_func)

        if buff_update_func:
            num_bytes = buff_update_func()
        else:
            num_bytes = len(fake_buffer)

        io_func.assert_called_once_with(mock.sentinel.pipe_handle,
                                        fake_buffer, num_bytes,
                                        mock.sentinel.overlapped_structure,
                                        mock.sentinel.completion_routine)
        if exception:
            self._handler._stopped.set.assert_called_once_with()

    def test_start_io_worker(self):
        self._test_start_io_worker()

    def test_start_io_worker_with_buffer_update_method(self):
        self._test_start_io_worker(buff_update_func=mock.Mock())

    def test_start_io_worker_exception(self):
        self._test_start_io_worker(exception=IOError)

    @mock.patch.object(namedpipe.NamedPipeHandler, '_write_to_log')
    def test_read_callback(self, mock_write_to_log):
        self._mock_setup_pipe_handler()
        fake_data = self._handler._ioutils.get_buffer_data.return_value

        self._handler._read_callback(mock.sentinel.num_bytes)

        self._handler._ioutils.get_buffer_data.assert_called_once_with(
            self._handler._r_buffer, mock.sentinel.num_bytes)
        self._mock_output_queue.put.assert_called_once_with(fake_data)
        mock_write_to_log.assert_called_once_with(fake_data)

    @mock.patch.object(namedpipe, 'time')
    def test_get_data_to_write(self, mock_time):
        self._mock_setup_pipe_handler()
        self._handler._stopped.isSet.side_effect = [False, False]
        self._mock_client_connected.isSet.side_effect = [False, True]
        fake_data = 'fake input data'
        self._mock_input_queue.get.return_value = fake_data

        num_bytes = self._handler._get_data_to_write()

        mock_time.sleep.assert_called_once_with(1)
        self._handler._ioutils.write_buffer_data.assert_called_once_with(
            self._handler._w_buffer, fake_data)
        self.assertEqual(len(fake_data), num_bytes)

    @mock.patch.object(namedpipe.NamedPipeHandler, '_rotate_logs')
    def _test_write_to_log(self, mock_rotate_logs, size_exceeded=False):
        self._mock_setup_pipe_handler()
        self._handler._stopped.isSet.return_value = False
        fake_handle = self._handler._log_file_handle
        fake_handle.tell.return_value = (constants.MAX_CONSOLE_LOG_FILE_SIZE
                                         if size_exceeded else 0)
        fake_data = 'fake_data'

        self._handler._write_to_log(fake_data)

        if size_exceeded:
            mock_rotate_logs.assert_called_once_with()

        self._handler._log_file_handle.write.assert_called_once_with(
            fake_data)

    def test_write_to_log(self):
        self._test_write_to_log()

    def test_write_to_log_size_exceeded(self):
        self._test_write_to_log(size_exceeded=True)

    @mock.patch.object(namedpipe.NamedPipeHandler, '_retry_if_file_in_use')
    @mock.patch.object(builtins, 'open')
    @mock.patch.object(namedpipe, 'os')
    def test_rotate_logs(self, mock_os, mock_open, mock_exec_retry):
        fake_archived_log_path = self._FAKE_LOG_PATH + '.1'
        mock_os.path.exists.return_value = True

        self._mock_setup_pipe_handler()
        fake_handle = self._handler._log_file_handle

        self._handler._rotate_logs()

        fake_handle.flush.assert_called_once_with()
        fake_handle.close.assert_called_once_with()
        mock_os.path.exists.assert_called_once_with(
            fake_archived_log_path)

        mock_exec_retry.assert_has_calls([mock.call(mock_os.remove,
                                                    fake_archived_log_path),
                                          mock.call(mock_os.rename,
                                                    self._FAKE_LOG_PATH,
                                                    fake_archived_log_path)])

        mock_open.assert_called_once_with(self._FAKE_LOG_PATH, 'ab', 1)
        self.assertEqual(mock_open.return_value,
                         self._handler._log_file_handle)

    @mock.patch.object(namedpipe, 'time')
    def test_retry_if_file_in_use_exceeded_retries(self, mock_time):
        class FakeWindowsException(Exception):
            errno = errno.EACCES

        raise_count = self._handler._MAX_LOG_ROTATE_RETRIES + 1
        mock_func_side_eff = [FakeWindowsException] * raise_count
        mock_func = mock.Mock(side_effect=mock_func_side_eff)

        with mock.patch.object(namedpipe, 'WindowsError',
                               FakeWindowsException, create=True):
            self.assertRaises(FakeWindowsException,
                              self._handler._retry_if_file_in_use,
                              mock_func, mock.sentinel.arg)
            mock_time.sleep.assert_has_calls(
                [mock.call(1)] * self._handler._MAX_LOG_ROTATE_RETRIES)
