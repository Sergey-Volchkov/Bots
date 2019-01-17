from connection_to_database import connect
import re


class subscription():
    def check(self, string, user_id):
        print('Проверяем наличие совпадений в строке')
        if string.find('я хочу подписаться') != -1:
            try:
                return self.parser(string, 0, user_id)
            except:
                return 'Неверно написали строку'
        elif string.find('я хочу отписаться') != -1:
            try:
                return self.parser(string, 1, user_id)
            except:
                return 'Неверно написали строку'

    def parser(self, string, type_fw, user_id):
        print('Парсим')
        if type_fw == 0:
            string = string.split('я хочу подписаться на ')[1]
            string = re.sub("ё", "е", str(string))
            print('Распарсили')
            return self.follow(string, user_id)
        else:
            string = string.split('я хочу отписаться от ')[1]
            return self.unfollow(string, user_id)



    def follow(self, string, user_id):
        # Проверяем, не записывается ли человек повторно
        con = connect()
        # Делаем запрос к бд в таблицу с подписчиками имеется ли запись по подписке
        try:
            with con.cursor() as cursor:
                print('Делаем запрос к бд на проверку наличия возможности подписки')
                cursor.execute(
                    """select contentname from contenttype where id = (select contentname from testword where word = '{0}')""".format(string))
            key = cursor.fetchall()[0][0]

            # Потом в эту команду добавить проверку по медиатипу
            with con.cursor() as cursor:
                print('Проверяем подписан ли человек уже')
                cursor.execute(
                    """select count(*) from subscriber where (idUser={0}) and (contentName=(select id from contenttype where contentname ='{1}')) and (mediaName=(select id from mediatype where medianame='picture'))""".format(
                        user_id, key))
            if cursor.fetchall()[0][0] != 0:
                con.close()
                return 'Вы уже подписаны'
            else:
                print('Проверяем если ли человек в базе данных с id')
                with con.cursor() as cursor:
                    cursor.execute("""select count(*) from idUser where id={0}""".format(user_id))
                    if cursor.fetchall()[0][0] == 0:
                        print('Этот подписчик ещё не был ни на что подписан, добавляем его')
                        cursor.execute("""INSERT INTO idUser VALUES({0})""".format(user_id))
                con.commit()
                print('Подписываем на то, что он хотел')
                # В дальнейшем модифицировать и сделать возможным подписку на гифки с видосиками
                with con.cursor() as cursor:
                    print('До запроса')
                    cursor.execute("""INSERT INTO subscriber(iduser,contentname,medianame) VALUES((select id from bot_bd.iduser where id ={0}),
                                   (select id from contenttype where contentname='{1}'),
                                   (select id from mediatype where medianame='picture'))""".format(user_id, key))
                    print('Подписка прошла успешно')

                con.commit()
                con.close()
                return 'Вы успешно подписаны на ' + string

        except:
            return 'Запросили подписаться на что-то несуществующее, попробуйте ещё раз'

    def del_from_file(self, user_id, key):
        con = connect()
        with con.cursor() as cursor:
            cursor.execute(
                """select id from subscriber where (idUser={0}) and (contentName= (select id from contenttype where contentname ='{1}'))""".format(
                    user_id, key))
        if len(cursor.fetchall())!=0:
            with con.cursor() as cursor:
                print('Убираем подписку на ' + (key))
                cursor.execute(
                    """delete from subscriber where (idUser={0}) and (contentName= (select id from contenttype where contentname ='{1}'))""".format(
                        user_id, key))
            con.commit()
            with con.cursor() as cursor:
                print('Проверяем подписан ли на что-то ещё пользователь ')
                cursor.execute(
                    """select count(*) from subscriber where idUser={0}""".format(user_id))
            if cursor.fetchall()[0][0] == 0:
                print('Если нет, удаляем его совсем везде')
                with con.cursor() as cursor:
                    cursor.execute("""delete from iduser where id={0}""".format(user_id))
                con.commit()
            con.close()
            return 'Они больше вас не побеспокоят'
        con.close()
        return 'Вы на это не подписаны'
    def unfollow(self, string, user_id):
        try:
            print(string)
            con = connect()
            with con.cursor() as cursor:
                print('Делаем запрос к бд на проверку наличия возможности отпписки')
                cursor.execute(
                    """select contentname from contenttype where id = (select contentname from testword where word = '{0}')""".format(string))
            key = cursor.fetchall()[0][0]
            return (self.del_from_file(user_id, key))

        except:
            return "Запросили отписаться от чего-то несуществующего"

    def list_of_subscribers (self, user_id):
        buf1 = ''
        try:
            con = connect()
            # переделать если будет добавлена возможность подписки на различные медиатайпы
            with con.cursor() as cursor:
                cursor.execute(
                    """select word from testword where contentname in (select contentName from subscriber where (idUser= {0}) and (medianame = (select id from mediatype where medianame ='picture')))""".format(
                        user_id))
            buf = list(map(list, cursor.fetchall()))
            if len(buf)!=0:
                buf = [item for sublist in buf for item in sublist]
                print(buf)
                buf1 = (', '.join(buf))
                con.close()
                return 'Вы подписаны  ' + buf1
            else:
                con.close()
                return 'Вы пока ни на что не подписаны'
        except: return 'Произошла ошибка при выведении списка подписок'

    def main_f(self, string, user_id):
        try:
            return self.check(string, user_id)
        except:
            pass
