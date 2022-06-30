import ssl
from pprint import pprint

import toml
import socket

import twitch

config = toml.load('config.toml')

bot_username = config['bot_username']
channel_name = config['channel_name']


def collectSolution(irc: ssl.SSLSocket):
    while True:
        data = irc.recv(1024)
        raw_message = data.decode('UTF-8')

        for line in raw_message.splitlines():
            if line.startswith('PING :tmi.twitch.tv'):
                twitch.send_pong(irc)
            else:
                components = line.split()
                command = components[1]

                if command == 'PRIVMSG':
                    if "!stand" == twitch.getMessage(line):
                        twitch.CalculateStand(irc, channel_name)
                    name = twitch.getName(line)
                    number = twitch.parseNumber(twitch.getMessage(line))
                    if name == twitch.admin and number is not None:
                        pprint(number)
                        return number


def collectData(irc: ssl.SSLSocket):
    users = []
    numbers = []
    while True:
        data = irc.recv(1024)
        raw_message = data.decode('UTF-8')

        for line in raw_message.splitlines():
            if line.startswith('PING :tmi.twitch.tv'):
                twitch.send_pong(irc)
            else:
                components = line.split()
                command = components[1]

                if command == 'PRIVMSG':
                    message = twitch.getMessage(line)
                    name = twitch.getName(line)
                    if "!stand" == message:
                        twitch.CalculateStand(irc, channel_name)
                    if name == twitch.admin and message == 'ende':
                        return users, numbers
                    number = twitch.parseNumber(message)
                    if name not in users and number is not None:
                        users.append(name)
                        numbers.append(number)
                    pprint(users)
                    pprint(numbers)


def determineWinner(users: list, numbers: list, solution: int):
    dif = 10000
    WinnerIndex = []
    length = len(numbers)
    i = 0
    while i < length:
        deff = solution - numbers[i]
        deff = abs(deff)
        if deff < dif:
            dif = deff
            if len(WinnerIndex) > 0:
                WinnerIndex.clear()
            WinnerIndex.append(numbers[i])
        elif deff == dif:
            WinnerIndex.append(numbers[i])
        i += 1
    winner = []
    ind = 0
    equal = False
    for y in numbers:
        if y == WinnerIndex[0]:
            winner.append(users[ind])
        ind = ind + 1
    if WinnerIndex[0] == solution:
        equal = True
    return winner, equal
