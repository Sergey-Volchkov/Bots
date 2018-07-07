import random
import time


def get_photos(vk_session, request, vk):
    try:
        print(request)
        f = open('bd.txt', 'r')
        b = eval(f.read())
        f.close()
        attachment = ''
        max_num = len(b[request])
        print(max_num)
        num = random.randint(1, max_num - 5)
        pictures = b[request][num:num + 5]
        buf = []
        print(pictures)
        for element in pictures:
            buf.append(element)
        attachment = ','.join(buf)
        return attachment
    except:
        return get_photos(vk_session, request, vk)

