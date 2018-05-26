#!/usr/bin/env python3

import os

import asyncio
from dialogue_manager import DialogueManager


ips_file = os.path.join('.', 'white_list.txt')
checkIpFlag = False


def is_unicode(text):
    return len(text) == len(text.encode())


class SimpleDialogueManager(object):
    def generate_answer(self, question):
        return "Hello, pal"


dialogue_manager = DialogueManager()


class ClientServerProtocol(asyncio.Protocol):
    def __init__(self):
        super().__init__()
        self.ips = self.readIps()

    def readIps(self):
        with open(ips_file, 'r') as f:
            result = f.readlines()

        result = [l.strip() for l in result if len(l.strip()) != 0]

        return result

    def connection_made(self, transport):
        self.transport = transport

        self.peername = transport.get_extra_info('peername')
        self.sockname = transport.get_extra_info('sockname')

        self.ip_address = self.peername[0]

        if checkIpFlag and self.ip_address not in self.ips:
            print('IP address {0} not in white list'.format(self.ip_address))

            self.transport.write(("Sorry, your IP address not in white list :)\n").encode())
            self.transport.close()

            return

    def data_received(self, data):
        try:
            decoded_data = data.decode().strip(' ')
        except UnicodeDecodeError:
            return

        # Wait till command ends with '\n'
        if not decoded_data.endswith('\n'):
            return

        print('> ' + decoded_data, end='')

        try:
            # Process incoming message
            resp = self.process_data(decoded_data)
        except Exception as err:
            self.transport.write(("Error\n" + str(err) + "\n\n").encode())
            return

        # Send response
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
        ClientServerProtocol, host, port
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
