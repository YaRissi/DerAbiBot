import ssl
from typing import Union, Any

import toml
import socket

import json

from TwitchCommands import schlagdenabi_Runde

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

    if user == admin and (message == "start" or message == "Start" or message == "START"):
        return 'start'
    if message.split(" ")[0] == "!stand":
        return "!stand"
    if user == admin and message == "!reset":
        return "!reset"
    if user == admin and message == "!endstand":
        return "!endstand"
    return False


def schlagdenabi(irc):
    users, numbers = schlagdenabi_Runde.collectData(irc)
    if len(users) == 0:
        return None, None
    solution = schlagdenabi_Runde.collectSolution(irc)
    winnerList, equal = schlagdenabi_Runde.determineWinner(users, numbers, solution)
    gewinner = ' '.join(winnerList)
    if len(winnerList) == 1:
        if equal:
            msg = "/me Der Gewinner mit Punktlandung ist: " + gewinner
        else:
            msg = "/me Der Gewinner ist: " + gewinner
        send_chat(irc, msg, channel_name)
    if len(winnerList) > 1:
        if equal:
            msg = "/me Die Gewinner mit Punktlandung sind: " + gewinner
        else:
            msg = "/me Die Gewinner sind: " + gewinner
        send_chat(irc, msg, channel_name)
    return winnerList, equal


def CalculateStand(irc, channel_name, line):
    stand = load_Stand()
    if len(stand) == 0:
        send_chat(irc, 'Es gibt noch keinen Spielstand', channel_name)
    elif len(line.split(" ")) == 2:
        key = str(line.split(" ")[1]).lower()
        if key in stand.keys():
            punkteUser = str(key).lower() + " = " + str(stand[key])
            send_chat(irc, punkteUser, channel_name)
        else:
            CalculateStand(irc, channel_name, line.split(" ")[0])
    else:
        spielstand = ""
        for key in sorted(stand.items(), key=lambda item: item[1], reverse=True):
            name = str(key).split("'")[1]
            punkte = str(key).split(", ")[1].split(")")[0]
            punktePerson = name + " = " + punkte + " "
            spielstand = spielstand + punktePerson
        send_chat(irc, spielstand, channel_name)
    write_stand(stand)


def load_Stand():
    with open('ressources/stand.json', 'r') as fp:
        return json.load(fp)


def write_stand(stand):
    with open("ressources/stand.json", "w") as fp:
        json.dump(stand, fp)


def give_Winner_Points(user, equal):
    stand = load_Stand()
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
    write_stand(stand)


def getstand():
    return stand


if __name__ == '__main__':
    config = toml.load("ressources/config.toml")

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

    stand: dict[Union[list[Any], Any], Union[int, Any]] = {}

    write_stand(stand)

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
                    if command == 'start':
                        send_chat(irc, 'derabiRraga', channel_name)
                        user, equal = schlagdenabi(irc)
                        if user is not None:
                            give_Winner_Points(user, equal)
                        else:
                            send_chat(irc, "Ach be keiner hat mitgemacht", channel_name)
                    if command == '!stand':
                        CalculateStand(irc, channel_name, getMessage(line))
                    if command == '!reset':
                        stand.clear()
                        write_stand(stand)
                        send_chat(irc, 'Reset erfolgreich', channel_name)
