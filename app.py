from flask import Flask, request, Response
import requests
import json
import re

app = Flask(__name__)
wptoken = 'DQVJzYXY3eG1RU3NBSEsya05sM2hqOEMwdkM0YkMwN1RSS3JoeWtYM05oRWRNT0JVb0drWEJsX2ZAuYzJJa2wwTWxmY0lqbUNnMElLVUMxMmxuQVhoc09KX2xjUFdNSlhjSl8yZAVhLT1VBUGRia1ROXzdzYVAyc082WFlXWVA5ZAXUxTU00dHR1czFkb21sUkFwUDQ3WDFuX1Vra1l4ZADVOUWtNQThkQU9rdkVLbEpOOGRsc0Q2dkVsbmt2aFhKOS10V2lhbWhn'
wp_headers = {
    'Authorization': 'Bearer ' + wptoken,
    'Content-Type': 'application/json'
}
tr_headers = {"Accept": "application/json"}
query = {
    'key': 'e16b5d87b76092e1854b698a1cc9f465',
    'token': '1594c0a47da4689feb849ef6444572de271cd4ad664a5c46ac33ff31973733c7'
}
tid_wpid = {'6013adbeb2e35865db709850': '100063124216900'}
id_db = {'renpiczz': {'wp_id': '100063124216900',
                      'tr_id': '6013adbeb2e35865db709850'}}


@app.route('/')
def index():
    return 'Last update:2021/02/03 12:27'


@app.route('/', methods=['POST'])
def respond():
    req_act = request.json['action']
    act_type = req_act['type']
    req_data = req_act['data']
    card = req_data['card']
    if act_type == 'commentCard':
        commenter = req_act['memberCreator']['username']
        shot_user = card['name'].split('] [')[2]
        pattern = re.compile(r'@[a-z]+')
        mention_list = pattern.findall(req_data['text'])
        card_members_id = (get_card_members_id(card['id']))
        send_wp_ids = []
        if commenter.split('renpic')[1] == shot_user and card_members_id != []:
            card_members_id.remove(id_db[commenter]['tr_id'])
        for i in card_members_id:
            send_wp_ids.append(tid_wpid[i])
        if mention_list != []:
            for user in mention_list:
                send_wp_ids.append(id_db[user.strip('@')]['wp_id'])
        send_wp_ids = list(set(send_wp_ids))
        for i in send_wp_ids:
            send_msg(i)
    return Response(status=200)


def send_msg(id):
    req_data = request.json['action']['data']
    proj_name = req_data['list']['name']
    shot_name = req_data['card']['name']
    short_link = req_data['card']['shortLink']
    text = proj_name + r'\n' + shot_name + \
        r'\n⚠️有新留言\nhttps://trello.com/c/' + short_link
    data = '{"recipient":{"id":"' + id + '"},"message":{"text":"' + text + '"}}'
    response = requests.request(
        'POST',
        'https://graph.facebook.com/me/messages',
        headers=wp_headers,
        data=data.encode('utf-8')
    )
    print(response.text)


def get_card_members_id(card_id):
    url = "https://api.trello.com/1/cards/" + card_id + '/idMembers'
    response = requests.request(
        "GET",
        url,
        headers=tr_headers,
        params=query,
    )
    return json.loads(response.text)


if __name__ == '__main__':
    app.run(debug=True)
