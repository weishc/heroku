from flask import Flask, request, Response
import requests
import json

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
tid_wpid = {}
id_db = {}

def get_trello_staff():
    url = "https://api.trello.com/1/organizations/test84104475/members"

    response = requests.request(
        "GET",
        url,
        headers=tr_headers,
        params=query
    )

    return json.loads(response.text)

def get_wp_staff():
    url = 'https://graph.facebook.com/company/organization_members'
    response = requests.request(
        'GET',
        url,
        headers=wp_headers
    )
    return json.loads(response.text)['data']

for t in get_trello_staff():
    for w in get_wp_staff():
        if t['fullName'] in w['name']:
            tid_wpid[t['id']] = w['id']
            id_db[t['username']] = {
                'wp_id': w['id'], 'tr_id': t['id']}


@app.route('/')
def index():
    return 'Last update:2021/02/03 10:27'


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
        card_members_id = json.loads(get_card_members_id(card['id']))
        if commenter.split('renpic')[1] == shot_user:
            card_members_id.remove(id_db[commenter]['tr_id'])
        for i in card_members_id:
            if card['id'] not in get_unread_list(i):
                send_wp_ids.append(tid_wpid[i])
        if mention_list != []:
            for user in mention_list:
                tr_id = id_db[user.strip('@')]['tr_id']
                if card['id'] not in get_unread_list(trid):
                    send_wp_ids.append(id_db[user.strip('@')]['wp_id'])
        send_wpids = list(set(send_wpids))
        for wpid in send_wpids:
            send_msg(wpid)
    return Response(status=200)

def send_msg(id):
    req_data = request.json['action']['data']
    proj_name = req_data['list']['name']
    shot_name = req_data['card']['name']
    short_link = req_data['card']['shortLink']
    text = proj_name + r'\n' + shot_name + r'\n⚠️有新留言\nhttps://trello.com/c/' + short_link
    data = '{"recipient":{"id":"' + id + '"},"message":{"text":"' + text +'"}}'
    response = requests.request(
        'POST',
        'https://graph.facebook.com/me/messages',
        headers=wp_headers,
        data=data.encode('utf-8')
    )
    print(response.text)

def get_card_members_id(card_id):
    url = "https://api.trello.com/1/cards/"+card_id+'/idMembers'
    response = requests.request(
       "GET",
       url,
       headers=tr_headers,
       params=query,
    )
    return response.text

def get_unread_list(id):
    url = "https://api.trello.com/1/members/" + id + "/notifications/"
    query['read_filter'] = 'unread'
    query['fields'] = 'data'
    query['memberCreator_fields'] = ''
    response = requests.request(
       "GET",
       url,
       headers=tr_headers,
       params=query
    )
    notif_list = json.loads(response.text)
    return [i['data']['card']['id'] for i in notif_list]

if __name__ == '__main__':
    app.run(debug=True)
