import sys
sys.path.insert(0, '../')
import data
import vk_api
import time

def update_data(groups):
    login, password = data.data('user')
    vk_session = vk_api.VkApi(login, password)
    vk_session.auth()
    vk = vk_session.get_api()
    # while True:
    f = open('bd.txt', 'w')
    b = {}
    for key in groups:
        max_num = vk.photos.get(owner_id=groups[key][0], album_id='wall', count=0)['count']
        b[key] = []
        for i in range(1, max_num, 1000):
            pictures = vk.photos.get(owner_id=str(groups[key][0]), album_id='wall', count=1000, offset=i)['items']
            for element in pictures:
                b[key].append('photo' + str(groups[key][0]) + '_' + str(element['id']))

    for key in b:
        print(key)
        print(b[key])
    f.write(str(b))
    f.close()
    print('READY')