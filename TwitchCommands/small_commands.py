import random

from pprint import pprint

import twitch


def fight(irc, channel_name, raw_message):
    line = twitch.getMessage(raw_message)
    if len(line.split(" ")) == 2:
        name = twitch.getName(raw_message)
        other_user = str(line.split(" ")[1]).lower()
        if other_user.startswith("@"):
            other_user = other_user.split("@")[1]
        if name == "test":
            message = f"{name} hat im 1vs1 gegen {other_user} mit einem dicken K.O. gewonnen. "
            twitch.send_chat(irc, message, channel_name)
            return
        rando = random.randint(0, 100)
        if (rando % 2) == 0:
            message = f"{name} hat im 1vs1 gegen {other_user} mit einem dicken K.O. gewonnen. "
        else:
            message = f"{name} hat im 1vs1 gegen {other_user} mit einem dicken K.O. verloren. "
        twitch.send_chat(irc, message, channel_name)


def blöff(irc, channel_name, raw_message):
    name = twitch.getName(raw_message)
    line = twitch.getMessage(raw_message)
    pprint(line)
    if len(line.split(" ")) == 2:
        name = str(line.split(" ")[1]).lower()
    if name == ("yarissi" or "der_abi__"):
        message = f"{name} ist zu 0% blöff. "
        twitch.send_chat(irc, message, channel_name)
        return
    rando = random.randint(0, 100)
    message = f"{name} ist zu {rando}% blöff. "
    twitch.send_chat(irc, message, channel_name)
