import json

import twitch


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


def resetStand(irc, channel_name):
    stand = load_Stand()
    stand.clear()
    write_stand(stand)
    twitch.send_chat(irc, 'Reset erfolgreich', channel_name)


def CalculateStand(irc, channel_name, line):
    stand = load_Stand()
    if len(stand) == 0:
        twitch.send_chat(irc, 'Es gibt noch keinen Spielstand', channel_name)
    elif len(line.split(" ")) == 2:
        key = str(line.split(" ")[1]).lower()
        if key.startswith("@"):
            key = key.split("@")[1]
        if key in stand.keys():
            punkteUser = str(key) + " = " + str(stand[key])
            twitch.send_chat(irc, punkteUser, channel_name)
        else:
            CalculateStand(irc, channel_name, line.split(" ")[0])
    else:
        spielstand = ""
        for key in sorted(stand.items(), key=lambda item: item[1], reverse=True):
            name = str(key).split("'")[1]
            punkte = str(key).split(", ")[1].split(")")[0]
            punktePerson = name + " = " + punkte + " "
            spielstand = spielstand + punktePerson
        twitch.send_chat(irc, spielstand, channel_name)
    write_stand(stand)


def give_Points(irc, channel_name, line):
    stand = load_Stand()
    if len(line.split(" ")) == 3:
        key = str(line.split(" ")[1]).lower()
        if key.startswith("@"):
            key = key.split("@")[1]
        if key in stand.keys() or key in twitch.getUserList(channel_name):
            number = twitch.parseNumber(line.split(" ")[2])
            # Nummer ung??ltig oder Nummer gleich 0
            if number is None or number == 0:
                twitch.send_chat(irc, "Ach be du bekommst keine Punkte", channel_name)
            else:
                if key not in stand:
                    # if user has no points
                    if number < 1:
                        twitch.send_chat(irc, "Der User hat noch keine Punkte", channel_name)
                        return
                    stand[key] = number
                else:
                    stand[key] = stand.get(key) + number
                    # if user has less than 0 points
                    if stand.get(key) < 1:
                        del stand[key]
                        write_stand(stand)
                        twitch.send_chat(irc, "Der User wurde von der Liste entfernt", channel_name)
                        return
                write_stand(stand)
                if number > 1:
                    punkteUser = str(key) + " wurden " + str(number) + " Punkte gegeben."
                elif number == 1:
                    punkteUser = str(key) + " wurde einen Punkte gegeben."
                elif number == -1:
                    punkteUser = str(key) + " wurde einen Punkte abgezogen."
                else:
                    punkteUser = str(key) + " wurden " + str(abs(number)) + " Punkte abgezogen."
                twitch.send_chat(irc, punkteUser, channel_name)
        else:
            twitch.send_chat(irc, "Ung??ltiger Benutzername", channel_name)
    else:
        twitch.send_chat(irc, "Ung??ltiges Format: !give [username] [points]", channel_name)
