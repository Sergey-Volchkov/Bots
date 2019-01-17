import sys
sys.path.insert(0, '../')
import re
import data
import vk_api
import time
from connection_to_database import connect

def update_data(mediaType):
    login, password = data.data('user')
    vk_session = vk_api.VkApi(login, password)
    vk_session.auth()
    vk = vk_session.get_api()
    start = time.time()

    if mediaType == 'picture':
        con = connect()
        with con.cursor() as cursor:
            cursor.execute("""select contentName from contenttype""")
            keys = cursor.fetchall()
        for key in keys:
            print(key[0])
            with con.cursor() as cursor:
                cursor.execute("""select url from source where contentName = (select id from contenttype where contentname = '{0}')""".format(key[0]))
                groupId = cursor.fetchall()
            for gid in groupId:
                print(gid[0])
                print(str(gid[0]))
                with con.cursor() as cursor:
                    cursor.execute("""select contentname from source where(contentname=(select id from contenttype where contentname ='{0}')) and (url = {1}) """.format(key[0],gid[0]))
                    contentName = cursor.fetchall()[0][0]
                    cursor.execute("""select medianame from source where(medianame=(select id from mediatype where medianame ='{0}')) and (url = {1}) """.format('picture',gid[0]))
                    mediaName = cursor.fetchall()[0][0]
                max_num = vk.photos.get(owner_id=gid[0], album_id='wall', count=0)['count']
                b = []
                for i in range(1, max_num, 1000):
                    pictures = vk.photos.get(owner_id=str(gid[0]), album_id='wall', count=1000, offset=i)['items']
                    for element in pictures:
                        #первое url,второе contentname, 3 medianame
                        b.append(['photo' + str(gid[0]) + '_' + str(element['id']),contentName,mediaName, gid])
                print(start - time.time())
                result = re.sub("]" ,")", str(b))
                result = re.sub(re.escape('[') ,"(", str(result))[1:len(result)-1]
                with con.cursor() as cursor:
                    try:
                        cursor.execute("""insert into content(urlContent,contentName,mediaName,groupid) values{0}""".format(result))
                    except:pass
        con.commit()
        con.close()
        print(start -time.time())
    print('READY')