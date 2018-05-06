import socket


class ClientError(Exception):
    """Общий класс исключений клиента"""
    pass


class ClientSocketError(ClientError):
    """Исключение, выбрасываемое клиентом при сетевой ошибке"""
    pass


class Client:
    def __init__(self, host, port, timeout=None):
        # Класс инкапсулирует создание сокета
        self.host = host
        self.port = port
        try:
            self.connection = socket.create_connection((host, port), timeout)
        except socket.error as err:
            raise ClientSocketError("Error while creating connection", err)

    def _read(self):
        """Метод для чтения ответа сервера"""
        data = b""
        # Накапливаем буфер, пока не встретим "\n" в конце команды
        while not data.endswith(b"\n"):
            try:
                data += self.connection.recv(1024)
            except socket.error as err:
                raise ClientSocketError("Error recv data", err)

        decoded_data = data.decode()

        return decoded_data

    def post(self, message):
        # Отправляем запрос
        try:
            self.connection.sendall(
                message.encode()
            )
        except socket.error as err:
            raise ClientSocketError("error send data", err)

        # Разбираем ответ
        return self._read()

    def close(self):
        try:
            self.connection.close()
        except socket.error as err:
            raise ClientSocketError("Error close connection", err)


if __name__ == "__main__":
    client = Client("ec2-54-89-217-31.compute-1.amazonaws.com", 8080, timeout=10)

    message = ''

    print('Talk!\n')
    while message.strip(' ').lower() != 'ciao!':
        message = input('> ')
        print('> ' + client.post(message + '\n'))

    client.close()
