from flask import Flask, request, Response
import requests
import json

app = Flask(__name__)

@app.route('/')
    def hello():
        return "hello"

@app.route('/', methods=['POST'])
def respond():
    data = json.dumps(request.json, sort_keys=True,
                      indent=4, separators=(',', ': '))
    print(data)
    to_workplace()
    return Response(status=200)


def to_workplace():
    text = 'receive'
    url = 'https://graph.facebook.com/me/messages'
    token = 'DQVJzYXY3eG1RU3NBSEsya05sM2hqOEMwdkM0YkMwN1RSS3JoeWtYM05oRWRNT0JVb0drWEJsX2ZAuYzJJa2wwTWxmY0lqbUNnMElLVUMxMmxuQVhoc09KX2xjUFdNSlhjSl8yZAVhLT1VBUGRia1ROXzdzYVAyc082WFlXWVA5ZAXUxTU00dHR1czFkb21sUkFwUDQ3WDFuX1Vra1l4ZADVOUWtNQThkQU9rdkVLbEpOOGRsc0Q2dkVsbmt2aFhKOS10V2lhbWhn'
    data = {'recipient': {'id': '100063124216900'}, 'message': {'text': text}}

    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }

    response = requests.request(
        'POST',
        url,
        headers=headers,
        data=str(data)
    )

    print(response.text)
