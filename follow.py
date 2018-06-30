class subscription():
    def parser(self,string,type_fw,user_id):
        print('парсим')
        if type_fw == 0:
            string = string.split('я хочу подписаться на ')[1]
            return self.follow(string,user_id)
        else:
            string = string.split('я хочу отписаться от ')[1]
            return self.unfollow(string, user_id)

    def check(self,string,user_id):
        print('проверяем наличие совпадений в строке')
        if string.find('я хочу подписаться')!= -1:
            try:
                return self.parser(string,0, user_id)
            except:
                return 'Неверно написали строку'
        elif string.find('я хочу отписаться')!= -1:
            try:
                return self.parser(string,1,user_id)
            except:
                return 'Неверно написали строку'

    def follow(self,string,user_id):
        try:
            #Проверяем, не записывается ли человек повторно
            print('Открываем файл...')
            f = open('../subscribers.txt', 'r')
            print('Файл открыли')
            try:
                d = eval(f.read())
                print('Прочитали файл')
            except:
                print('не получилось прочитать файл, словарь делаем пустым')
            print(string)
            if string == 'пёселей' or string == 'песелей':
                d['dog'].index(user_id)
                return 'Вы уже подписаны'
            elif string == 'котиков' or string == 'котеек':
                d['cat'].index(user_id)
                return 'Вы уже подписаны'
            elif string == 'лолей' or string == 'лолек':
                d['loli'].index(user_id)
            elif string == 'лис' or string == 'лисичек':
                d['fox'].index(user_id)
                return 'Вы уже подписаны'
            else:
                return "Запросили подписаться на что-то несуществующее, попробуйте ещё раз"

        except :
            if string == 'пёселей' or string == 'песелей':
                d['dog'].append(user_id)
            elif string == 'котиков' or string == 'котеек':
                d['cat'].append(user_id)
            elif string == 'лолей' or string == 'лолек':
                d['loli'].append(user_id)
            elif string == 'лис' or string == 'лисичек':
                d['fox'].append(user_id)
            f = open('../subscribers.txt', 'w')
            f.write(str(d))
            return 'Вы успешно подписаны на ' + string
        finally:
            f.close()

    def del_from_file(self,d,user_id,name):
        d[name].remove(user_id)
        f = open('../subscribers.txt', 'w')
        f.write(str(d))
        f.close()
        return 'Они больше вас не побеспокоят'
    def unfollow(self,string,user_id):
        try:
            f = open('../subscribers.txt', 'r')
            d = eval(f.read())
            f.close()
            if string == 'пёселей' or string == 'песелей':
                return(self.del_from_file(d,user_id,'dog'))
            elif string == 'котиков' or string == 'котеек':
                return (self.del_from_file(d,user_id,'cat'))
            elif string == 'лолей' or string == 'лолек':
                return (self.del_from_file(d,user_id,'loli'))
            elif string == 'лис' or string == 'лисичек':
                return (self.del_from_file(d,user_id,'fox'))
            else: return "Запросили отписаться от чего-то несуществующего"
        except:
            return 'Не удалось отписаться'
        finally:
            f.close()

    def list_of_subscribers(self,user_id):
        buf=''
        try:
            f = open('../subscribers.txt', 'r')
            d = eval(f.read())
            try:
                d['dog'].index(user_id)
                buf +=' пёселей'
            except:
                pass
            try:
                d['cat'].index(user_id)
                buf +=' котиков'
            except:
                pass
            try:
                d['loli'].index(user_id)
                buf += ' лолек'
            except:pass
            try:
                d['fox'].index(user_id)
                buf += ' лисичек'
            except:pass
            if len(buf)>2:
                return 'Вы подписаны на' + buf
            else:
                return 'Вы ни на что не подписаны'
        except:
            return 'Произошла ошибка при выведении списка подписок'

    def main_f(self, string,user_id):
        try:
            return self.check(string,user_id)
        except:
            pass
