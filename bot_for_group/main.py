import sys
sys.path.insert(0, '../')
import vk_api
import time
import time
import vk_api
import random
from datetime import datetime
from multiprocessing import Process
import get_picture
import data
import updater
import follow
global vk_session
from vk_api.longpoll import VkLongPoll, VkEventType

token = data.data('group')
vk_session = vk_api.VkApi(token=token)
global vk
global id_groups
vk = vk_session.get_api()

def choice_group_and_send(mas, response, item, vk_ses, key, id):
    mas.index(response)
    attachment = get_picture.get_photos(vk_ses, key, vk)
    if id == 'user_id':
        write_msg(item, 'Держи!', attachment, id)
    else:
        print(item)
        write_msg(item, 'Держите!', attachment, id)


def write_msg(user_id, s, attachment, id):
    vk_session.method('messages.send', {id: user_id, 'message': s, 'attachment': attachment})


def command_for_user(user_id,all_commands):
#     vk_session.method('messages.send', {'user_id': user_id,
#                                         'message': "Команды для бота: \n\n"
#                                                    "Для получения {0} напишите что-то из '{1}'.\n \n"
#                                                    "Если хотите подписаться на рассылку {0}, напишите 'Я хочу подписаться на {0}'.\n \n"
#                                                    "Если хотите отписаться от рассылки, напишите 'Я хочу отписаться от {0}'.\n \n"
#                                                    "Для того, чтобы узнать на что вы подписаны, напишите 'На что я подписан?\n\n"
#                                                    "C 22:00 до 8:00 рассылка не производится, чтобы не будить вас ночью.\n\n".format(all_commands[request][2][0],', '.join(all_commands[request][1]))})
    vk_session.method('messages.send', {'user_id': user_id,
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
            choice_group_and_send(all_commands[key][1], response, item, vk_ses, key, id)
            break
        except:
            pass
    try:
        vk_session.method('messages.send', {'user_id': item,
                                            'message': fw.main_f(response, item, all_commands)})
    except:
        pass


def send_picture(all_commands):
    vk_ses = vk_session
    fw = follow.subscription()
    longpoll = VkLongPoll(vk_session)
    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW:
                    print('Сообщение пришло в ' + str(datetime.strftime(datetime.now(), "%H:%M:%S")))
                    response = event.text.lower()
                    print(response)
                    if event.from_user and not(event.from_me):
                        print(event.user_id)
                        if response == 'команды':
                            command_for_user(event.user_id, all_commands)
                        elif response == 'привет':
                            vk_session.method('messages.send', {'user_id': event.user_id,
                                                                'message': 'Привет! Напиши "команды" чтобы узнать, что может бот С:'})
                        elif response == 'на что я подписан?' or response == 'на что я подписан':
                            vk_session.method('messages.send', {'user_id': event.user_id,
                                                                'message': fw.list_of_subscribers(event.user_id,
                                                                                                  all_commands)})

                        check_message(all_commands, response, event.user_id, vk_ses, 'user_id', fw)
                    else:
                        pass
                    time.sleep(2)
        except:
            pass


def dispatch_module(vk_session, id_groups, vk, d):
    for key in id_groups:
        try:
            attachment = get_picture.get_photos(vk_session, key, vk)
            for element in d[key]:
                try:
                    print('Отправляем ' + str(key) + str(element))
                    write_msg(element, ' ', attachment, 'user_id')
                    time.sleep(5)
                except Exception as er:
                    print(str(key) + ' не удалось отправить пользователю ' + str(element) + ' из-за ' + str(er))
        except Exception as er:
            print(er)


def dispatch(id_groups):
    try:
        while True:
            f = open('subscribers.txt', 'r')
            b = eval(f.read())
            f.close()
            print(int(datetime.strftime(datetime.now(), "%H")))
            if 22 > int(datetime.strftime(datetime.now(), "%H")) + 3 >= 8:
                dispatch_module(vk_session, id_groups, vk, b)
            print('В сон на 60 минут')
            time.sleep(10800)


    except FileNotFoundError:
        print('Файла нет, будет создан пустой')
        b = {}
        for key in id_groups:
            b[key] = []
        f = open('subscribers.txt', 'w')
        f.write(str(b))
        f.close()
        dispatch(id_groups)

def my_commands():
        return {'cat': [-130670107,
                            ['котик', 'кошка', 'кот', 'котенок', 'котяра', 'cat', 'котика', 'котики', 'коты', 'cats',
                              'киса', 'котейка', 'котейки', 'кисы',
                             'шаверма', 'шаурма', 'котя'],['котиков']],
                    'dog': [-121355400,
                            ['пёсель', 'собака', 'пёс', 'doge', 'песель', 'псина', 'пёсели', 'песели', 'псины',
                             'пёсики', 'песики', 'хлеп', 'хлеб', 'булочка', 'булочки', 'собакен', 'собакены', 'dog',
                             'dogs'], ['песелей','пёселей']],
                    'loli': [-101072212, ['лоли', 'лольки', 'loli', 'лолька', 'лоля', 'лоликон'], 'лолей'],
                    'fox': [-123223613, ['лиса', 'лисы', 'лисичка', 'лисички', 'fox', 'фокс', 'фоксы', 'foxes'], 'лис'],
                    'owl': [-113854206, ['совы', 'совушки', 'сов', 'owl', 'owls','сова'], ['сов']]}
        
def main():
    all_commands = my_commands()
    #updater.update_data(all)
    p1 = Process(target=send_picture, args=(all_commands,))
    p2 = Process(target=dispatch, args=(all_commands,))
    p1.start()
    p2.start()


if __name__ == '__main__':
    # updater.update_data(my_commands())
    main()
