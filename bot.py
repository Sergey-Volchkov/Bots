import sys

sys.path.insert(0, '../')

import time
import vk_api
import random
from datetime import datetime
from multiprocessing import Process
import itisclass
import data
import follow

login, password = data.data()
global vk_session
vk_session = vk_api.VkApi(login, password)
vk_session.auth()
global vk
global id_groups

vk = vk_session.get_api()
del login, password


def choice_group_and_send(mas, response, item, vk_ses, id_group, id):
    mas.index(response)
#     print('До получения пикч ' + str(datetime.strftime(datetime.now(), "%H:%M:%S")))
    attachment = itisclass.get_photos(vk_ses, id_group, vk)
    if item.get('chat_id') == None:
#         print('До отправки сообщения ' + str(datetime.strftime(datetime.now(), "%H:%M:%S")))
        write_msg(item[id], 'Держи!', attachment, id)
#         print('После отправки сообщения ' + str(datetime.strftime(datetime.now(), "%H:%M:%S")))
        if id_group == -121355400 and item[id] != 111312042:
            write_msg(111312042, 'Кто-то попросил у меня пёселей, но я и тебе пришлю!', attachment, id)
    else:
        write_msg(item[id], 'Держите!', attachment, id)


def write_msg(user_id, s, attachment, id):
    vk_session.method('messages.send', {id: user_id, 'message': s, 'attachment': attachment})


def commands(item):
    vk_session.method('messages.send', {'user_id': item['user_id'],
                                        'message': "Команды для бота: \n\n Для получения лолей напишите что-то из 'лоли', 'лольки', 'loli', 'лолька', 'лоля', 'лоликон'.\n \n"
                                                   " Для получения котиков напишите что-то из 'котик', 'кошка', 'кот', 'котенок', 'котяра', 'cat', 'котика', 'котики', 'коты', 'cats', 'пушистый педрила','киса','котейка','котейки','кисы', 'пушистые педрилы', 'пушистые пидрилы', 'пушистая педрила', 'пушастый пидрила', 'шаверма', 'шаурма', 'котя'.\n \n"
                                                   "Для получения пёселей напишите что-то из 'пёсель', 'собака', 'пёс', 'doge', 'песель', 'псина', 'пёсели', 'песели', 'псины', 'пёсики', 'песики', 'хлеп', 'хлеб', 'булочка', 'булочки', 'собакен', 'собакены', 'dog', 'dogs'.\n \n"
                                                   "Для получения лис напишите что-то из 'лиса', 'лисы', 'лисичка', 'лисички','foxes' ,'фокс', 'фоксы', 'fox'.\n \n"
                                                   "Для получения сов напишите что-то из 'совы', 'совушки', 'сов', 'owl', 'owls', 'сова'.\n \n"
                                                   "Если хотите подписаться на рассылку чего-либо из этого, напишите 'Я хочу подписаться на --', где вместо -- напишите 'пёселей', 'котиков', 'лис', 'сов' или 'лолей'.\n \n"
                                                   "Если хотите отписаться от рассылки чего-либо из подписанного, напишите 'Я хочу отписаться от --', где вместо -- напишите 'песелей', 'котиков', 'лис', 'сов' или 'лолей'.\n \n"
                                                   "При подписке вы так же будете получать информацию об обновлениях бота.\n\n"
                                                   "Для того, чтобы узнать на что вы подписаны, напишите 'На что я подписан?'\n\n"
                                                   "C 22:00 до 8:00 рассылка не производится, чтобы не будить вас ночью.'\n\n"
                                                   "Если нашли какие-то баги, нерабочую команду или что-то ещё, то сразу пишите мне."})


def check_message(all_commands, response, item, vk_ses, id, fw):
    for key in all_commands:
        try:
            choice_group_and_send(all_commands[key][1], response, item, vk_ses, all_commands[key][0], id)

            break
        except:
            pass
    if id == 'user_id':
        try:
            vk_session.method('messages.send', {'user_id': item['user_id'],
                                                'message': fw.main_f(response, item['user_id'], all_commands)})
        except:
            pass


