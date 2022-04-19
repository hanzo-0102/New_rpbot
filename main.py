import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import datetime
import sqlite3
import json
from secrets import TOKEN, group_id


def main():
    in_dialogue = False
    curr = None
    dialogue = None
    with open('world.json', encoding='utf-8') as file:
        world = json.load(file)
    with open('npcs.json', encoding='utf-8') as file:
        npcs = json.load(file)
    with open('mobs.json', encoding='utf-8') as file:
        mobs = json.load(file)
    with open('locations.json', encoding='utf-8') as file:
        locations = json.load(file)
    vk_session = vk_api.VkApi(
        token=TOKEN)
    longpoll = VkBotLongPoll(vk_session, group_id)
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
            if (str(event.obj.message['from_id']),) not in cur.execute("""SELECT player_id FROM main""").fetchall() and \
                    text[0] != '/':
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
            elif in_dialogue and text in map(lambda y: y["text"], dialogue[curr]['choose']):
                for i in dialogue[curr]['choose']:
                    if text == i["text"]:
                        curr = i["next"]
                        if dialogue[curr]['type'] == 'dialog':
                            vk.messages.send(user_id=event.obj.message['from_id'],
                                             message=dialogue[curr]['text'],
                                             random_id=random.randint(0, 2 ** 64))
                            for j in dialogue[curr]['choose']:
                                vk.messages.send(user_id=event.obj.message['from_id'],
                                                 message=i['text'],
                                                 random_id=random.randint(0, 2 ** 64))
                        break
                if curr == "out":
                    in_dialogue = False
            elif text[0] == '/':
                if text[1:].split()[0] == 'помощь':
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=f"Общие :\n"
                                             f"место - выводит название локации и места в локации, где Вы находитесь\n"
                                             f"инвентарь - выведет информацию о Вашем инвентаре\n"
                                             f"уровень - выведет информацию о вашем уровне и очках опыта\n"
                                             f"ждать - восстановить 5 % от максимального здоровья, 10 % от максималь"
                                             f"ной маны, а также подождать событий вокруг (есть вероятность нарваться"
                                             f"на битву)\n"
                                             "{название параметра} +{кол-во очков} - прокачает навык на определённое"
                                             " количество очков\n"
                                             "квесты - выводит список квестов"
                                             "перейти {локация} - перемещает Вас в новую локацию/"
                                             "новое место в локации\n"
                                             "пути - показывает доступные места в локации, а также доступные для перех"
                                             "ода локации\n"
                                             "{название предмета} - использовать предмет\n"
                                             "квест - если возможно, то выполняет квестовое действие\n"
                                             f"Для битв :\n"
                                             "{название предмета} - использовать предмет\n"
                                             "сбежать - попытаться уйти с битвы"
                                             "враги - выводит список врагов"
                                             "{индекс врага} - устанавливает целью врага с выбранным индексом",
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
                        "воин": {
                            "STR": 7,
                            "CON": 6,
                            "DEX": 5,
                            "WIS": 4,
                            "INT": 3,
                            "CHA": 5
                        }
                    }
                    races = {
                        "орк": {
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
                        cur.execute(f'''INSERT INTO main(player_id,
                        level, experience, health, mana, STR, DEX, WIS, CON, INT, CHA,
                        RACE, wolf_fur, wolf_fang, common_training_sword, mana_potion,
                        bow, arrow, ruby, copper_coin, silver_coin, gold_coin, NAME,
                        equiped_weapon, equiped_helmet, equiped_chestplate, eqiped_leggings,
                         equiped_boots, world, location, exp_points, mode,
                         queue, quests) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                         ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (int(event.obj.message['from_id']),
                                                                                    1, 0, 2 * max(1, races[
                            info[2].lower()]['CON'] + classes[info[3].lower()]['CON']),
                                                                                    2 * max(1, races[info[2].lower()][
                                                                                        'WIS'] +
                                                                                            classes[info[3].lower()][
                                                                                                'WIS']),
                                                                                    max(1,
                                                                                        races[info[2].lower()]['STR'] +
                                                                                        classes[info[3].lower()][
                                                                                            'STR']),
                                                                                    max(1,
                                                                                        races[info[2].lower()]['DEX'] +
                                                                                        classes[info[3].lower()][
                                                                                            'DEX']),
                                                                                    max(1,
                                                                                        races[info[2].lower()]['WIS'] +
                                                                                        classes[info[3].lower()][
                                                                                            'WIS']),
                                                                                    max(1,
                                                                                        races[info[2].lower()]['CON'] +
                                                                                        classes[info[3].lower()][
                                                                                            'CON']),
                                                                                    max(1,
                                                                                        races[info[2].lower()]['INT'] +
                                                                                        classes[info[3].lower()][
                                                                                            'INT']),
                                                                                    max(1,
                                                                                        races[info[2].lower()]['CHA'] +
                                                                                        classes[info[3].lower()][
                                                                                            'CHA']),
                                                                                    info[2].lower(), 0, 0, 0, 0, 0, 0,
                                                                                    0, 0, 0, 0, info[1], '', '', '', '',
                                                                                    '', 'spawn',
                                                                                    'tavernspawn', 0, 'idle', '',
                                                                                    'story0'))
                        con.commit()
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=f"Создан персонаж 1 уровня. Имя : {info[1]}\n"
                                                 f"Раса : {info[2]}, Класс : {info[3]}.\n\n"
                                                 f"Вы очнулись в таверне прекрассного города А. Удачи в изучении мира."
                                                 f"Чтобы получить помощь в использовании комманд напишите /помощь.",
                                         random_id=random.randint(0, 2 ** 64))
                    else:
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=f"Я вас не понимаю...",
                                         random_id=random.randint(0, 2 ** 64))
            elif text == 'место':
                owner = event.obj.message['from_id']
                result = cur.execute(f"""SELECT world, location FROM main
                            WHERE player_id = {owner}""").fetchall()
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Вы находитесь в {world[result[0][0]]['name']}. А если быть точнее то в"
                                         f" {locations[result[0][1]]['name']}",
                                 random_id=random.randint(0, 2 ** 64))
            elif text == 'уровень':
                owner = event.obj.message['from_id']
                result = cur.execute(f"""SELECT level, experience, exp_points FROM main
                            WHERE player_id = {owner}""").fetchall()[0]
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Ваш текущий уровень : {result[0]}\n"
                                         f"До следующего уровня осталось : {(result[0] * 5) - result[1]}\n"
                                         f"Текущее кол-во нераспределённых очков навыков : {result[2]}",
                                 random_id=random.randint(0, 2 ** 64))
            elif text == 'инвентарь':
                owner = event.obj.message['from_id']
                result = cur.execute(f"""SELECT wolf_fur, wolf_fang, common_training_sword,
                 mana_potion, bow, arrow, ruby, copper_coin, silver_coin, gold_coin, equiped_weapon,
                  equiped_helmet, equiped_chestplate, eqiped_leggings, equiped_boots FROM main
                            WHERE player_id = {owner}""").fetchall()[0]
                wolf_fur = result[0]
                wolf_fang = result[1]
                common_training_sword = result[2]
                mana_potion = result[3]
                bow = result[4]
                arrow = result[5]
                ruby = result[6]
                copper_coin = result[7]
                silver_coin = result[8]
                gold_coin = result[9]
                equiped_weapon = result[10]
                equiped_helmet = result[11]
                equiped_chestplate = result[12]
                equiped_leggings = result[13]
                equiped_boots = result[14]
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"На Вас надето : {equiped_helmet}, {equiped_chestplate},"
                                         f"{equiped_leggings}, {equiped_boots}\n"
                                         f"В руках Вы держите : {equiped_weapon}\n"
                                         f"Также у Вас есть :"
                                         f"{f'{wolf_fur} волчья шерсть' if wolf_fur != 0 else ''}\n"
                                         f"{f'{wolf_fang} волчий клык' if wolf_fang != 0 else ''}\n"
                                         f"""{f'{common_training_sword} обычный меч для тренировок'
                                         if common_training_sword != 0 else ''}\n"""
                                         f"{f'{mana_potion} зелье маны' if mana_potion != 0 else ''}\n"
                                         f"{f'{bow} лук' if bow != 0 else ''}\n"
                                         f"{f'{arrow} стрела' if arrow != 0 else ''}\n"
                                         f"{f'{ruby} рубин' if ruby != 0 else ''}\n"
                                         f"{f'{copper_coin} медная монета' if copper_coin != 0 else ''}\n"
                                         f"{f'{silver_coin} серебрянная монета' if silver_coin != 0 else ''}\n"
                                         f"{f'{gold_coin} золотая монета' if gold_coin != 0 else ''}\n",
                                 random_id=random.randint(0, 2 ** 64))
            elif text == 'квесты':
                message = ''
                with open('quests.json') as f:
                    quests = json.load(f)
                for i in quests.keys():
                    for item in ['name', 'text', 'target']:
                        message += f"{item}: {quests[i][item]}\n"
                    message += '\n'
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Вам доступны квесты: {message}",
                                 random_id=random.randint(0, 2 ** 64))
            elif text.split()[0] == 'Поговорить':
                obj = text.split()[-1]
                with open('npcs.json') as f:
                    dialogue = json.load(f)
                dialogue = dialogue[obj]['dialog']
                curr = '00'
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=dialogue[curr]['text'],
                                 random_id=random.randint(0, 2 ** 64))
                for i in dialogue[curr]['choose']:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=i['text'],
                                     random_id=random.randint(0, 2 ** 64))
                in_dialogue = True
            elif text.split()[0] == 'перейти':
                to = ' '.join(text.split()[1:])
                x = {}
                for i in locations.keys():
                    x[locations[i]['name']] = i
                for i in world.keys():
                    x[world[i]['name']] = i
                if to in x.keys():
                    to1 = x[to]
                    owner = event.obj.message['from_id']
                    result = cur.execute(f"""SELECT world, location FROM main
                                                WHERE player_id = {owner}""").fetchall()[0]
                    if to1 in world[result[0]]['locations']:
                        cur.execute(f"""UPDATE main
                                        SET location = ?
                                        WHERE player_id = ?""", (to1, owner))
                        con.commit()
                        result = cur.execute(f"""SELECT world, location FROM main
                                                    WHERE player_id = {owner}""").fetchall()
                        mobs = cur.execute(f"""SELECT Name FROM Mobs WHERE World = ?""", (to1,)).fetchall()
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=f"Вы находитесь в {world[result[0][0]]['name']}. А если быть точнее то в"
                                                 f" {locations[result[0][1]]['name']}, Вы можете поговорить с любым из:\n",
                                         random_id=random.randint(0, 2 ** 64))
                        message = ''
                        for i in mobs:
                            message += i
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=message,
                                         random_id=random.randint(0, 2 ** 64))
                    elif to1 in world[result[0]]['paths']:
                        cur.execute(f"""UPDATE main
                                        SET world = ?
                                        WHERE player_id = ?""", (to1, owner))
                        to2 = world[to1]['locations'][0]
                        con.commit()
                        cur.execute(f"""UPDATE main
                                        SET location = ?
                                        WHERE player_id = ?""", (to2, owner))
                        con.commit()
                        result = cur.execute(f"""SELECT world, location FROM main
                                                                            WHERE player_id = {owner}""").fetchall()
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=f"Вы находитесь в {world[result[0][0]]['name']}. А если быть точнее то в"
                                                 f" {locations[result[0][1]]['name']}",
                                         random_id=random.randint(0, 2 ** 64))
                    else:
                        mobs = cur.execute(f"""SELECT Name FROM Mobs WHERE World = ?""", (to1,)).fetchall()
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=f"Отсюда туда добраться нельзя... Попробуй другое место. Но Вы можете поговорить с\n",
                                         random_id=random.randint(0, 2 ** 64))
                        message = ''
                        for i in mobs:
                            message += i[0]
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=message,
                                         random_id=random.randint(0, 2 ** 64))
                else:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=f"Я не знаю такого места :(",
                                     random_id=random.randint(0, 2 ** 64))
            elif text == "враги":
                message = ''
                with open('mobs.json') as f:
                    mobs = json.load(f)
                for i in mobs.keys():
                    message += f"{mobs[i]['name']}, health: {mobs[i]['health']}\n"
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Текущие враги:\n {message}",
                                 random_id=random.randint(0, 2 ** 64))
            elif text == "сбежать":
                if ("battle",) in cur.execute(
                        f"""SELECT mode FROM main WHERE player_id = {event.obj.message['from_id']}""").fetchall():
                    temp = random.randint(0, 1)
                    if temp:
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=f"Вы сбежали с поля боя",
                                         random_id=random.randint(0, 2 ** 64))
                    else:
                        vk.message.send(user_id=event.obj.message['from_id'],
                                        message=f"Вам не удалось совершить побег. За дизертирство вы были пойманы и временно забанены. Теперь вы не можете принимать участие в игре",
                                        random_id=random.randint(0, 2 ** 64))
            elif ("battle",) in cur.execute(
                    f"""SELECT mode FROM main WHERE player_id = {event.obj.message['from_id']}""").fetchall() and \
                    text.split()[0] == 'взять':
                with open("Weapons.json") as f:
                    weapons = json.load(f)
                temp = list(weapons.keys())
                text = text.split()[-1]
                for i in range(len(temp)):
                    temp[i] = weapons[temp[i]]['name']
                if text in temp:
                    cur.execute(f"""UPDATE main
                                    SET equiped_weapon = ?
                                    WHERE player_id = ?""", (text, event.obj.message['from_id'])).fetchall()
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=f'Вы выбрали на вооружение '
                                             f'{(cur.execute(f"""SELECT equiped_weapon FROM main WHERE player_id = {event.obj.message["from_id"]}""").fetchall())[0][0]}',
                                     random_id=random.randint(0, 2 ** 64))
            else:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"""Я вас не понимаю...""",
                                 random_id=random.randint(0, 2 ** 64))
    con.close()


if __name__ == '__main__':
    main()
