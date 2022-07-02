import ssl
from pprint import pprint

import toml

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
                    if "!stand" == twitch.getMessage(line).split(" ")[0]:
                        twitch.CalculateStand(irc, channel_name, twitch.getMessage(line))
                    name = twitch.getName(line)
                    number = twitch.parseNumber(twitch.getMessage(line))
                    if name == twitch.admin and number is not None:
                        pprint("Lösung: " + str(number))
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
                    if "!stand" == twitch.getMessage(line).split(" ")[0]:
                        twitch.CalculateStand(irc, channel_name, twitch.getMessage(line))
                    if name == twitch.admin and (message == 'ende' or message == 'Ende' or message == 'ENDE'):
                        return users, numbers
                    number = twitch.parseNumber(message)
                    if name not in users and number is not None:
                        users.append(name)
                        numbers.append(number)
                    pprint(users)
                    pprint(numbers)


def determineWinner(users: list, numbers: list, solution: int):
    actualDifference = float('inf')
    WinnerIndex = []
    i = 0
    for value in numbers:
        DifferenceOfValue = abs(solution - value)
        if DifferenceOfValue < actualDifference:
            actualDifference = DifferenceOfValue
            if len(WinnerIndex) > 0:
                WinnerIndex.clear()
            WinnerIndex.append(i)
        elif DifferenceOfValue == actualDifference:
            WinnerIndex.append(i)
        i += 1
    winner = []
    equal = False
    for index in WinnerIndex:
        winner.append(users[index])
    if numbers[WinnerIndex[0]] == solution:
        equal = True
    return winner, equal