def send_picture(values, all_commands):
    vk_ses = vk_session
    fw = follow.subscription()
    while True:
        try:
            response = vk_session.method('messages.get', values)
            if response['items']:
                print('Сообщение пришло в ' + str(datetime.strftime(datetime.now(), "%H:%M:%S")))
                response['items'].reverse()
            for item in response['items']:
                response = item['body'].lower()
                if item.get('chat_id') == None:
                    print(item['user_id'])
                    if response == 'команды':
                        commands(item)
                    elif response == 'на что я подписан?' or response == 'на что я подписан':
                        vk_session.method('messages.send', {'user_id': item['user_id'],
                                                            'message': fw.list_of_subscribers(item['user_id'],
                                                                                              all_commands)})
                    check_message(all_commands, response, item, vk_ses, 'user_id', fw)
                else:
                    print(item['chat_id'])
                    check_message(all_commands, response, item, vk_ses, 'chat_id', fw)
                values['last_message_id'] = item['id']

            time.sleep(1)
        except:
            pass


def dispatch_module(vk_session, id_groups, vk, d):
    for key in id_groups:
        try:
            attachment = itisclass.get_photos(vk_session, id_groups[key][0], vk)
            for element in d[key]:
                try:
                    print('Отправляем ' + str(key) + str(element))
                    write_msg(element, ' ', attachment, 'user_id')
                    time.sleep(5)
                except Exception as er:
                    print(str(key) + ' не удалось отправить пользователю ' + str(element) + 'из-за ' + str(er))
        except Exception as er:
            print(er)


def dispatch(id_groups):
    # try:
    while True:
        time.sleep(10800)
        f = open('../subscribers.txt', 'r')
        d = eval(f.read())
        f.close()
        print(int(datetime.strftime(datetime.now(), "%H")))
        if 22 > int(datetime.strftime(datetime.now(), "%H")) + 3 >= 8:
            dispatch_module(vk_session, id_groups, vk, d)
        print('В сон на 60 минут')

    # except FileNotFoundError:
    #     print('Файла нет')
    #     d = {'пёсели': [], 'котики': [], 'лольки': [], }
    #     f = open('../subscribers.txt', 'w')
    #     f.write(str(d))
    #     f.close()
    #     dispatch()


def main():
    values = {'out': 0, 'count': 20, 'time_offset': 120}
    all_commands = {'cat': [-130670107,
                            ['котик', 'кошка', 'кот', 'котенок', 'котяра', 'cat', 'котика', 'котики', 'коты', 'cats',
                             'пушистый педрила', 'киса', 'котейка', 'котейки', 'кисы', 'пушистые педрилы',
                             'пушистые пидрилы', 'пушистая педрила', 'пушастый пидрила', 'шаверма', 'шаурма', 'котя'],
                            'котиков'],
                    'dog': [-121355400,
                            ['пёсель', 'собака', 'пёс', 'doge', 'песель', 'псина', 'пёсели', 'песели', 'псины',
                             'пёсики', 'песики', 'хлеп', 'хлеб', 'булочка', 'булочки', 'собакен', 'собакены', 'dog',
                             'dogs'], 'песелей'],
                    'loli': [-101072212, ['лоли', 'лольки', 'loli', 'лолька', 'лоля', 'лоликон'], 'лолей'],
                    'fox': [-123223613, ['лиса', 'лисы', 'лисичка', 'лисички', 'fox', 'фокс', 'фоксы', 'foxes'], 'лис'],
                    'owl': [-113854206, ['совы', 'совушки', 'сов', 'owl', 'owls','сова'], 'сов']}

    p1 = Process(target=send_picture, args=(values, all_commands,))
    p2 = Process(target=dispatch, args=(all_commands,))
    p1.start()
    p2.start()


if __name__ == '__main__':
    main()
