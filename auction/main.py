"""
Задача данного бота является ответ
пользователям о перебивке их ставок
на аукционе проходящем в вашей группе в ВК

"""
import sys

sys.path.insert(0, '../')

from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import vk_api, random, time,os
from multiprocessing import Process
import datetime
from datetime import  timedelta, tzinfo

vk_user_session = vk_api.VkApi(login=login, password=password, app_id=2685278)
vk_user_session.auth()
user_session_api = vk_user_session.get_api()
vk_session = vk_api.VkApi(token=token)
session_api = vk_session.get_api()

longpoll = VkBotLongPoll(vk_session, group_id)

last_event=0
def checking():
    posts = {}
    f = open('file.txt', 'w')
    f.write(str(posts))
    f.close()
    for event in longpoll.listen():
        print(event)
        if event.type == VkBotEventType.WALL_POST_NEW:
            f = open('file.txt', 'r')
            posts = eval(f.read())
            f.close()
            post_id = event.obj.id

            #ДЛЯ НАСТОЯЩЕГО КОДА
            end_date = datetime.datetime.fromtimestamp(event.obj.date).replace(hour=22,minute=00,second=00) + timedelta(days=2)
            #ДЛЯ ТЕСТА
            # end_date = datetime.datetime.fromtimestamp(event.obj.date) + timedelta(minutes=1)
            try:
                for element in event.obj.attachments:
                    buf =element['photo']['id']
                    posts[buf] = {'date': end_date}
            except Exception as e:
                print(e)

            print('Создали пост ', posts)
        if event.type == VkBotEventType.PHOTO_COMMENT_NEW:
            try:

                if event.obj.post_owner_id != '-' + str(group_id):
                    now = datetime.datetime.fromtimestamp(event.obj.date)
                    if event.obj.text.lower() == 'старт':
                        cost = 20
                    else:
                        cost = int(event.obj.text)

                    if not 'last_cost' in posts[event.obj.photo_id] or cost >= posts[event.obj.photo_id]['last_cost'] + 20:
                        if cost >= 20 :
                            antisniper = 0

                            if posts[event.obj.photo_id]['date'].day == now.day and\
                                posts[event.obj.photo_id]['date'].hour-1 <= now.hour and\
                                posts[event.obj.photo_id]['date'].minute-10 <= now.minute:
                                posts[event.obj.photo_id]['date'] = now + timedelta(minutes=10)
                                #print('ВРЕМЯ ИЗМЕНЕНО! Новое время окончания аукциона:', posts[event.obj.photo_id]['date'])
                                antisniper = datetime.datetime.fromtimestamp(event.obj.date)
                            if 'last_cost' in posts[event.obj.photo_id]:
                                if antisniper ==0:
                                    message = "Ваша ставка перебита!"
                                else:message ="Ваша ставка перебита! Антиснайпер до {}".format(datetime.datetime.fromtimestamp(event.obj.date))

                                user_session_api.photos.createComment(owner_id = '-'+ str(group_id),
                                                               photo_id = event.obj.photo_id,
                                                               reply_to_comment=posts[event.obj.photo_id]['last_comment_id'],
                                                               message= message,
                                                                      from_group=1)

                            posts[event.obj.photo_id]['last_cost']= cost
                            posts[event.obj.photo_id]['last_commentator'] = event.obj.from_id
                            posts[event.obj.photo_id]['last_comment_id'] = event.obj.id
                            time.sleep(5)

                            user_session_api.photos.createComment(owner_id='-' + str(group_id),
                                                           photo_id=event.obj.photo_id,
                                                           message='{} принято'.format(cost),
                                                                  from_group=1)
                            f = open('file.txt', 'w')
                            f.write(str(posts))
                            f.close()
            except Exception as e:
                print(e)
                print('Это не число или ошибка')
                pass
def winner():
    while True:
        print('Запущена проверка победителей в ', datetime.datetime.now())
        try:
            f = open('file.txt', 'r')
            posts = eval(f.read())
            f.close()
            print(posts)

            if len(posts)!=0:
                for key, value in posts.copy().items():
                    #print(value['date'] < datetime.datetime.now())
                    print(value['date'] < datetime.datetime.now())
                    if value['date'] < datetime.datetime.now()and 'last_comment_id' in value:
                        print(value)
                        print(value['last_comment_id'])
                        user_session_api.photos.createComment(owner_id='-' + str(group_id),
                                                       photo_id=key,
                                                       reply_to_comment=value['last_comment_id'],
                                                       message="Поздравляю! Вы победили🍷🍸🎉 Свяжитесь с владельцем лота!!",
                                                              from_group=1)
                        f = open('file.txt', 'w')
                        buf = posts
                        buf.pop(key)
                        f.write(str(buf))
                        f.close()
        except Exception as e:
            print(e)
        finally:
            time.sleep(30)


def main():


    p1 = Process(target=checking)
    p2 = Process(target=winner)
    p1.start()
    p2.start()


if __name__ == '__main__':
    main()