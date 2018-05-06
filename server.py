#!/usr/bin/env python3

import asyncio
from dialogue_manager import DialogueManager


def is_unicode(text):
    return len(text) == len(text.encode())


class SimpleDialogueManager(object):
    def generate_answer(self, question):
        return "Hello, pal"


dialogue_manager = DialogueManager()

class ClientServerProtocol(asyncio.Protocol):
    def __init__(self):
        super().__init__()

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        try:
            decoded_data = data.decode().strip(' ')
        except UnicodeDecodeError:
            return

        # Ждём данных, если команда не завершена символом \n
        if not decoded_data.endswith('\n'):
            return

        print('> ' + decoded_data, end='')

        try:
            # Обработка поступившего сообщения
            resp = self.process_data(decoded_data)
        except Exception as err:
            self.transport.write(("Error\n" + str(err) + "\n\n").encode())
            return

        # Отправка ответа
        self.transport.write(resp.encode())

    def process_data(self, data):
        if data == 'help\n' or data == '?\n':
            answer = "We can talk about it"
        else:
            answer = dialogue_manager.generate_answer(data)

        answer += '\n'
        print('> ' + answer)

        return answer


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )

    server = loop.run_until_complete(coro)

    print("Server created!\n")

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == '__main__':
    run_server('', 8080)
