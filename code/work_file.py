import json
import os


class File:

    # Писал данные функции еще в первой версии таймера поэтому сами разбирайтесь, что тут и как
    # можете просто разобраться как работает json

    # Перебирает в директории иконки и возвращает нужную иконку по индексу
    @staticmethod
    def get_icon_name(file, index):
        pic_count = 0
        for i in os.listdir(path=file):
            name = i
            if index == pic_count:
                return f'{file}//{name}'
            pic_count += 1

    # Читает конфиг и возвращает его данные
    @staticmethod
    def read_file(file):
        with open(file, "r", encoding='utf-8') as f:
            TimerConfig = json.load(f)
            return TimerConfig

    # Записывает таймер в конфиг
    @staticmethod
    def write_file(file, timername, icon, time, id):
        list = {
            "TimerName": timername,
            "Icon": icon,
            "Time": time,
            "id": id
        }
        newlist = []
        newlist.append(list)
        massive = File.read_file(file) + newlist
        with open(file, "w", encoding='utf-8') as f:
            json.dump(massive, f, indent=4, ensure_ascii=False)

    # Переназначение id в конфиге, нужно, чтобы поменять id листа при удалении одного из таймеров
    @staticmethod
    def id_in_config(file):
        list = File.read_file(file)
        empty_list = []
        new_id = 0
        for i in list:
            list_new = {
                "TimerName": i['TimerName'],
                "Icon": i['Icon'],
                "Time": i["Time"],
                "id": new_id
            }
            empty_list.append(list_new)
            new_id += 1
        with open(file, "w", encoding='utf-8') as f:
            json.dump(empty_list, f, indent=4, ensure_ascii=False)

    # Удаляет таймер из конфига
    @staticmethod
    def delete_file(file, timername):
        list = File.read_file(file)
        for i in list:
            if i['TimerName'] == timername:
                list.remove(i)
        with open(file, "w", encoding='utf-8') as f:
            json.dump(list, f, indent=4)
        File.id_in_config(file)
