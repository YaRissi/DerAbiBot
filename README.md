[![DerAbiBot](img/lost.png)](https://github.com/yarissi/derabibot)


# Der Abi Bot

[![License: GPL v3](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE) [![Python 3](https://img.shields.io/badge/python-3-blue.svg)](https://www.python.org/)

DerAbiBot is a Twitch Bot written for the streamer [Der Abi](https://www.twitch.tv/der_abi__) and 
espacially for his personal show "Schlag den Abi", where you need a lot of interaction with the chat.
If you want to learn more, about how this show works, you can visit his [Homepage](https://derabi.com/)

## Installation

```$ pip install -r requirements.txt```

## Usage

Enter your personal oauth_token, channel-name and user-name in [config.toml](https://github.com/YaRissi/DerAbiBot/blob/main/ressources/config.toml)
```python
bot_username = 'xxxxxxx'
channel_name = 'xxxxxxx'
oauth_token = 'xxxxxxxxxxxx'
```

The Channel owner will always be one of the admins.\
Change the admin in twitch.py to your personal needs
```python
def checkAdmins(user):
    ....
    chatter = ['']
    ...
```

## Dokumentation

- *Keywords: Start and Ende* These two keywords mark the start and the end of each round. 
Its irrelevant, if you write them all in uppercase or all in lowercase.\
After the admin send the message "Ende", he can enter the solution in the chat.\
The Bot outputs the winner of this round and even tells you, if the winner hit a precision landing.\
The winner get a point added to their score. For a precision landing you get two points.\
If there are multiple winners, the round goes on to the play-offs, there is no need to write start again.
In this round, only the winners of the previous round can participate. At the end it's similar to a normal round.
The admins send the message "Ende" and the solution in the chat. Only the winner of this round gets the points.
- *Commands:*
    - *!stand:* Sends the current score in the chat
    - *!stand [user]:* Give the score of a specific user
    - *!help:* Refers to this repository
    - *!blöff:* How much blöff are you?
    - *!fight [user]:* Would you win in a fight against this user?
    - *!lieben [user]:* Picks a random user in the chat to be your love of your life
    - *!runde:* Send in which round you currently are in the chat
    - **Only for admin:**
      - *!reset:* Resets the current score
      - *!give [user] [points]:* Gives the user a specific amount of points
    

## License
MIT

See the [license](./LICENSE) document for the full text.
