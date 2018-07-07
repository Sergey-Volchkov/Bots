class subscription():
    def parser(self, string, type_fw, user_id, all_commands):
        print('парсим')
        if type_fw == 0:
            string = string.split('я хочу подписаться на ')[1]
            return self.follow(string, user_id, all_commands)
        else:
            string = string.split('я хочу отписаться от ')[1]
            return self.unfollow(string, user_id, all_commands)

    def check(self, string, user_id, all_commands):
        print('Проверяем наличие совпадений в строке')
        if string.find('я хочу подписаться') != -1:
            try:
                return self.parser(string, 0, user_id, all_commands)
            except:
                return 'Неверно написали строку'
        elif string.find('я хочу отписаться') != -1:
            try:
                return self.parser(string, 1, user_id, all_commands)
            except:
                return 'Неверно написали строку'

    def follow(self, string, user_id, all_commands):
        try:
            # Проверяем, не записывается ли человек повторно
            print('Открываем файл...')
            f = open('subscribers.txt', 'r')
            print('Файл открыли')
            try:
                d = eval(f.read())
                print('Прочитали файл')
            except:
                print('Не получилось прочитать файл')
            print(string)
            flag = 0
            for key in all_commands:

                for element in all_commands[key][2]:
                    print('Строка: ' +str(string))
                    print(element)
                    print('ключ ' +str(key))
                    print(d[key])
                    print(user_id)
                    try:
                        if string == element:
                            print('ОН ПРОШЁЛ')
                            d[key].index(user_id)
                            flag = 1
                            return 'Вы уже подписаны'
                    except: 'Не удалось проверить подписку'
            if flag == 0:
                return "Запросили подписаться на что-то несуществующее, попробуйте ещё раз"

        except:
            for key in all_commands:
                for element in all_commands[key][2]:
                    if string == all_commands[key][2]:
                        d[key].append(user_id)
                        break
                    break
            f = open('subscribers.txt', 'w')
            f.write(str(d))
            return 'Вы успешно подписаны на ' + string
        finally:
            f.close()

    def del_from_file(self, d, user_id, name):
        d[name].remove(user_id)
        f = open('subscribers.txt', 'w')
        f.write(str(d))
        f.close()
        return 'Они больше вас не побеспокоят'

    def unfollow(self, string, user_id, all_commands):
        try:
            f = open('subscribers.txt', 'r')
            d = eval(f.read())
            f.close()
            flag = 0
            for key in all_commands:
                for element in all_commands[key][2]:
                    try:
                        if string == element:
                            flag =1
                            return (self.del_from_file(d, user_id, key))
                    except:pass
            if flag == 0:
                return "Запросили отписаться от чего-то несуществующего"
        except:
            return 'Не удалось отписаться'
        finally:
            f.close()

    def list_of_subscribers(self, user_id, all_commands):
        buf = ''
        try:
            f = open('subscribers.txt', 'r')
            d = eval(f.read())
            for key in all_commands:
                try:
                    d[key].index(user_id)
                    buf += ' ' + str(all_commands[key][2][0])
                except:
                    pass
            if len(buf) > 2:
                return 'Вы подписаны на' + buf
            else:
                return 'Вы ни на что не подписаны'
        except:
            return 'Произошла ошибка при выведении списка подписок'

    def main_f(self, string, user_id, all_commands):
        try:
            return self.check(string, user_id, all_commands)
        except:
            pass
