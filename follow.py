class subscription():
    def parser(self,string,type_fw,user_id):
        if type_fw == 0:
            string = string.split('я хочу подписаться на ')[1]
            return self.follow(string,user_id)
        else:
            string = string.split('я хочу отписаться от ')[1]
            return self.unfollow(string, user_id)

    def check(self,string,user_id):
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
            f = open('../subscribers.txt', 'r')
            try:
                d = eval(f.read())
            except:
                print('не получилось прочитать файл, словарь делаем пустым')
                d = {'пёсели':[],'котики':[],'лольки':[],}
            if string == 'пёселей' or string == 'песелей':
                d['пёсели'].index(user_id)
                return 'Вы уже подписаны'
            elif string == 'котиков' or string == 'котеек':
                d['котики'].index(user_id)
                return 'Вы уже подписаны'
            elif string == 'лолей' or string == 'лолек':
                d['лольки'].index(user_id)
                return 'Вы уже подписаны'
            else:
                return "Запросили подписаться на что-то несуществующее, попробуйте ещё раз"

        except :
            if string == 'пёселей' or string == 'песелей':
                d['пёсели'].append(user_id)
            elif string == 'котиков' or string == 'котеек':
                d['котики'].append(user_id)
            elif string == 'лолей' or string == 'лолек':
                d['лольки'].append(user_id)
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
        return str(name.capitalize()) + ' больше вас не побеспокоят'
    def unfollow(self,string,user_id):
        try:
            f = open('../subscribers.txt', 'r')
            d = eval(f.read())
            f.close()
            if string == 'пёселей' or string == 'песелей':
                return(self.del_from_file(d,user_id,'пёсели'))
            elif string == 'котиков' or string == 'котеек':
                return (self.del_from_file(d,user_id,'котики'))
            elif string == 'лолей' or string == 'лолек':
                return (self.del_from_file(d,user_id,'лольки'))
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
                d['пёсели'].index(user_id)
                buf +=' пёселей'
            except:
                pass
            try:
                d['котики'].index(user_id)
                buf +=' котиков'
            except:
                pass
            try:
                d['лольки'].index(user_id)
                buf += ' лолек'
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