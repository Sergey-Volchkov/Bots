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
login,password = data.data()
global vk_session
vk_session = vk_api.VkApi(login, password)
vk_session.auth()
global vk
global id_group_cat
global id_group_dog
global id_group_loli
id_group_cat = -130670107
id_group_dog = -121355400
id_group_loli = -127518015
vk = vk_session.get_api()
del login, password



def choice_group_and_send(mas,response,item,vk_ses,id_group):
    mas.index(response)
    attachment = itisclass.get_photos(vk_ses, id_group, vk)
    write_msg(item['user_id'], 'Держи!', attachment)
    if id_group == -121355400 and item['user_id'] != 111312042:
        write_msg(111312042, 'Кто-то попросил у меня пёселей, но я и тебе пришлю!', attachment)

def write_msg(user_id, s, attachment):
    vk_session.method('messages.send', {'user_id': user_id, 'message': s, 'attachment': attachment})

def send_picture(values):
    vk_ses = vk_session
    loli = ['лоли','лольки','loli','лолька','лоля','лоликон']
    cat = ['котик', 'кошка', 'кот', 'котенок', 'котяра', 'cat','котика','котики','коты','cats','пушистый педрила','пушистые педрилы','пушистые пидрилы','пушистая педрила','пушастый пидрила','шаверма','шаурма']
    dog = ['пёсель','собака','пёс','doge','песель','псина','пёсели','песели','псины','пёсики','песики','хлеп','хлеб','булочка','булочки']

    fw = follow.subscription()
    while True:
        try:
            response = vk_session.method('messages.get', values)
            if response['items']:
                print('Сообщение пришло в ' + str(datetime.strftime(datetime.now(), "%H:%M:%S")))
                values['last_message_id'] = response['items'][0]['id']
            for item in response['items']:
                response = response['items'][0]['body'].lower()
                if response == 'команды':
                    vk_session.method('messages.send', {'user_id': item['user_id'], 'message': "Команды для бота: \n Для получения лолей напишите что-то из 'лоли', 'лольки', 'loli', 'лолька', 'лоля', 'лоликон'. \n \n"
                                                                                               "Для получения котиков напишите что-то из 'котик', 'кошка', 'кот', 'котенок', 'котяра', 'cat', 'котика', 'котики', 'коты', 'cats', 'пушистый педрила', 'пушистые педрилы', 'пушастая педрила', 'шаверма', 'шаурма'.\n \n"
                                                                                               "Для получения пёселей напишите что то из 'пёсель', 'собака', 'пёс', 'doge', 'песель', 'псина', 'пёсели', 'песели', 'псины', 'пёсики', 'песики', 'хлеп', 'хлеб', 'булочка', 'булочки'\n \n"
                                                                                               "Если хотите подписаться на рассылку чего-либо из этого, напишите 'Я хочу подписаться на --', где вместо -- напишите 'пёселей', 'котиков' или 'лолей'\n \n"
                                                                                               "Если хотите отписаться от рассылки чего-либо из подписанного, напишите 'Я хочу отписаться от --', где вместо -- напишите 'пёселей', 'котиков' или 'лолей'\n \n"
                                                                                               "Для того, чтобы узнать на что вы подписаны, напишите 'На что я подписан?'\n\n"
                                                                                               "C 22:00 до 8:00 рассылка не производится, чтобы не будить вас ночью'\n\n" 
                                                                                               "Если нашли какие-то баги, нерабочую команду или что-то ещё, то сразу пишите мне"})
                elif response == 'на что я подписан?' or response == 'на что я подписан':
                    vk_session.method('messages.send', {'user_id': item['user_id'], 'message':fw.list_of_subscribers(item['user_id'])})


                try:
                    choice_group_and_send(cat, response, item, vk_ses, id_group_cat)
                except:
                    try:
                        choice_group_and_send(dog, response, item, vk_ses, id_group_dog)
                    except:

                        try:
                            choice_group_and_send(loli,response, item,vk_ses, id_group_loli)
                        except:pass
                finally:
                    try:
                        vk_session.method('messages.send', {'user_id': item['user_id'],
                                                            'message': fw.main_f(response, item['user_id'])})
                    except:
                        pass
            time.sleep(1)
        except:
            pass

def dispatch():
#     try:
    
    while True:
        f = open('../subscribers.txt', 'r')
        d = eval(f.read())
        f.close()
        print(int(datetime.strftime(datetime.now(), "%H")))
        if 22 > int(datetime.strftime(datetime.now(), "%H"))+3 => 8:
            try:
                attachment = itisclass.get_photos(vk_session, id_group_dog, vk)
                for element in d['пёсели']:
                    print('Отправляем пёселей' + str(element))
                    write_msg(element, ' ', attachment)
            except:pass
            time.sleep(2)
            try:
                attachment = itisclass.get_photos(vk_session, id_group_cat, vk)
                for element in d['котики']:
                    print('Отправляем котиков' + str(element))
                    write_msg(element, ' ', attachment)
            except:pass
            time.sleep(2)
            try:
                attachment = itisclass.get_photos(vk_session, id_group_loli, vk)
                for element in d['лольки']:

                    print('Отправляем лолей' + str(element))
                    write_msg(element, ' ', attachment)
            except:pass
        print('В сон на 60 минут')
        time.sleep(3600)
#     except:
#         print('Файла нет')
#         # d = {'пёсели': [], 'котики': [], 'лольки': [], }
#         # f = open('../subscribers.txt', 'w')
#         # f.write(str(d))
#         # f.close()
#         dispatch()



def main():

    values = {'out': 0, 'count': 20, 'time_offset': 120}

    p1 = Process(target=send_picture, args=(values,))
    p2 = Process(target=dispatch)
    p1.start()
    p2.start()
if __name__ == '__main__':
    main()
