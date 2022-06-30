import ssl
from pprint import pprint
from typing import Dict, Union, Any, List

import toml
import socket

import schlagdenabi_Runde

stand: dict[Union[list[Any], Any], Union[int, Any]] = {}

admin = 'yarissi'


def send(irc: ssl.SSLSocket, message: str):
    irc.send(bytes(f'{message}\r\n', 'UTF-8'))


def send_chat(irc: ssl.SSLSocket, message: str, channel: str):
    send(irc, f'PRIVMSG #{channel} :{message}')


def send_pong(irc: ssl.SSLSocket):
    send(irc, 'PONG :tmi.twitch.tv')


def getName(raw_message: str):
    components = raw_message.split()
    user, host = components[0].split('!')[1].split('@')
    return user


def getMessage(raw_message: str):
    components = raw_message.split()
    message = ' '.join(components[3:])[1:]
    return message


def parseNumber(msg):
    try:
        data = msg.split()[0].split("g")[0]
        return int(data)
    except:
        return None


def handle_chat(raw_message: str):
    components = raw_message.split()

    user, host = components[0].split('!')[1].split('@')
    channel = components[2]
    message = ' '.join(components[3:])[1:]

    if user == admin and message == "start":
        return 'start'
    if message == "!stand":
        return "!stand"
    if user == admin and message == "!reset":
        return "!reset"
    if user == admin and message == "!endstand":
        return "!endstand"
    return False


def schlagdenabi(irc):
    users, numbers = schlagdenabi_Runde.collectData(irc)
    solution = schlagdenabi_Runde.collectSolution(irc)
    winnerList, equal = schlagdenabi_Runde.determineWinner(users, numbers, solution)
    gewinner = ' '.join(winnerList)
    if len(winnerList) == 1:
        msg = "/me Der Gewinner ist: " + gewinner
        send_chat(irc, msg, channel_name)
    if len(winnerList) > 1:
        msg = "/me Die Gewinner sind: " + gewinner
        send_chat(irc, msg, channel_name)
    return winnerList, equal


def CalculateStand(irc, channel_name):
    if len(stand) == 0:
        send_chat(irc, 'Es gibt noch keinen Spielstand', channel_name)
    else:
        spielstand: str = ""
        for key in stand:
            punktePerson = str(key) + " = " + str(stand.get(key)) + ", "
            spielstand = spielstand + punktePerson
        send_chat(irc, spielstand, channel_name)


def getstand():
    return stand


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

    send_chat(irc, 'Bot is running', channel_name)

    while True:
        data = irc.recv(1024)
        raw_message = data.decode('UTF-8')

        for line in raw_message.splitlines():
            if line.startswith('PING :tmi.twitch.tv'):
                send_pong(irc)
            else:
                components = line.split()
                text = components[1]

                if text == 'PRIVMSG':
                    command = handle_chat(line)
                    pprint(command)
                    if command == 'start':
                        send_chat(irc, 'derabiRraga', channel_name)
                        user, equal = schlagdenabi(irc)
                        for winner in user:
                            if winner not in stand:
                                if equal:
                                    stand[winner] = 2
                                else:
                                    stand[winner] = 1
                            else:
                                if equal:
                                    stand[winner] = stand.get(winner) + 2
                                else:
                                    stand[winner] = stand.get(winner) + 1
                    if command == '!stand':
                        CalculateStand(irc, channel_name)
                    if command == '!reset':
                        send_chat(irc, 'Reset erfolgreich', channel_name)
                        stand.clear()
