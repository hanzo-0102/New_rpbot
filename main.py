import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import datetime
import sqlite3
import json


def main():
    world = json.load('world.json')
    npcs = json.load('npcs.json')
    mobs = json.load('mobs.json')
    locations = json.load('locations.json')
    vk_session = vk_api.VkApi(
        token=TOKEN)
    longpoll = VkBotLongPoll(vk_session, id_сообщества)
    con = sqlite3.connect("db_session.db")
    cur = con.cursor()
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            print(event)
            print('Новое сообщение:')
            print('Для меня от:', event.obj.message['from_id'])
            print('Текст:', event.obj.message['text'])
            text = event.obj.message['text']
            vk = vk_session.get_api()
            if event.obj.message['text'] not in cur.execute("""SELECT player id FROM main""").fetchall() and text[0] != '/':
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Приветствую Вас, Соискатель. Вас ожидает интересное приключение в"
                                         f" мире Зельтронии. Я - Ваш проводник. Меня зовут C:\\Users\\...\\main.py, но"
                                         f"Вы можете звать меня Консуас. Для начала предлагаю Вам создать персонажа. Дл"
                                         f"я"
                                         "этого напишите в чат /создать {имя вашего персонажа} {раса персонажа} {класс "
                                         "персонажа}\nРаса персонажа должна входить в список : {орк, дварф, человек, "
                                         "эльф}. А класс в список : {воин}.\nЕсли хотите узнать подробнее о расах и "
                                         "классах напишите в чат /инфо расы или /инфо классы",
                                 random_id=random.randint(0, 2 ** 64))
            elif text[0] == '/':
                if text[1:].split()[0] == 'помощь':
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=f"Общие :\n"
                                             f"место - выводит название локации и места в локации, где Вы находитесь\n"
                                             f"инвентарь - выведет информацию о Вашем инвентаре\n"
                                             f"уровень - выведет информацию о вашем уровне и очках опыта\n"
                                             "{название параметра} +{кол-во очков} - прокачает навык на определённое"
                                             " количество очков\n"
                                             f"Для битв :\n"
                                             "{название предмета} - использовать предмет\n"
                                             "сбежать - сбажеть",
                                     random_id=random.randint(0, 2 ** 64))
                elif text[1:].split()[0] == 'инфо':
                    if text[1:].split()[1] == 'расы':
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=f"Орк : +2 к СИЛЕ, +1 к ВЫНОСЛИВОСТИ, -2 к ХАРИЗМЕ, -1 к ИНТЕЛЛЕКТУ\n"
                                                 f"Дварф : +2 к ВЫНОСЛИВОСТИ, -1 к ХАРИЗМЕ, -1 к ЛОВКОСТИ\n"
                                                 f"Человек : никаких бонусов или минусов... жалкие людишки :)\n"
                                                 f"Эльф : +1 к ЛОВКОСТИ, +1 к ИНТЕЛЛЕКТУ, -2 к ВЫНОСЛИВОСТИ",
                                         random_id=random.randint(0, 2 ** 64))
                    elif text[1:].split()[1] == 'классы':
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=f"Воин : 7 СИЛЫ, 6 ВЫНОСЛИВОСТИ, 5 ЛОВКОСТИ, 4 МУДРОСТИ, 3 ИНТЕЛЛЕКТА,"
                                                 f"5 ХАРИЗМЫ",
                                         random_id=random.randint(0, 2 ** 64))
                    else:
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=f"Я вас не понимаю...",
                                         random_id=random.randint(0, 2 ** 64))
                elif text[1:].split()[0] == 'создать':
                    info = text[1:].split()
                    classes = {
                        "воин" : {
                            "STR" : 7,
                            "CON" : 6,
                            "DEX" : 5,
                            "WIS" : 4,
                            "INT" : 3,
                            "CHA" : 5
                        }
                    }
                    races = {
                        "орк" : {
                            "STR": 0,
                            "CON": 2,
                            "DEX": -1,
                            "WIS": 0,
                            "INT": 0,
                            "CHA": -1
                        },
                        "дварф": {
                            "STR": 2,
                            "CON": 2,
                            "DEX": 0,
                            "WIS": 0,
                            "INT": -1,
                            "CHA": -2
                        },
                        "человек": {
                            "STR": 0,
                            "CON": 0,
                            "DEX": 0,
                            "WIS": 0,
                            "INT": 0,
                            "CHA": 0
                        },
                        "эльф": {
                            "STR": 0,
                            "CON": -2,
                            "DEX": 1,
                            "WIS": 0,
                            "INT": 1,
                            "CHA": 0
                        }
                    }
                    if info[2].lower() in ['орк', 'дварф', 'человек', 'эльф'] and info[3].lower() in ['воин']:
                        cur.execute(f'''INSERT INTO main VALUES ({event.obj.message['text']}
                        1, 0, {2 * min(1, races[info[2].lower()]['CON'] + classes[info[3].lower()]['CON'])}
                        , {2 * min(1, races[info[2].lower()]['WIS'] + classes[info[3].lower()]['WIS'])},
                         {min(1, races[info[2].lower()]['STR'] + classes[info[3].lower()]['STR'])},
                         {min(1, races[info[2].lower()]['DEX'] + classes[info[3].lower()]['DEX'])},
                         {min(1, races[info[2].lower()]['WIS'] + classes[info[3].lower()]['WIS'])},
                         {min(1, races[info[2].lower()]['CON'] + classes[info[3].lower()]['CON'])},
                         {min(1, races[info[2].lower()]['INT'] + classes[info[3].lower()]['INT'])},
                         {min(1, races[info[2].lower()]['CHA'] + classes[info[3].lower()]['CHA'])},
                         {info[2].lower()}, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, {info[1]}, '', '', '', '', '', 'spawn',
                          'tavernspawn', 0)''')
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=f"Создан персонаж 1 уровня. Имя : {info[1]}\n"
                                                 f"Раса : {info[2]}, Класс : {info[3]}.\n\n"
                                                 f"Вы очнулись по центру прекрассного города А. Удачи в изучении мира."
                                                 f"Чтобы получить помощь в использовании комманд напишите /помощь.",
                                         random_id=random.randint(0, 2 ** 64))
                    else:
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=f"Я вас не понимаю...",
                                         random_id=random.randint(0, 2 ** 64))
            elif text == 'место':
                owner = event.obj.message['from_id']
                result = cur.execute(f"""SELECT world, location FROM main
                            WHERE player id = {owner}""").fetchall()
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Вы находитесь в {world[result[0][0]]['name']}. А если быть точнее то ваша локация это"
                                         f": {locations[result[0][1]]['name']}",
                                 random_id=random.randint(0, 2 ** 64))
            else:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Я вас не понимаю...",
                                 random_id=random.randint(0, 2 ** 64))
    con.close()



if __name__ == '__main__':
    main()
