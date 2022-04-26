import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import datetime
import sqlite3
import json


def main():
    with open('world.json', encoding='utf-8') as file:
        world = json.load(file)
    with open('npcs.json', encoding='utf-8') as file:
        npcs = json.load(file)
    with open('mobs.json', encoding='utf-8') as file:
        mobs = json.load(file)
    with open('locations.json', encoding='utf-8') as file:
        locations = json.load(file)
    with open('weapons.json', encoding='utf-8') as file:
        weapons = json.load(file)
    with open('food.json', encoding='utf-8') as file:
        food = json.load(file)
    vk_session = vk_api.VkApi(
        token='50f9dff39373368d994a39535633bc4794c7d7cc3777c2562940b5d59ed3e9fc67c82cd0dce2ef0d775b4')
    longpoll = VkBotLongPoll(vk_session, '212262401')
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
            owner = event.obj.message['from_id']
            if (str(event.obj.message['from_id']),) not in cur.execute("""SELECT player_id FROM main""").fetchall() and \
                    text[0] != '/':
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Приветствую Вас, Соискатель. Вас ожидает интересное приключение в"
                                         f" мире Зельтронии. Я - Ваш проводник. Меня зовут C:\\Users\\...\\main.py, но "
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
                                             f"ждать - восстановить 5 % от максимального здоровья, 10 % от максималь"
                                             f"ной маны, а также подождать событий вокруг (есть вероятность нарваться"
                                             f"на битву)\n"
                                             "{название параметра} +{кол-во очков} - прокачает навык на определённое"
                                             " количество очков\n"
                                             "квесты - выводит список квестов"
                                             "перейти {локация} - перемещает Вас в новую локацию/"
                                             "новое место в локации\n"
                                             "торговля - выводит список торговли если возможно\n"
                                             "торговать {номер} - обменивает предметы по сделке с выбранным номером\n"
                                             "пути - показывает доступные места в локации, а также доступные для перех"
                                             "ода локации\n"
                                             "{название предмета} - использовать предмет\n"
                                             "квест - если возможно, то выполняет квестовое действие\n"
                                             f"Для битв :\n"
                                             "{название предмета} - использовать предмет\n"
                                             "сбежать - попытаться уйти с битвы\n"
                                             "враги - выводит список врагов\n"
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
            elif text == 'пути':
                owner = event.obj.message['from_id']
                result = cur.execute(f"""SELECT world FROM main
                            WHERE player_id = {owner}""").fetchall()
                canto = [world[i]['name'] for i in world[result[0][0]]['paths']]
                canto1 = [locations[i]['name'] for i in world[result[0][0]]['locations']]
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Вы можете перейти в {', '.join(canto)}.\n"
                                         f"А также вы можете попасть в {', '.join(canto1)}.",
                                 random_id=random.randint(0, 2 ** 64))
            elif text == "торговля":
                owner = event.obj.message['from_id']
                result = cur.execute(f"""SELECT location FROM main
                                            WHERE player_id = {owner}""").fetchall()[0][0]
                level = cur.execute(f"""SELECT level FROM main
                                            WHERE player_id = {owner}""").fetchall()[0][0]
                if not locations[result]['trade']:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=f"Торговцев здесь нет... Эх :(",
                                     random_id=random.randint(0, 2 ** 64))
                else:
                    trades = locations[result]['trade_list']
                    number = 1
                    for i in trades.keys():
                        if int(i) < level:
                            for j in trades[i]:
                                vk.messages.send(user_id=event.obj.message['from_id'],
                                                 message=f"Сделка номер {number} :"
                                                         f" Вы отдадите {j['give_count']} {j['give']}, а получите"
                                                         f" {j['got_count']} {j['got']}",
                                                 random_id=random.randint(0, 2 ** 64))
                                number += 1
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
                  equiped_helmet, equiped_chestplate, eqiped_leggings, equiped_boots, jigsaw, mace, stuff,
                  magic_stuff, wolf_dagger, stuff_of_dwarfs_god, potato, turnip, yellow_alcohol_drink FROM main
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
                jigsaw = result[15]
                mace = result[16]
                stuff = result[17]
                magic_stuff = result[18]
                wolf_dagger = result[19]
                stuff_of_dwarfs_god = result[20]
                potato = result[21]
                turnip = result[22]
                yellow_alcohol_drink = result[23]
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"На Вас надето : {equiped_helmet}, {equiped_chestplate},"
                                         f"{equiped_leggings}, {equiped_boots}\n"
                                         f"В руках Вы держите : {equiped_weapon}\n"
                                         f"Также у Вас есть :\n"
                                         f"{f'{wolf_fur} волчья шерсть' if wolf_fur != 0 else ''}\n"
                                         f"{f'{wolf_fang} волчий клык' if wolf_fang != 0 else ''}\n"
                                         f"{f'{jigsaw} сабля' if jigsaw != 0 else ''}\n"
                                         f"{f'{mace} булава' if mace != 0 else ''}\n"
                                         f"{f'{stuff} боевой посох' if stuff != 0 else ''}\n"
                                         f"""{f'{magic_stuff} волшебный посох уровня начинающий'
                                         if magic_stuff != 0 else ''}\n"""
                                         f"""{f'{wolf_dagger} кинжал из клыка вождя волков Белого клыка'
                                         if wolf_dagger != 0 else ''}\n"""
                                         f"""{f'{stuff_of_dwarfs_god} посох бога дварфов Берфестокто'
                                         if stuff_of_dwarfs_god != 0 else ''}\n"""
                                         f"""{f'{common_training_sword} обычный меч для тренировок'
                                         if common_training_sword != 0 else ''}\n"""
                                         f"""{f'{yellow_alcohol_drink} светло-жёлтый алкогольный напиток'
                                         if yellow_alcohol_drink != 0 else ''}\n"""
                                         f"{f'{potato} картошка' if potato != 0 else ''}\n"
                                         f"{f'{turnip} репка' if turnip != 0 else ''}\n"
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
                owner = event.obj.message['from_id']
                result = cur.execute(f"""SELECT quests FROM main
                                                                WHERE player_id = {owner}""").fetchall()[0]
                with open('quests.json', encoding='utf-8') as f:
                    quests = json.load(f)
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Вам доступны квесты :\n",
                                 random_id=random.randint(0, 2 ** 64))
                for i in result:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=f"Название : {quests[i]['name']}\n"
                                            f"Описание : {quests[i]['text']}\n"
                                            f"Цель : {quests[i]['target']}",
                                     random_id=random.randint(0, 2 ** 64))
            elif text.split()[0] == "торговать":
                totrade = int(text.split()[1])
                owner = event.obj.message['from_id']
                result = cur.execute(f"""SELECT location FROM main
                                            WHERE player_id = {owner}""").fetchall()[0][0]
                level = cur.execute(f"""SELECT level FROM main
                                            WHERE player_id = {owner}""").fetchall()[0][0]
                if not locations[result]['trade']:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=f"Торговцев здесь нет... Эх :(",
                                     random_id=random.randint(0, 2 ** 64))
                else:
                    trades = locations[result]['trade_list']
                    number = 1
                    for i in trades.keys():
                        if int(i) < level:
                            for j in trades[i]:
                                if number == totrade:
                                    give = cur.execute(f"""SELECT {j['give']} FROM main
                                                            WHERE player_id = {owner}""").fetchall()[0][0]
                                    got = cur.execute(f"""SELECT {j['got']} FROM main
                                                            WHERE player_id = {owner}""").fetchall()[0][0]
                                    if give >= j['give_count']:
                                        cur.execute(f"""UPDATE main
                                                        SET {j['give']} = ?
                                                        WHERE player_id = ?""", (give - j['give_count'], owner))
                                        con.commit()
                                        cur.execute(f"""UPDATE main
                                                        SET {j['got']} = ?
                                                        WHERE player_id = ?""", (got + j['got_count'], owner))
                                        con.commit()
                                        vk.messages.send(user_id=event.obj.message['from_id'],
                                                         message="Сделка прошла успешно !",
                                                         random_id=random.randint(0, 2 ** 64))
                                    else :
                                        vk.messages.send(user_id=event.obj.message['from_id'],
                                                         message="Торговец : У тебя нет материалов, а я в благородства"
                                                                 " играть не буду...",
                                                         random_id=random.randint(0, 2 ** 64))
                                number += 1
            elif text.split()[0] == 'перейти':
                mode = cur.execute(f"""SELECT mode FROM main
                                                                WHERE player_id = {owner}""").fetchall()[0][0]
                if mode != 'battle':
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
                            vk.messages.send(user_id=event.obj.message['from_id'],
                                             message=f"Вы находитесь в {world[result[0][0]]['name']}. А если быть точнее то в"
                                                     f" {locations[result[0][1]]['name']}",
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
                            print(world[result[0][0]]['mob_spawn'])
                            if world[result[0][0]]['mob_spawn']:
                                chance = random.randint(0, 100)
                                if chance >= 50:
                                    x = len(world[result[0][0]]['mob_list']) - 1
                                    queue = world[result[0][0]]['mob_list'][random.randint(0, x)]
                                    queue = f"{queue}-{mobs[queue]['health']}"
                                    cur.execute(f"""UPDATE main
                                                    SET queue = ?
                                                    WHERE player_id = ?""", (queue, owner))
                                    con.commit()
                                    cur.execute(f"""UPDATE main
                                                    SET mode = ?
                                                    WHERE player_id = ?""", ('battle', owner))
                                    con.commit()
                                    vk.messages.send(user_id=event.obj.message['from_id'],
                                                     message=f"На Вас напал/напали {queue}",
                                                     random_id=random.randint(0, 2 ** 64))
                        else:
                            vk.messages.send(user_id=event.obj.message['from_id'],
                                             message=f"Отсюда туда добраться нельзя... Попробуй другое место.",
                                             random_id=random.randint(0, 2 ** 64))
                    else:
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=f"Я не знаю такого места (",
                                         random_id=random.randint(0, 2 ** 64))
                else:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=f"Пока Вы находитесь в битве спокойно ходить нельзя :)",
                                     random_id=random.randint(0, 2 ** 64))
            elif text == 'враги':
                queue = cur.execute(f"""SELECT queue FROM main
                                             WHERE player_id = {owner}""").fetchall()[0][0]
                mode = cur.execute(f"""SELECT mode FROM main
                                             WHERE player_id = {owner}""").fetchall()[0][0]
                if mode == 'battle':
                    index = 0
                    for i in queue.split():
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=f"{index} : {i}",
                                         random_id=random.randint(0, 2 ** 64))
                        index += 1
                else:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=f"Вы пока ни с кем не сражаетесь :)",
                                     random_id=random.randint(0, 2 ** 64))
            elif text is enumerate:
                queue = cur.execute(f"""SELECT queue FROM main
                                                             WHERE player_id = {owner}""").fetchall()[0][0]
                mode = cur.execute(f"""SELECT mode FROM main
                                                             WHERE player_id = {owner}""").fetchall()[0][0]
                queue = queue.split()
                if mode == 'battle':
                    if len(queue) < int(text):
                        queue[0], queue[int(text)] = queue[int(text)], queue[0]
                    else:
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=f"ОШИБКА : Неверное число. Повторите попытку позже",
                                         random_id=random.randint(0, 2 ** 64))
                else:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=f"Вы пока ни с кем не сражаетесь :)",
                                     random_id=random.randint(0, 2 ** 64))
            elif text == 'сбежать':
                mode = cur.execute(f"""SELECT mode FROM main
                                                       WHERE player_id = {owner}""").fetchall()[0][0]
                if mode == 'battle':
                    chance = random.randint(0, 100)
                    if chance >= 80:
                        cur.execute(f"""UPDATE main
                                        SET mode = ?
                                        WHERE player_id = ?""",
                                    ('idle', owner))
                        con.commit()
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=f"Побег успешен :)",
                                         random_id=random.randint(0, 2 ** 64))
                    else:
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=f"Что-то пошло не так :/",
                                         random_id=random.randint(0, 2 ** 64))
                        queue = cur.execute(f"""SELECT queue FROM main
                                                                                   WHERE player_id = {owner}""").fetchall()[
                            0][0].split()
                        queue = [i.split('-') for i in queue]
                        if queue and mode == 'battle':
                            dmg = 0
                            armor = 0
                            for i in queue:
                                number = random.randint(0, len(mobs[i[0]]['attack']) - 1)
                                dmg += mobs[i[0]]['attack'][number]['dmg'] * armor
                                vk.messages.send(user_id=event.obj.message['from_id'],
                                                 message=f"Вас атоковал {i[0]} атакой {mobs[i[0]]['attack'][number]['name']}."
                                                         f" Вы получили {mobs[i[0]]['attack'][number]['dmg'] * armor} урона.",
                                                 random_id=random.randint(0, 2 ** 64))
                                if mobs[i[0]]['attack'][number]['effect'] == "posion":
                                    posion = random.randint(0, 1) * 5 * armor
                                    dmg += posion
                                    vk.messages.send(user_id=event.obj.message['from_id'],
                                                     message=f"Вы получили {posion * armor} урона из-за эффекта posion",
                                                     random_id=random.randint(0, 2 ** 64))
                                elif mobs[i[0]]['attack'][number]['effect'] == "stun":
                                    stun = random.randint(0, 1) * 30 * armor
                                    dmg += stun
                                    vk.messages.send(user_id=event.obj.message['from_id'],
                                                     message=f"Вы получили {stun * armor} урона из-за эффекта stun",
                                                     random_id=random.randint(0, 2 ** 64))
                                elif mobs[i[0]]['attack'][number]['effect'] == "run":
                                    will = bool(random.randint(0, 1))
                                    if will and i == queue[0]:
                                        vk.messages.send(user_id=event.obj.message['from_id'],
                                                         message=f"{queue[0][0]} сбежал",
                                                         random_id=random.randint(0, 2 ** 64))
                                        del queue[0]
                                elif mobs[i[0]]['attack'][number]['effect'] == "fire":
                                    fire = random.randint(1, 4) * armor
                                    dmg += fire
                                    vk.messages.send(user_id=event.obj.message['from_id'],
                                                     message=f"Вы получили {fire * armor} урона из-за эффекта fire",
                                                     random_id=random.randint(0, 2 ** 64))
                            cur.execute(f"""UPDATE main
                                            SET health = health - ?
                                            WHERE player_id = ?""",
                                        (dmg, owner))
                            con.commit()
                            health = cur.execute(f"""SELECT health FROM main
                                                    WHERE player_id = {owner}""").fetchall()[0][0]
                            vk.messages.send(user_id=event.obj.message['from_id'],
                                             message=f"У Вас осталось {health}",
                                             random_id=random.randint(0, 2 ** 64))
                else:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=f"А от кого сбегать то ?",
                                     random_id=random.randint(0, 2 ** 64))
            elif text in ['картошка', 'репка', 'зелье маны', 'светло-жёлтый алкогольный напиток']:
                owner = event.obj.message['from_id']
                mode = cur.execute(f"""SELECT mode FROM main
                                                       WHERE player_id = {owner}""").fetchall()[0][0]
                result = list(cur.execute(f"""SELECT health, mana FROM main
                                                       WHERE player_id = {owner}""").fetchall()[0])
                translate = {"картошка":"potato",
                             "репка":"turnip",
                             "зелье маны":"mana_potion",
                             "светло-жёлтый алкогольный напиток":"yellow_alcohol_drink"}
                command = f"SELECT {translate[text]} FROM main WHERE player_id = {owner}"
                if cur.execute(command).fetchall()[0][0]:
                    result[0] += food[translate[text]]['health_plus']
                    result[1] += food[translate[text]]['mana_plus']
                    cur.execute("UPDATE main SET health = ? WHERE player_id = ?", (result[0], owner))
                    con.commit()
                    cur.execute("UPDATE main SET mana = ? WHERE player_id = ?", (result[1], owner))
                    con.commit()
                    command = f"UPDATE main SET {translate[text]} = {translate[text]} - 1 WHERE player_id = {owner}"
                    cur.execute(command)
                    con.commit()
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=f"Вы съели {text}",
                                     random_id=random.randint(0, 2 ** 64))
                    if mode == 'battle':
                        dmg = 0
                        armor = 0
                        for i in queue:
                            number = random.randint(0, len(mobs[i[0]]['attack']) - 1)
                            dmg += mobs[i[0]]['attack'][number]['dmg'] * armor
                            vk.messages.send(user_id=event.obj.message['from_id'],
                                             message=f"Вас атоковал {i[0]} атакой {mobs[i[0]]['attack'][number]['name']}."
                                                     f" Вы получили {mobs[i[0]]['attack'][number]['dmg'] * armor} урона.",
                                             random_id=random.randint(0, 2 ** 64))
                            if mobs[i[0]]['attack'][number]['effect'] == "posion":
                                posion = random.randint(0, 1) * 5 * armor
                                dmg += posion
                                vk.messages.send(user_id=event.obj.message['from_id'],
                                                 message=f"Вы получили {posion * armor} урона из-за эффекта posion",
                                                 random_id=random.randint(0, 2 ** 64))
                            elif mobs[i[0]]['attack'][number]['effect'] == "stun":
                                stun = random.randint(0, 1) * 30 * armor
                                dmg += stun
                                vk.messages.send(user_id=event.obj.message['from_id'],
                                                 message=f"Вы получили {stun * armor} урона из-за эффекта stun",
                                                 random_id=random.randint(0, 2 ** 64))
                            elif mobs[i[0]]['attack'][number]['effect'] == "run":
                                will = bool(random.randint(0, 1))
                                if will and i == queue[0]:
                                    vk.messages.send(user_id=event.obj.message['from_id'],
                                                     message=f"{queue[0][0]} сбежал",
                                                     random_id=random.randint(0, 2 ** 64))
                                    del queue[0]
                            elif mobs[i[0]]['attack'][number]['effect'] == "fire":
                                fire = random.randint(1, 4) * armor
                                dmg += fire
                                vk.messages.send(user_id=event.obj.message['from_id'],
                                                 message=f"Вы получили {fire * armor} урона из-за эффекта fire",
                                                 random_id=random.randint(0, 2 ** 64))
                        cur.execute(f"""UPDATE main
                                        SET health = health - ?
                                        WHERE player_id = ?""",
                                    (dmg, owner))
                        con.commit()
                        health = cur.execute(f"""SELECT health FROM main
                                                WHERE player_id = {owner}""").fetchall()[0][0]
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=f"У Вас осталось {health}",
                                         random_id=random.randint(0, 2 ** 64))
                else:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=f"У Вас нет такого предмета",
                                     random_id=random.randint(0, 2 ** 64))
            elif text in ['обычный меч для тренировок', 'кулак', 'сабля', 'булава', 'боевой посох',
                          'кинжал из клыка вождя волков Белого клыка', 'волшебный посох уровня начинающий',
                          'посох бога дварфов Берфестокто']:
                owner = event.obj.message['from_id']
                mode = cur.execute(f"""SELECT mode FROM main
                                       WHERE player_id = {owner}""").fetchall()[0][0]
                translate = {"обычный меч для тренировок":"common_training_sword",
                             "кулак":"fist",
                             "jigsaw":"сабля",
                             "mace":"булава",
                             "stuff":"боевой посох",
                             "wolf_dagger":"кинжал из клыка вождя волков Белого клыка",
                             "magic_stuff":"волшебный посох уровня начинающий",
                             "stuff_of_dwarfs_god":"посох бога дварфов Берфестокто"}
                weapon = cur.execute(f"""SELECT equiped_weapon FROM main
                                                                WHERE player_id = {owner}""").fetchall()[0][0]
                if translate[text] == weapon:
                    if mode == 'idle':
                        if translate[text] != 'fist':
                            have = cur.execute(f"""SELECT {translate[text]} FROM main
                                                   WHERE player_id = {owner}""").fetchall()[0][0]
                            STR = cur.execute(f"""SELECT STR FROM main
                                                   WHERE player_id = {owner}""").fetchall()[0][0]
                            WIS = cur.execute(f"""SELECT WIS FROM main
                                                  WHERE player_id = {owner}""").fetchall()[0][0]
                            DEX = cur.execute(f"""SELECT DEX FROM main
                                                  WHERE player_id = {owner}""").fetchall()[0][0]
                            INT = cur.execute(f"""SELECT INT FROM main
                                                  WHERE player_id = {owner}""").fetchall()[0][0]
                            CHA = cur.execute(f"""SELECT CHA FROM main
                                                  WHERE player_id = {owner}""").fetchall()[0][0]
                            CON = cur.execute(f"""SELECT CON FROM main
                                                  WHERE player_id = {owner}""").fetchall()[0][0]
                            if have:
                                requirements = weapons[translate[text]]['need']
                                if (STR >= requirements['STR'] and WIS >= requirements['WIS'] and
                                    DEX >= requirements['DEX'] and INT >= requirements['INT'] and
                                    CHA >= requirements['CHA'] and CON >= requirements['CON']):
                                    cur.execute(f"""UPDATE main
                                                    SET equiped_weapon = ?
                                                    WHERE player_id = ?""", (translate[text], owner))
                                    con.commit()
                                    vk.messages.send(user_id=event.obj.message['from_id'],
                                                     message=f"Поздравляем ! {text} экипирован !",
                                                     random_id=random.randint(0, 2 ** 64))
                                else:
                                    vk.messages.send(user_id=event.obj.message['from_id'],
                                                     message=f"Кажется Вы недостаточно прокачаны :(",
                                                     random_id=random.randint(0, 2 ** 64))
                                    vk.messages.send(user_id=event.obj.message['from_id'],
                                                     message=f"Требования :\n"
                                                             f"СИЛА - {STR}"
                                                             f"ЛОВКОСТЬ - {DEX}"
                                                             f"ВЫНОСЛИВОСТЬ - {CON}"
                                                             f"МУДРОСТЬ - {WIS}"
                                                             f"ИНТЕЛЛЕКТ - {INT}"
                                                             f"ХАРИЗМА - {CHA}",
                                                     random_id=random.randint(0, 2 ** 64))
                            else:
                                vk.messages.send(user_id=event.obj.message['from_id'],
                                                 message=f"В рюкзак гляжу... оружия не нахожу",
                                                 random_id=random.randint(0, 2 ** 64))
                        else:
                            cur.execute(f"""UPDATE main
                                            SET equiped_weapon = ?
                                            WHERE player_id = ?""",
                                        (translate[text], owner))
                            con.commit()
                            vk.messages.send(user_id=event.obj.message['from_id'],
                                             message=f"Поздравляем ! {text} экипирован !",
                                             random_id=random.randint(0, 2 ** 64))
                    elif mode == 'battle':
                        queue = cur.execute(f"""SELECT queue FROM main
                                                   WHERE player_id = {owner}""").fetchall()[0][0].split()
                        queue = [i.split('-') for i in queue]
                        weapon = cur.execute(f"""SELECT equiped_weapon FROM main
                                                    WHERE player_id = {owner}""").fetchall()[0][0]
                        if weapon == '':
                            weapon = 'fist'
                        dmg = weapons[weapon]['dmg'][random.randint(0, len(weapons[weapon]['dmg']) - 1)]
                        try:
                            effect = weapons[weapon]['effect'][random.randint(0, len(weapons[weapon]['effect']) - 1)]
                        except Exception:
                            effect = ''
                        if effect == 'heal' :
                            HP, LVL = cur.execute(f"""SELECT health, level FROM main
                                                            WHERE player_id = {owner}""").fetchall()[0][0]
                            cur.execute(f"""UPDATE main
                                            SET health = ?
                                            WHERE player_id = ?""",
                                        (HP + random.randint(1, LVL + 1), owner))
                            con.commit()
                        elif effect == 'posion':
                            LVL = cur.execute(f"""SELECT level FROM main WHERE player_id = {owner}""").fetchall()[0][0]
                            vk.messages.send(user_id=event.obj.message['from_id'],
                                             message=f"Эффект posion задействован",
                                             random_id=random.randint(0, 2 ** 64))
                            dmg += random.randint(0, 1) * LVL * 2
                        elif effect == 'fire':
                            LVL = cur.execute(f"""SELECT level FROM main WHERE player_id = {owner}""").fetchall()[0][0]
                            vk.messages.send(user_id=event.obj.message['from_id'],
                                             message=f"Эффект fire задействован",
                                             random_id=random.randint(0, 2 ** 64))
                            dmg += random.randint(1, LVL)
                        elif effect == 'stun':
                            LVL = cur.execute(f"""SELECT level FROM main WHERE player_id = {owner}""").fetchall()[0][0]
                            chance = random.randint(0, 100)
                            if chance >= 99 - LVL:
                                vk.messages.send(user_id=event.obj.message['from_id'],
                                                 message=f"При помощи эффекта stun Вы вывели из строя {queue[0][0]}",
                                                 random_id=random.randint(0, 2 ** 64))
                                del queue[0]
                        if queue:
                            if int(queue[0][1]) <= dmg:
                                for i in mobs[queue[0][0]]['drop'].keys():
                                    chance = random.randint(0, 100)
                                    if chance > int(i):
                                        command = f"""UPDATE main
                                                    SET {mobs[queue[0][0]]['drop'][i]} = {mobs[queue[0][0]]['drop'][i]} + 1
                                                    WHERE player_id = {owner}"""
                                        cur.execute(command)
                                        con.commit()
                                vk.messages.send(user_id=event.obj.message['from_id'],
                                                 message=f"{queue[0][0]} убит",
                                                 random_id=random.randint(0, 2 ** 64))
                                info = list(cur.execute(f"""SELECT level, experience, exp_points FROM main
                                                            WHERE player_id = {owner}""").fetchall()[0])
                                plus = mobs[queue[0][0]]['health']
                                info[1] += plus
                                while info[1] >= info[0] * 5:
                                    info[2] += random.randint(1, 3)
                                    info[1] -= info[0] * 5
                                    info[0] += 1
                                command = f"""UPDATE main
                                            SET level = {info[0]}
                                            WHERE player_id = {owner}"""
                                cur.execute(command)
                                con.commit()
                                command = f"""UPDATE main
                                            SET experience = {info[1]}
                                            WHERE player_id = {owner}"""
                                cur.execute(command)
                                con.commit()
                                command = f"""UPDATE main
                                            SET exp_points = {info[2]}
                                            WHERE player_id = {owner}"""
                                cur.execute(command)
                                con.commit()
                                del queue[0]
                            else:
                                vk.messages.send(user_id=event.obj.message['from_id'],
                                                 message=f"Нанесено {dmg} урона",
                                                 random_id=random.randint(0, 2 ** 64))
                                queue[0][1] = str(int(queue[0][1]) - dmg)
                                queue = ' '.join(['-'.join(i) for i in queue])
                        try:
                            cur.execute("""UPDATE main SET queue = ? WHERE player_id = ?""", (queue, owner))
                            con.commit()
                            queue = cur.execute(f"""SELECT queue FROM main
                                                           WHERE player_id = {owner}""").fetchall()[0][0].split()
                            queue = [i.split('-') for i in queue]
                            if queue and mode == 'battle':
                                dmg = 0
                                armor = 0
                                for i in queue:
                                    number = random.randint(0, len(mobs[i[0]]['attack']) - 1)
                                    dmg += mobs[i[0]]['attack'][number]['dmg'] * armor
                                    vk.messages.send(user_id=event.obj.message['from_id'],
                                                     message=f"Вас атоковал {i[0]} атакой {mobs[i[0]]['attack'][number]['name']}."
                                                             f" Вы получили {mobs[i[0]]['attack'][number]['dmg'] * armor} урона.",
                                                     random_id=random.randint(0, 2 ** 64))
                                    if mobs[i[0]]['attack'][number]['effect'] == "posion":
                                        posion = random.randint(0, 1) * 5 * armor
                                        dmg += posion
                                        vk.messages.send(user_id=event.obj.message['from_id'],
                                                         message=f"Вы получили {posion * armor} урона из-за эффекта posion",
                                                         random_id=random.randint(0, 2 ** 64))
                                    elif mobs[i[0]]['attack'][number]['effect'] == "stun":
                                        stun = random.randint(0, 1) * 30 * armor
                                        dmg += stun
                                        vk.messages.send(user_id=event.obj.message['from_id'],
                                                         message=f"Вы получили {stun * armor} урона из-за эффекта stun",
                                                         random_id=random.randint(0, 2 ** 64))
                                    elif mobs[i[0]]['attack'][number]['effect'] == "run":
                                        will = bool(random.randint(0, 1))
                                        if will and i == queue[0]:
                                            vk.messages.send(user_id=event.obj.message['from_id'],
                                                             message=f"{queue[0][0]} сбежал",
                                                             random_id=random.randint(0, 2 ** 64))
                                            del queue[0]
                                    elif mobs[i[0]]['attack'][number]['effect'] == "fire":
                                        fire = random.randint(1, 4) * armor
                                        dmg += fire
                                        vk.messages.send(user_id=event.obj.message['from_id'],
                                                         message=f"Вы получили {fire * armor} урона из-за эффекта fire",
                                                         random_id=random.randint(0, 2 ** 64))
                                cur.execute(f"""UPDATE main
                                                SET health = health - ?
                                                WHERE player_id = ?""",
                                            (dmg, owner))
                                con.commit()
                                health = cur.execute(f"""SELECT health FROM main
                                                                            WHERE player_id = {owner}""").fetchall()[0][0]
                                vk.messages.send(user_id=event.obj.message['from_id'],
                                                 message=f"У Вас осталось {health}",
                                                 random_id=random.randint(0, 2 ** 64))
                        except Exception:
                            cur.execute(f"""UPDATE main
                                            SET mode = ?
                                            WHERE player_id = ?""",
                                        ('idle', owner))
                            vk.messages.send(user_id=event.obj.message['from_id'],
                                             message=f"Битва закончена !",
                                             random_id=random.randint(0, 2 ** 64))
            else:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Я вас не понимаю.....",
                                 random_id=random.randint(0, 2 ** 64))
    con.close()


if __name__ == '__main__':
    main()
