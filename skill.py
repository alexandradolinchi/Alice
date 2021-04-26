import json
import random

from flask import Flask, request
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
run_with_ngrok(app)

player_class = {
    'gypsy_girl': {
        'name': 'Цыганка',
        'img': '997614/70c72e2d826c0c6989f1',
    },
    'water_man': {
        'name': 'Водяной',
        'img': '1652229/40b9b28f46168ae8f39c',
    },
    'baba_yaga': {
        'name': 'Баба-Яга',
        'img': '965417/adb9887cdc82e7d3443a',
    }
}

enemy_list = [
    {'name': 'Дюдюка', 'img': '1521359/72a82ea0ac64b64101cc'},
    {'name': 'Штуша Кутуша', 'img': '997614/38a6a7ed688dbe8ee777'},
    {'name': 'Волк', 'img': '965417/d0bcfdc8f1d91dc7e4f2'},
]


def offer_class(user_id, req, res):
    for entity in req['request']['nlu']['entities']:
        if entity['type'] == 'YANDEX.FIO':
            if name := entity['value'].get('first_name'):
                name = name.capitalize()
                session_state[user_id]['first_name'] = name
                res['response']['text'] = f'приятно познакомиться, {name}, выбери свою стихию'
                res['response']['card'] = {
                    'type': 'ItemsList',
                    'header': {
                        'text': f'приятно познакомиться, {name}, выбери свою стихию'
                    },
                    'items': [
                        {
                            'image_id': player_class['baba_yaga']['img'],
                            'title': player_class['baba_yaga']['name'],
                            'description': 'метла может разогнаться до 299,792,458 м/с.',
                        },
                        {
                            'image_id': player_class['gypsy_girl']['img'],
                            'title': player_class['gypsy_girl']['name'],
                            'description': 'карты никогда не врут.',
                        },
                        {
                            'image_id': player_class['water_man']['img'],
                            'title': player_class['water_man']['name'],
                            'description': 'утопнуть можно даже в луже.',

                        }
                    ],
                    'footer': {
                        'text': 'не ошибись с выбором, путник..'
                    }
                }
                res['response']['buttons'] = [
                    {
                        'title': 'Цыганка',
                        "payload": {'class': 'gypsy_girl'},
                        'hide': True
                    },
                    {
                        'title': 'Водяной',
                        "payload": {'class': 'water_man'},
                        'hide': True
                    },
                    {
                        'title': 'Баба-Яга',
                        "payload": {'class': 'baba_yaga'},
                        'hide': True
                    }
                ]
                session_state[user_id] = {
                    'state': 2
                }

        return
    else:
        res['response']['txt'] = 'я не расслышала! повтори пж'


def offer_adventure(user_id, req, res):
    try:
        selected_class = req['request']['payload']['class']
    except KeyError:
        res['response']['txt'] = 'пж выбери класс!'
        return
    session_state[user_id].update({
        'class': selected_class,
        'state': 3
    })
    res['response'] = {
        'text': f'{selected_class.capitalize()} - отличный выбор!',
        'card': {
            'type': 'BigImage',
            'image_id': player_class[selected_class]['img'],
            'title': f'{selected_class.capitalize()} - отличный выбор!',
        },
        'buttons': [
            {
                'title': 'В БОЙ',
                'payload': {'fight': True},
                'hide': True
            },
            {
                'title': 'завершить приключение :(',
                'payload': {'fight': False},
                'hide': True
            }
        ]
    }


def offer_fight(user_id, req, res):
    try:
        answer = req['request']['payload']['fight']
    except KeyError:
        res['response']['text'] = 'пж выбери действие'
        return

    if answer:
        enemy = random.choice(enemy_list)
        session_state[user_id]['state'] = 4
        res['response'] = {
            'text': f'бойся, твой противник - ' + {enemy['name']},
            'card': {
                'type': 'BigImage',
                'image_id': enemy['img'],
                'title': f'бойся, твой противник - ' + {enemy['name']},
            },
            'buttons': [
                {
                    'title': 'БЕЙ',
                    'payload': {'fight': True},
                    'hide': True
                },
                {
                    'title': 'БЕЖАААТЬ',
                    'payload': {'fight': False},
                    'hide': True
                }
            ]
        }
    else:
        end_game(user_id, req, res)


def end_game(user_id, req, res):
    try:
        answer = req['request']['payload']['fight']
    except KeyError:
        res['response']['text'] = 'выберите действие пж'
        return
    if not answer:
        res['response']['text'] = 'игра закончена! не успев начаться!'
    else:
        res['response']['text'] = 'вот ето да. вы победили. поздравляем!'
    res['response']['end_session'] = True


@app.route('/post', methods=['POST'])
def get_alice_request():
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    handle_dialog(request.json, response)
    return json.dumps(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']
    if req['session']['new']:
        res['response']['text'] = 'Привет! Как твое имя?'
        session_state[user_id] = {
            'state': 1
        }
        return
    states[session_state[user_id]['state']](user_id, req, res)


states = {
    1: offer_class,
    2: offer_adventure,
    3: offer_fight,
    4: end_game
}
session_state = {}

if __name__ == '__main__':
    app.run()
