import socket
import json
import os

class ClientError(Exception):
    """General Client exception"""
    pass


class ClientSocketError(ClientError):
    pass


class Client:
    def __init__(self, host, port, timeout=None):
        # Socket encapsulation
        self.host = host
        self.port = port

        try:
            self.connection = socket.create_connection((host, port), timeout)
        except socket.error as err:
            raise ClientSocketError("Error while creating connection", err)

    def _read(self):
        """Reads Server's answer"""

        data = b""

        # Fill buffer while '\n' not encountered
        while not data.endswith(b"\n"):
            try:
                data += self.connection.recv(1024)
            except socket.error as err:
                raise ClientSocketError("Error recv data", err)

        decoded_data = data.decode()

        return decoded_data

    def post(self, message):
        # Send message
        try:
            self.connection.sendall(message.encode())
        except socket.error as err:
            raise ClientSocketError("Error send data", err)

        # Read answer
        return self._read()

    def close(self):
        try:
            self.connection.close()
        except socket.error as err:
            raise ClientSocketError("Error close connection", err)


if __name__ == "__main__":
    config_file_path = os.path.join('.', 'bin', 'config.data')

    with open(config_file_path, 'r') as f:
        config = json.loads(f.read())

    host = 'localhost' # config["host"]
    port = int(config["port"])

    client = Client(host, port, timeout=10)

    message = ''

    print('Talk!\n')
    while message.strip(' ').lower() != 'ciao!':
        message = input('> ')
        print('> ' + client.post(message + '\n'))

    client.close()
