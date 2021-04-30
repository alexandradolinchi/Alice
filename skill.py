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

weapon_list = {
    'cards': {
        'name': 'Карты',
        'img': '1521359/461c6503661d7278d741',
    },
    'cursed_gold': {
        'name': 'Проклятое золото',
        'img': '1030494/92d19a053f22042a4b53',
    },
    'whirlpool': {
        'name': 'Водоворот',
        'img': '1030494/022a6e9f86d5c40dc1e9',
    },
    'creepy_fish': {
        'name': 'Жуткая рыба',
        'img': '1521359/f47b05243fc4a5dff3e0',
    },
    'cannibal_cat': {
        'name': 'Кот-людоед',
        'img': '1030494/32dbe90d7115d95ed090',
    },
    'poisoned_potion': {
        'name': 'Отравленное зелье',
        'img': '1521359/d1da9563484c3b41ce73',
    },
}


def offer_class(user_id, req, res):
    for entity in req['request']['nlu']['entities']:
        if entity['type'] == 'YANDEX.FIO':
            if name := entity['value'].get('first_name'):
                name = name.capitalize()
                session_state[user_id]['first_name'] = name
                res['response']['text'] = f'Приятно познакомиться, {name}! Выбери свою стихию:'
                res['response']['card'] = {
                    'type': 'ItemsList',
                    'header': {
                        'text': f'Приятно познакомиться, {name}! Выбери свою стихию:'
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
        res['response']['txt'] = 'Я не расслышала! Повтори, пожалуйста'


def offer_adventure(user_id, req, res):
    try:
        selected_class = req['request']['payload']['class']
    except KeyError:
        res['response']['txt'] = 'Пожалуйста, выбери класс!'
        return
    session_state[user_id].update({
        'class': selected_class,
        'state': 3
    })
    res['response'] = {
        'text': f'{selected_class.capitalize()} - отличный выбор!(поговаривают, что этот воин непобедим..)',
        'card': {
            'type': 'BigImage',
            'image_id': player_class[selected_class]['img'],
            'title': f'{selected_class.capitalize()} - отличный выбор!(поговаривают, что этот воин непобедим..)',
        },

        'buttons': [
            {
                'title': 'В БОЙ',
                'payload': {'fight': True},
                'hide': True
            },
            {
                'title': 'Завершить приключение :(',
                'payload': {'fight': False},
                'hide': True
            }
        ]
    }


def weapon_selection(user_id, req, res):
    try:
        answer = req['request']['payload']['fight']
    except KeyError:
        res['response']['text'] = 'Пожалуйста, выбери оружие!'
        return

    if answer:
        res['response']['text'] = 'Пожалуйста, выбери оружие!'
        session_state[user_id]['state'] = 4
        if session_state[user_id]['class'] == 'gypsy_girl':
            res['response']['card'] = {
                'type': 'ItemsList',
                'header': {
                    'text': f'Выбери оружие:'
                },
                'items': [
                    {
                        'image_id': weapon_list['cards']['img'],
                        'title': weapon_list['cards']['name'],
                        'description': 'эти карты острее клинка.',
                    },
                    {
                        'image_id': weapon_list['cursed_gold']['img'],
                        'title': weapon_list['cursed_gold']['name'],
                        'description': 'лишь раз дотронься, познаешь ужас золотых монет.',
                    },
                ]
            }

            res['response']['buttons'] = [
                {
                    'title': 'Карты',
                    'payload': {'fight': True},
                    'hide': True
                },
                {
                    'title': 'Проклятое золото',
                    'payload': {'fight': True},
                    'hide': True
                }
            ]

        elif session_state[user_id]['class'] == 'water_man':
            res['response']['card'] = {
                'type': 'ItemsList',
                'header': {
                    'text': f'Выбери оружие:'
                },
                'items': [
                    {
                        'image_id': weapon_list['whirlpool']['img'],
                        'title': weapon_list['whirlpool']['name'],
                        'description': 'попав в него, выбраться уже не получится.',
                    },
                    {
                        'image_id': weapon_list['creepy_fish']['img'],
                        'title': weapon_list['creepy_fish']['name'],
                        'description': 'говорят, эта рыба может проглотить целиком кого угодно.',
                    },
                ]
            }

            res['response']['buttons'] = [
                {
                    'title': 'Водоворот',
                    'payload': {'fight': True},
                    'hide': True
                },
                {
                    'title': 'Жуткая рыба',
                    'payload': {'fight': True},
                    'hide': True
                }
            ]

        elif session_state[user_id]['class'] == 'baba_yaga':
            res['response']['card'] = {
                'type': 'ItemsList',
                'header': {
                    'text': f'Выбери оружие:'
                },
                'items': [
                    {
                        'image_id': weapon_list['cannibal_cat']['img'],
                        'title': weapon_list['cannibal_cat']['name'],
                        'description': 'съест и без специй.',
                    },
                    {
                        'image_id': weapon_list['poisoned_potion']['img'],
                        'title': weapon_list['poisoned_potion']['name'],
                        'description': 'от одного взгляда на бутылку становится дурно.',
                    },
                ],
            }

            res['response']['buttons'] = [
                {
                    'title': 'Кот-людоед',
                    'payload': {'fight': True},
                    'hide': True
                },
                {
                    'title': 'Отравленное зелье',
                    'payload': {'fight': True},
                    'hide': True
                }
            ]

    else:
        end_game(user_id, req, res)


def offer_fight(user_id, req, res):
    try:
        answer = req['request']['payload']['fight']
    except KeyError:
        res['response']['text'] = 'Пожалуйста, выбери действие!'
        return

    if answer:
        enemy = random.choice(enemy_list)
        session_state[user_id]['state'] = 5
        res['response'] = {
            'text': f'Бойся.. твой противник - ' + enemy['name'] + "!!!",
            'card': {
                'type': 'BigImage',
                'image_id': enemy['img'],
                'title': f'Бойся.. твой противник - ' + enemy['name'] + "!!!",
            },
            'buttons': [
                {
                    'title': 'УДАР',
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
        res['response']['text'] = 'Выберите действие, пожалуйста!'
        return
    if not answer:
        res['response']['text'] = 'Игра закончена! Даже не успев начаться!'
    else:
        res['response']['text'] = 'Вот ето да.. Победа твоя! Поздравляю'
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
    3: weapon_selection,
    4: offer_fight,
    5: end_game
}
session_state = {}

if __name__ == '__main__':
    app.run()
