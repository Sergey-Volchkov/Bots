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
from connection_to_database import connect
from copy import deepcopy
global vk_session
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

token = data.data('group')
vk_session = vk_api.VkApi(token=token)
global vk
global id_groups
vk = vk_session.get_api()

global start


def send(contentname, item, vk_ses, keyboard):
    attachment = get_picture.get_photos(vk_ses, contentname, vk)
    write_msg(item, 'Держи!', attachment,keyboard)

def write_msg(user_id, s, attachment, keyboard):
    vk_session.method('messages.send', {'user_id': user_id, 'message': s, 'attachment': attachment, 'random_id': random.randint(-2147483648,+2147483648), 'keyboard':keyboard.get_keyboard()})

def command_for_user(user_id):
    con = connect()
    with con.cursor() as cursor:
        cursor.execute(
            """select word from testword""".format(user_id))

    testword = list(map(list, cursor.fetchall()))
    print(testword)
    result = deepcopy(testword)
    for i in range(len(testword)):
        with con.cursor() as cursor:
            cursor.execute(
                """select word from keyword where testord = (select id from testword where word = '{0}')""".format(
                    testword[i][0]))
            result[i].append([item for sublist in list(map(list, cursor.fetchall())) for item in sublist])
    print(result)
    vk_session.method('messages.send', {'user_id': user_id,
                                        'message': "Команды для бота: \n\n"
                                                   "{0}.\n \n"
                                                   "{1}.\n \n"
                                                   "{2}.\n \n"
                                                   "Для того, чтобы узнать на что вы подписаны, напишите 'На что я подписан?\n\n"
                                                   "C 22:00 до 8:00 по московскому времени рассылка не производится, чтобы не будить вас ночью.\n\n".format(
                                            ('.\n \n').join(list(map(lambda buf: "Для получения " + str(
                                                buf[0]) + ", напишите что-то из: " + str(', '.join(buf[1])) + "",
                                                                     result))),
                                            "Если хотите подписаться на рассылку чего-либо из этого, напишите 'Я хочу подписаться на  --', где вместо -- подставте что-то из: " + str(
                                                (', ').join([item for sublist in testword for item in sublist])),
                                            "Если хотите отписаться , напишите 'Я хочу отписаться от  --', где вместо -- подставте что-то из: " + str(
                                                (', ').join([item for sublist in testword for item in sublist]))), 'random_id': random.randint(-2147483648,+2147483648)})

def all_keyboards(type):
    keyboard = VkKeyboard(one_time=False)
    if type =='start':
        keyboard.add_button('Команды', color=VkKeyboardColor.DEFAULT)
        keyboard.add_button('Подписка', color=VkKeyboardColor.DEFAULT)
        # keyboard.add_button('Лольки', color=VkKeyboardColor.DEFAULT)
        # keyboard.add_button('Лисы', color=VkKeyboardColor.DEFAULT)
        # keyboard.add_line()
        # keyboard.add_button('Совы', color=VkKeyboardColor.DEFAULT)
        # keyboard.add_line()
        # keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)
    elif type == 'picture':
        keyboard.add_button('Котики', color=VkKeyboardColor.DEFAULT)
        keyboard.add_button('Пёсели', color=VkKeyboardColor.DEFAULT)
        keyboard.add_button('Лольки', color=VkKeyboardColor.DEFAULT)
        keyboard.add_button('Лисы', color=VkKeyboardColor.DEFAULT)
        keyboard.add_line()
        keyboard.add_button('Совы', color=VkKeyboardColor.DEFAULT)
        keyboard.add_line()
        keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)
    # elif type == 'gif':
    # elif type == 'video':
    # elif type == 'follow':
    #     pass
    else:
        keyboard.add_button()
    return keyboard
def check_message(keyword, item, vk_ses, fw):
    try:
        con = connect()
        with con.cursor() as cursor:
            cursor.execute(
                """select contentname from contenttype where id = (select contentname from keyword where word = '{0}')""".format(
                    keyword))
        contentname = cursor.fetchall()
        con.close()
        if len(contentname)>0:
            keyboard = all_keyboards('picture')
            send(contentname[0][0], item, vk_ses,keyboard)
        else:
            try:
                vk_session.method('messages.send',
                                  {'user_id': item, 'message': fw.main_f(keyword, item), 'random_id': random.randint(-2147483648,+2147483648)})
            except:
                pass
    except:
        print('Что то пошло не так')
        pass


def send_picture():
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
                    if event.from_user and not (event.from_me):
                        print(event.user_id)
                        if response == 'команды':
                            print('ключевое слово')
                            command_for_user(event.user_id)
                        elif response == 'привет':
                            vk_session.method('messages.send', {'user_id': event.user_id,
                                                                'message': 'Привет! Напиши "команды" чтобы узнать, что может бот С:',
                                                                'random_id': random.randint(-2147483648,+2147483648)})
                        elif response == 'на что я подписан?' or response == 'на что я подписан':
                            vk_session.method('messages.send', {'user_id': event.user_id,
                                                                'message': fw.list_of_subscribers(event.user_id),
                                                                'random_id': random.randint(-2147483648,+2147483648)})
                        check_message(response, event.user_id, vk_ses, fw)
                    else:
                        pass
                    # time.sleep(2)
        except Exception:
            print(Exception)
            pass


def dispatch_module(vk_session,  vk):

        try:
            # key я так понял это dog, cat  и тд
            con = connect()
            with con.cursor() as cursor:
                cursor.execute("""select contentName from contenttype""")
                keys = cursor.fetchall()

            for key in keys:
                attachment = get_picture.get_photos(vk_session, key[0], vk)
                with con.cursor() as cursor:
                    cursor.execute("""select iduser from subscriber where contentname = (select id from contenttype where contentName ='{0}')""".format(key[0]))
                    ids = [item for sublist in list(map(list, cursor.fetchall())) for item in sublist]
                    print(ids)
                for id in ids:
                    try:
                        print('Отправляем ' + str(ids) + str(key[0]))
                        write_msg(id, ' ', attachment, 'user_id')
                        time.sleep(5)
                    except Exception as er:
                        print(str(key[0]) + ' не удалось отправить пользователю ' + str(id) + ' из-за ' + str(er))
        except Exception as er:
            print(er)


def dispatch():
    while True:

        print(int(datetime.strftime(datetime.now(), "%H")))
        if 22 > int(datetime.strftime(datetime.now(), "%H")) >= 8:
            dispatch_module(vk_session, vk)
        print('В сон на 60 минут')
        time.sleep(10800)



def main():
    # updater.update_data(all)
    p1 = Process(target=send_picture)
    p2 = Process(target=dispatch)
    p1.start()
    p2.start()


if __name__ == '__main__':
    # updater.update_data('picture')
    main()
