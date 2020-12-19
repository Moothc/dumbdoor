import socket
import logging

PORT = 4444
HOST = "localhost"
BUFFSIZE = 1024

class Dumb:
    def __init__(self, path_plugin="plugins/plugin.py"):
        self.client_sock = None
        self.path_plugin = path_plugin

    def off(self):
        if self.client_sock:
            logging.warning("Killing Dumb.")
            self.client_sock.close()
            self.client_sock = None

    def on(self):
        self._connect()
        logging.info(self.client_sock.recv(BUFFSIZE))
        self.client_sock.send("start_upload".encode())
        self.upload_plugin()

    def _connect(self):
        self.client_sock = socket.socket()
        self.client_sock.connect((HOST, PORT))

    def upload_plugin(self):
        try:
            with open(self.path_plugin, "rb") as plugin:
                data = plugin.read(BUFFSIZE)
                while data:
                    logging.info("Sending..")
                    self.client_sock.send(data)
                    data = plugin.read(BUFFSIZE)
            logging.info("Completed plugin upload.")
        finally:
            self.client_sock.shutdown(2)
            self.off()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    Dumb(path_plugin="plugins/get_door_info.py").on()
