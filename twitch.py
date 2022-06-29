import ssl
from pprint import pprint

import toml
import socket


def send(irc: ssl.SSLSocket, message: str):
    irc.send(bytes(f'{message}\r\n', 'UTF-8'))


def send_chat(irc: ssl.SSLSocket, message: str, channel: str):
    send(irc, f'PRIVMSG #{channel} :{message}')


def send_pong(irc: ssl.SSLSocket):
    send(irc, 'PONG :tmi.twitch.tv')


def getName(irc: ssl.SSLSocket, raw_message: str):
    components = raw_message.split()
    user, host = components[0].split('!')[1].split('@')
    return user


def getMessage(irc: ssl.SSLSocket, raw_message: str):
    components = raw_message.split()
    message = ' '.join(components[3:])[1:]
    return message


def parseNumber(msg):
    try:
        data = msg.split()[0].split("g")[0]
        return int(data)
    except:
        return None


def handle_chat(irc: ssl.SSLSocket, raw_message: str):
    components = raw_message.split()

    user, host = components[0].split('!')[1].split('@')
    channel = components[2]
    message = ' '.join(components[3:])[1:]

    if user == 'yarissi' and message == "start":
        return True
    return False


def collectData(irc: ssl.SSLSocket):
    users = []
    numbers = []
    while True:
        data = irc.recv(1024)
        raw_message = data.decode('UTF-8')

        for line in raw_message.splitlines():
            if line.startswith('PING :tmi.twitch.tv'):
                send_pong(irc)
            else:
                components = line.split()
                command = components[1]

                if command == 'PRIVMSG':
                    message = getMessage(irc, line)
                    name = getName(irc, line)
                    if name == 'yarissi' and message == 'ende':
                        return users, numbers
                    number = parseNumber(message)
                    if name not in users and number is not None:
                        users.append(name)
                        numbers.append(number)
                    pprint(users)
                    pprint(numbers)


def collectSolution(irc: ssl.SSLSocket):
    while True:
        data = irc.recv(1024)
        raw_message = data.decode('UTF-8')

        for line in raw_message.splitlines():
            if line.startswith('PING :tmi.twitch.tv'):
                send_pong(irc)
            else:
                components = line.split()
                command = components[1]

                if command == 'PRIVMSG':
                    name = getName(irc, line)
                    number = parseNumber(getMessage(irc, line))
                    if name == 'yarissi' and number is not None:
                        pprint(number)
                        return number


if __name__ == '__main__':
    config = toml.load('config.toml')

    bot_username = config['bot_username']
    channel_name = config['channel_name']
    oauth_token = config['oauth_token']

    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    irc = context.wrap_socket(socket)

    irc.connect(('irc.chat.twitch.tv', 6697))

    send(irc, f'PASS oauth:{oauth_token}')
    send(irc, f'NICK {bot_username}')
    send(irc, f'JOIN #{channel_name}')

    send_chat(irc, 'Das ist ein Test', channel_name)


    while True:
        data = irc.recv(1024)
        raw_message = data.decode('UTF-8')

        for line in raw_message.splitlines():
            if line.startswith('PING :tmi.twitch.tv'):
                send_pong(irc)
            else:
                components = line.split()
                command = components[1]

                if command == 'PRIVMSG':
                    start = handle_chat(irc, line)

                    if start:
                        users, numbers = collectData(irc)
                        solution = collectSolution(irc)


