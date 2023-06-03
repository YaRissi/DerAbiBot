from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import CommentEvent, ConnectEvent

client = TikTokLiveClient(unique_id="@julestat")


@client.on("connect")
async def on_connect(_: ConnectEvent):
    print("Connected to Room ID:", client.room_id)


# Notice no decorator?
async def on_comment(event: CommentEvent):
    print(f"{event.user.uniqueId} -> {event.comment}")


# Define handling an event via "callback"
client.add_listener("comment", on_comment)


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


def schlagdenabi():


if __name__ == '__main__':
    client.run()
