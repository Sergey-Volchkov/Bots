"""
Данный бот имеет возможность
скачивать голосовые сообщения
и отправлять их отправителю
"""
import sys

sys.path.insert(0, '../')

from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import vk_api, random, time, requests,os, json
from datetime import datetime
from urllib.request import urlretrieve
token, group_id = 'токен', "айди группы"
vk_session = vk_api.VkApi(token=token)
session_api = vk_session.get_api()

longpoll = VkBotLongPoll(vk_session, group_id)


def send_message(peer_id, message=None, attachment=None, keyboard=None, payload=None):
    session_api.messages.send(peer_id=peer_id, message=message, random_id=random.randint(-2147483648, +2147483648),
                              attachment=attachment, keyboard=keyboard, payload=payload)


def send_audio_message(event):
    send_audio_message(event)
    url = session_api.docs.getMessagesUploadServer(type='audio_message', peer_id=event.obj.peer_id)['upload_url']
    audio = event.obj.attachments[0]['audio_message']['link_ogg']
    urlretrieve(audio, "downloads/" + audio.split('/')[-1])
    f = open("downloads/" + audio.split('/')[-1], 'rb')
    up = {'file': (audio.split('/')[-1], f, "multipart/form-data")}
    response = requests.post(url, files=up)
    f.close()
    os.remove("downloads/" + audio.split('/')[-1])
    audio = session_api.docs.save(file=response.json()['file'])
    buf = 'doc' + str(audio['audio_message']['owner_id']) + '_' + str(audio['audio_message']['id']) + '_' + str(
        audio['audio_message']['access_key'])
    return buf


while True:
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            buf = send_audio_message(event)
            send_message(peer_id=event.obj.peer_id, attachment=buf)
