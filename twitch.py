import ssl
from typing import Union, Any

import requests as requests
import toml
import socket

from TwitchCommands import schlagdenabi_Runde, small_commands
from TwitchCommands.side_commands_schlagdenabi import CalculateStand, resetStand, give_Points, write_stand, \
    give_Winner_Points

import json


admin = 'xxxxxxx'


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
    error = '\U000e0000'
    if error in message:
        return message.split(" ")[0]
    return message


def parseNumber(msg):
    try:
        data = msg.split()[0].split("g")[0]
        return int(data)
    except:
        return None



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


def checkCommands(irc, channel_name, raw_message):
    components = raw_message.split()

    user, host = components[0].split('!')[1].split('@')
    message = ' '.join(components[3:])[1:]

    if user == admin and (message == "start" or message == "Start" or message == "START"):
        return 'start'
    if message.split(" ")[0] == "!stand":
        CalculateStand(irc, channel_name, getMessage(raw_message))
    if message.split(" ")[0] == "!fight":
        small_commands.fight(irc,channel_name, raw_message)
    if message.split(" ")[0] == "!blöff":
        small_commands.blöff(irc, channel_name, raw_message)
    if message == "!help":
        send_chat(irc, "Hier kommt ihr zum Code und den Commands vom Abi Bot: https://github.com/YaRissi/DerAbiBot", channel_name)
    if user == admin and message == "!reset":
        resetStand(irc, channel_name)
    if user == admin and message == "!endstand":
        return "!endstand"
    if user == admin and message.split(" ")[0] == "!give":
        give_Points(irc, channel_name, getMessage(raw_message))
    return False


def getUserList(channel_name):
    response = requests.get(f"https://tmi.twitch.tv/group/user/{channel_name}/chatters")

    chatter = json.loads(response.text)['chatters']
    listChatter = []

    for type in chatter:
        for chatty in chatter[type]:
            listChatter.append(chatty)

    return listChatter


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

    stand: dict[Union[list[Any], Any], Union[int, Any]] = {"yarissi": 1, "freeyarissi": 3}

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
                    command = checkCommands(irc, channel_name, line)
                    if command == 'start':
                        send_chat(irc, 'derabiRraga', channel_name)
                        user, equal = schlagdenabi(irc)
                        if user is not None:
                            give_Winner_Points(user, equal)
                        else:
                            send_chat(irc, "Ach be keiner hat mitgemacht", channel_name)