import time
import vk_api
import random
from datetime import datetime
from multiprocessing import Process
import itisclass
import data
login,password = data.data()
global vk_session
vk_session = vk_api.VkApi(login, password)
vk_session.auth()
global vk
vk = vk_session.get_api()
# del login, password


def interval(since,until,clock,hour,minute):
    if since <= int(clock[0]) <= until:
        print('Время после {} до {}'.format(since, until))
        choice(since, until, clock, hour, minute)
        return 0
    else: return 1
def choice_group_and_send(mas,response,item,vk_ses,id_group):
    mas.index(response)
    attachment = itisclass.get_photos(vk_ses, id_group, vk)
    write_msg(item['user_id'], 'Держи!', attachment)
    if id_group == -121355400 and item['user_id'] != 111312042:
        write_msg(111312042, 'Кто-то попросил у меня пёселей, но я и тебе пришлю!', attachment)
    if id_group == -121355400 and item['user_id'] == 100426275:
        vk_session.method('messages.send', {'user_id': 100426275, 'message': 'Всё равно ты пидр с:'})

def choice(n, m, clock,hour,minute):
    if not (n <= hour <= m):
        hour = random.randint(int(datetime.strftime(datetime.now(), "%H")), m)
        if hour == int(datetime.strftime(datetime.now(), "%H")):
            if int(datetime.strftime(datetime.now(), "%M")) < 40:
                buf = int(datetime.strftime(datetime.now(), "%M"))
            else:
                buf = 0
                hour+=1
            minute = random.randint(buf, 59)
        else:
            minute = random.randint(0, 59)
    for_kira_send_picture(clock, hour, minute)

def write_msg(user_id, s, attachment):
    vk_session.method('messages.send', {'user_id': user_id, 'message': s, 'attachment': attachment})

def send_picture(values):
    vk_ses = vk_session
    cat = ['котик', 'кошка', 'кот', 'котенок', 'котяра', 'cat','котика','пушистый педрила']
    id_group_cat = -32015300
    id_group_dog = -121355400
    dog = ['пёсель','собака','пёс','doge','песель','псина','пёсели','песели']
    while True:
        response = vk_session.method('messages.get', values)

        if response['items']:
            values['last_message_id'] = response['items'][0]['id']
        for item in response['items']:
            response = response['items'][0]['body'].lower()
            try:
                choice_group_and_send(cat, response, item, vk_ses, id_group_cat)
            except:
                try:
                    choice_group_and_send(dog, response, item, vk_ses, id_group_dog)
                except:
                    pass
        time.sleep(5)

def for_kira_decision():
    
    while True:
        clock = datetime.strftime(datetime.now(), "%H:%M:%S").split(':')
        for i in range(len(clock)):
            clock[i] = int(clock[i])
            if i == 0:
                clock[i]+=3
        print(clock)
        hour,minute = 0,0
        if interval(12, 14, clock, hour, minute) == 1 and interval(16, 18, clock, hour, minute) == 1:
            print('В сон на 20 минут')
            time.sleep(1200)

def for_kira_send_picture(clock,hour,minute):
    vk_ses = vk_session
    print(hour, minute)
    if hour == int(clock[0]):
        while True:
            print('проверяем совпадение минут')
            print((datetime.strftime(datetime.now(), "%M"), minute))
            clock_m = int(datetime.strftime(datetime.now(), "%M"))
            if minute == clock_m:
                attachment = itisclass.get_photos(vk_session, -121355400, vk)
                write_msg(111312042, 'Время пёселей!', attachment)
                time.sleep(59)
                break
            time.sleep(59)
    else:
        if int(datetime.strftime(datetime.now(), "%H")) >= 23:
            del hour
            del minute
        time.sleep(1200)


def main():

    values = {'out': 0, 'count': 1, 'time_offset': 60}

    p1 = Process(target=send_picture, args=(values,))
    p2 = Process(target=for_kira_decision)
    p1.start()
    p2.start()
if __name__ == '__main__':
    main()
