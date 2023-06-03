import json

user = "fsdafsadfsdaf"

if __name__ == '__main__':
    import requests

    headers = {
        'Authorization': 'Bearer yehy5oh2dy6kc54ft61ioz7xmyvdym',
        'Client-Id': 'gp762nuuoqcoxypju8c569th9wz7q5',
    }

    response = requests.get(f'https://api.twitch.tv/helix/users?login={user}', headers=headers)
    data = json.loads(response.text)

    print(response.text)
    print(data["data"])
    print(len(data["data"]) == 1)

