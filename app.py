from flask import Flask, request, Response
import requests
import json

app = Flask(__name__)


@app.route('/')
def index():
    return 'yo'


@app.route('/', methods=['POST'])
def respond():
    action_type = request.json['action']['type']
    if action_type == 'commentCard':
        to_workplace()
    return Response(status=200)


def to_workplace():
    proj_name = request.json['action']['data']['list']['name']
    shot_name = request.json['action']['data']['card']['name']
    short_link = request.json['action']['data']['card']['shortLink']
    text = proj_name + '\n' + shot_name + '\n有未讀留言\nhttps://trello.com/c/' + short_link
    url = 'https://graph.facebook.com/me/messages'
    token = 'DQVJzYXY3eG1RU3NBSEsya05sM2hqOEMwdkM0YkMwN1RSS3JoeWtYM05oRWRNT0JVb0drWEJsX2ZAuYzJJa2wwTWxmY0lqbUNnMElLVUMxMmxuQVhoc09KX2xjUFdNSlhjSl8yZAVhLT1VBUGRia1ROXzdzYVAyc082WFlXWVA5ZAXUxTU00dHR1czFkb21sUkFwUDQ3WDFuX1Vra1l4ZADVOUWtNQThkQU9rdkVLbEpOOGRsc0Q2dkVsbmt2aFhKOS10V2lhbWhn'
    data = "{\"recipient\": {\"id\": \"100063124216900 \"},\"message\": {\"text\": \""+ text.encode('utf-8') +"\"}}"

    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }

    response = requests.request(
        'POST',
        url,
        headers=headers,
        # proxies=proxies,
        data=data
    )

    print(response.text)


if __name__ == '__main__':
    app.run(debug=True)
