from flask import Flask, request, Response
import requests
import json

app = Flask(__name__)
staff_db = [{'name': 'test man', 'id': '100061038601811'}, {'name': 'Wei-Xiang Chen', 'id': '100063124216900'}]

@app.route('/')
def index():
    return 'yo'


@app.route('/', methods=['POST'])
def respond():
    action_type = request.json['action']['type']
    if action_type == 'commentCard':
        comment_creator = request.json['action']['"memberCreator']['fullName']
        receive_staff = ['test man','Wei-Xiang Chen (wc)',comment_creator]
        for i in staff_db:
            if i['name'] in receive_staff:
                send_msg(i['id'])
    return Response(status=200)


def send_msg(id):
    request_data = request.json['action']['data']
    proj_name = request_data['list']['name']
    shot_name = request_data['card']['name']
    short_link = request_data['card']['shortLink']
    text = proj_name + r'\n' + shot_name + r'\n⚠️有新留言\nhttps://trello.com/c/' + short_link
    url = 'https://graph.facebook.com/me/messages'
    token = 'DQVJzYXY3eG1RU3NBSEsya05sM2hqOEMwdkM0YkMwN1RSS3JoeWtYM05oRWRNT0JVb0drWEJsX2ZAuYzJJa2wwTWxmY0lqbUNnMElLVUMxMmxuQVhoc09KX2xjUFdNSlhjSl8yZAVhLT1VBUGRia1ROXzdzYVAyc082WFlXWVA5ZAXUxTU00dHR1czFkb21sUkFwUDQ3WDFuX1Vra1l4ZADVOUWtNQThkQU9rdkVLbEpOOGRsc0Q2dkVsbmt2aFhKOS10V2lhbWhn'
    data ='{"recipient":{"id":"' + id + '"},"message":{"text":"'+ text +'"}}'

    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }

    response = requests.request(
        'POST',
        url,
        headers=headers,
        data=data.encode('utf-8')
    )

    print(response.text)





if __name__ == '__main__':
    app.run(debug=True)
