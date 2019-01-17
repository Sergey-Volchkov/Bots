import random
import time
from connection_to_database import connect


def get_photos(vk_session, keyword, vk):
        con = connect()
        print(keyword)
        #keyword я так понял это dog, cat  и тд
        start = time.time()
        with con.cursor() as cursor:
            cursor.execute("""select urlContent from content where contentname=(select id from contenttype where contentname='{0}') order by rand() limit 5""".format(keyword))
            pictures = cursor.fetchall()
            print(time.time() - start)
        con.close()
        buf =[]
        for element in pictures:
            buf.append(element[0])
        attachment = ','.join(buf)
        print(attachment)
        return attachment
