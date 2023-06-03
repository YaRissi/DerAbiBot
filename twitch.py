import json
import socket
import ssl
from typing import Union, Any

import requests as requests 
import toml

from TwitchCommands import schlagdenabi_Runde
from TwitchCommands.side_commands_schlagdenabi import *


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


def schlagdenabiEqual(irc, winners):
    users, numbers = schlagdenabi_Runde.collectDataEqual(irc, winners)
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
    message = ' '.join(components[3:])[1:].lower()

    if checkAdmins(user) and message == "start":
        return 'start'
    if message.split(" ")[0] == "!stand":
        CalculateStand(irc, channel_name, getMessage(raw_message))
    # if message.split(" ")[0] == "!fight":
    #    small_commands.fight(irc, channel_name, raw_message)
    # if message.split(" ")[0] == "!blöff":
    #    small_commands.blöff(irc, channel_name, raw_message)
    # if message.split(" ")[0] == "!lieben":
    #    small_commands.lieben(irc, channel_name, raw_message)
    if message == "!commands":
        send_chat(irc, "Hier kommt ihr zu den Commands vom Abi Bot: https://github.com/YaRissi/DerAbiBot#dokumentation",
                  channel_name)
    if message == "!runde":
        send_chat(irc, f"Es wurde gerade die {readZähler()}. Runde gespielt", channel_name)
    if message == "!streams":
        send_chat(irc, f"Der Abi hat schon {getStreams(channel_name)} mal gestreamt.",
                  channel_name)
    if checkAdmins(user) and message == "!reset":
        resetStand(irc, channel_name)
    if checkAdmins(user) and message == "!endstand":
        return "!endstand"
    if checkAdmins(user) and message.split(" ")[0] == "!give":
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


def checkUserExist(user):
    import requests

    headers = {
        'Authorization': 'Bearer yehy5oh2dy6kc54ft61ioz7xmyvdym',
        'Client-Id': 'gp762nuuoqcoxypju8c569th9wz7q5',
    }

    response = requests.get(f'https://api.twitch.tv/helix/users?login={user}', headers=headers)
    test = json.loads(response.text)

    return len(test["data"]) == 1


def checkAdmins(user):
    config = toml.load("ressources/config.toml")
    channel_name = config['channel_name']
    # response = requests.get(f"https://tmi.twitch.tv/group/user/{channel_name}/chatters")
    # chatter = json.loads(response.text)['chatters']['moderators']
    chatter = ['yarissi', 'enes52_bjk', 'dilarax57', 'kassim_almaliky']

    return user in chatter or user == channel_name


def getStreams(channel_name):
    import re
    import cloudscraper
    from bs4 import BeautifulSoup

    scraper = cloudscraper.create_scraper(browser={'browser': 'firefox', 'platform': 'windows', 'mobile': False})

    html = scraper.get(f"https://sullygnome.com/channel/{channel_name}/2021").content
    soup = BeautifulSoup(html, 'html.parser')
    match = re.findall('<div class="InfoStatPanelTLCell"[^>]*>[^>]*</div>', str(soup))
    firstyear_streams = match[5].split("<")[1].split(">")[1]

    html = scraper.get(f"https://sullygnome.com/channel/{channel_name}/2022").content
    soup = BeautifulSoup(html, 'html.parser')
    match = re.findall('<div class="InfoStatPanelTLCell"[^>]*>[^>]*</div>', str(soup))
    secondyear_streams = match[5].split("<")[1].split(">")[1]

    html = scraper.get(f"https://sullygnome.com/channel/{channel_name}/2023").content
    soup = BeautifulSoup(html, 'html.parser')
    match = re.findall('<div class="InfoStatPanelTLCell"[^>]*>[^>]*</div>', str(soup))
    thirdyear_streams = match[5].split("<")[1].split(">")[1]

    total_streams = int(firstyear_streams)+int(secondyear_streams)+int(thirdyear_streams)
    return total_streams


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

    send_chat(irc, 'Bot is running MrDestructoid', channel_name)

    stand: dict[Union[list[Any], Any], Union[int, Any]] = {}

    writeZähler(0)
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
                        while user is not None and len(user) > 1:
                            user, equal = schlagdenabiEqual(irc, user)
                        if user is not None and len(user) == 1:
                            incrementRundenZähler()
                            give_Winner_Points(user, equal)
                        elif user is None:
                            send_chat(irc, "Ach be keiner hat mitgemacht", channel_name)
