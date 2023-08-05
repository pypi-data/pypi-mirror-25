import socket


class ReceiveControlComm(object):

        def __init__(self, ip_address='127.0.0.1', port=6555):
                self.ip_address = ip_address
                self.port = port
                self.name = ""
                self.acquisition_control = None

                self._buffer_size = 1024

        def __repr__(self):
            return '<%s %s %s:%s (%s)>' % (
                self.__class__.__name__,
                self.name,
                self.ip_address,
                self.port,
                self.acquisition_control)

        def stop_running(self):
                self.threads_active = False
                temp_s = socket.socket(
                        socket.AF_INET, socket.SOCK_STREAM)
                temp_s.connect(('127.0.0.1', self.port))
                self.s.close()
                temp_s.close()

        def start_socket(self):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.bind((self.ip_address, self.port))
                s.listen(1)
                self.s = s

        def start_comm_listening(self):
                self.start_socket()
                self._comm_listen_thread = Thread(
                                target=self._comm_listening)
                self._comm_listen_thread.start()

        def _parse_comm_string(self, comm_string, conn):
                acquisition_control = self.acquisition_control
                if comm_string[0] == "ACC":

                    if comm_string[1] == "PROC":
                        if comm_string[2] in acquisition_control.process_dict.keys():
                            proc = acquisition_control.process_dict['proc']
                            if comm_string[3] == "BRIGHTNESS":
                                proc.base_level_correction = comm_string[4]
                            if comm_string[3] == "CONTRAST":
                                proc.fraction_correction = 1.
                        else:
                            pass

                    elif comm_string[1] == "START_PROCESS":
                        if comm_string[2] == "BRIGHTFIELD":
                            name = acquisition_process.start_bf_process()
                            port = acquisition_control.process_dict[name]['comm'].port
                            conn.sendall(str(port) + "\n")
                        elif comm_string[2] == "COMXTHRESHOLD":
                            name = acquisition_process.start_com_x_threshold_process()
                            port = acquisition_control.process_dict[name]['comm'].port
                            conn.sendall(str(port) + "\n")
                        elif comm_string[2] == "COMYTHRESHOLD":
                            name = acquisition_process.start_com_y_threshold_process()
                            port = acquisition_control.process_dict[name]['comm'].port
                            conn.sendall(str(port) + "\n")

                    elif comm_string[1] == "CLEAR_QUEUES":
                        acquisition_control.clear_all_queues()
                    elif comm_string[1] == "CANCEL_ALL":
                        acquisition_control.cancel_all_processes()

        def _comm_listening(self):
                conn, addr = self.s.accept()
                while self.threads_active:
                    received_comm = conn.recv(self._buffer_size).split(",")
                    self._parse_comm_string(received_comm, conn)
                    conn.close()
                    conn, addr = self.s.accept()
