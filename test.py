import json

import requests

channel_name = "yarissi"

if __name__ == '__main__':
    response = requests.get(f"https://tmi.twitch.tv/group/user/{channel_name}/chatters")

    chatter = json.loads(response.text)['chatters']
    listChatter = []

    for type in chatter:
        for chatty in chatter[type]:
            listChatter.append(chatty)

    print(listChatter)