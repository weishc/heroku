from flask import Flask, request, Response
import requests
import json

app = Flask(__name__)
wp_staff_db = [{'name': 'test man (yc)', 'id': '100061038601811'}, {'name': 'Wei-Xiang Chen (wc)', 'id': '100063124216900'}]
headers = {"Accept": "application/json"}
query = {
    'key': 'e16b5d87b76092e1854b698a1cc9f465',
    'token': '1594c0a47da4689feb849ef6444572de271cd4ad664a5c46ac33ff31973733c7'
}  

@app.route('/')
def index():
    return 'yo'


@app.route('/', methods=['POST'])
def respond():
    action_type = request.json['action']['type']
    request_data = request.json['action']['data']

    if action_type == 'commentCard':
        card_id = request_data['card']['id']
        card_members_id = json.loads(get_card_members_id(card_id))
        card_members_name = []

        for i in card_members_id:
            card_members_name.append(get_fullname(i))
        send_wpids = []

        for staff in wp_staff_db:
            mention = '@renpic' + staff['name'].split('(')[1].strip(')')
            if mention in request_data['text']:
                send_wpids.append(staff['id'])
            if staff['name'].split(' (')[0] in card_members_name:
                send_wpids.append(staff['id'])
        send_wpids = list(set(send_wpids))

        for wpid in send_wpids:
            send_msg(wpid)

    return Response(status=200)


def send_msg(id):
    request_data = request.json['action']['data']
    proj_name = request_data['list']['name']
    shot_name = request_data['card']['name']
    short_link = request_data['card']['shortLink']
    text = proj_name + r'\n' + shot_name + r'\n⚠️有新留言\nhttps://trello.com/c/' + short_link
    wptoken = 'DQVJzYXY3eG1RU3NBSEsya05sM2hqOEMwdkM0YkMwN1RSS3JoeWtYM05oRWRNT0JVb0drWEJsX2ZAuYzJJa2wwTWxmY0lqbUNnMElLVUMxMmxuQVhoc09KX2xjUFdNSlhjSl8yZAVhLT1VBUGRia1ROXzdzYVAyc082WFlXWVA5ZAXUxTU00dHR1czFkb21sUkFwUDQ3WDFuX1Vra1l4ZADVOUWtNQThkQU9rdkVLbEpOOGRsc0Q2dkVsbmt2aFhKOS10V2lhbWhn'
    data ='{"recipient":{"id":"' + id + '"},"message":{"text":"'+ text +'"}}'

    wpheaders = {
        'Authorization': 'Bearer ' + wptoken,
        'Content-Type': 'application/json'
    }

    response = requests.request(
        'POST',
        'https://graph.facebook.com/me/messages',
        headers=wpheaders,
        data=data.encode('utf-8')
    )

    print(response.text)

def get_card_members_id(card_id):
    url = "https://api.trello.com/1/cards/"+card_id+'/idMembers'

    response = requests.request(
       "GET",
       url,
       headers=headers,
       params=query,
    )

    return response.text

def get_username(id):
    url = "https://api.trello.com/1/members/" + id + "/username"

    response = requests.request(
       "GET",
       url,
       headers=headers,
       params=query
    )

    return json.loads(response.text)['_value']

def get_fullname(id):
    url = "https://api.trello.com/1/members/" + id + '/fullName'

    response = requests.request(
       "GET",
       url,
       headers=headers,
       params=query
    )

    return json.loads(response.text)['_value']

if __name__ == '__main__':
    app.run(debug=True)
