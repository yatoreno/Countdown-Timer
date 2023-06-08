import os
import sys
from time import perf_counter

from PySide6 import QtCore, QtGui
from PySide6.QtCore import Slot, QSize
from PySide6.QtGui import QIcon, QIntValidator, QFont
from PySide6.QtWidgets import QMainWindow, QLabel, QApplication, QPushButton, QListWidgetItem, QListWidget, QLineEdit, \
    QComboBox, QMessageBox

import Timer_widget
from work_file import File


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # Настройки основного окна
        self.setWindowTitle('Timer by yatoreno')
        self.setGeometry(650, 150, 0, 0)

        font = QFont('Times', 12)
        self.setFont(font)

        # Нужно, чтобы в лайнедит можно было писать только цифры
        self.Validator = QIntValidator(self)

        # Нужно чтобы челы не меняли размеры окна
        self.setMaximumSize(400, 390)
        self.setMinimumSize(400, 390)

        # Создание едита для заполнения имени таймера
        self.Edit_timer_name = QLineEdit(self)
        self.Edit_timer_name.setPlaceholderText('Имя')
        self.Edit_timer_name.setGeometry(245, 60, 80, 20)

        # Создание едита для заполнения часов в таймер
        self.Edit_timer_hh = QLineEdit(self)
        self.Edit_timer_hh.setPlaceholderText('Часы')
        self.Edit_timer_hh.setGeometry(245, 85, 45, 20)
        self.Edit_timer_hh.setMaxLength(2)
        self.Edit_timer_hh.setValidator(self.Validator)

        # Создание едита для заполнения минут в таймер
        self.Edit_timer_mm = QLineEdit(self)
        self.Edit_timer_mm.setPlaceholderText('Минуты')
        self.Edit_timer_mm.setGeometry(295, 85, 45, 20)
        self.Edit_timer_mm.setMaxLength(2)
        self.Edit_timer_mm.setValidator(self.Validator)

        # Создание едита для заполнения секунд в таймер
        self.Edit_timer_ss = QLineEdit(self)
        self.Edit_timer_ss.setPlaceholderText('Cекунды')
        self.Edit_timer_ss.setGeometry(345, 85, 45, 20)
        self.Edit_timer_ss.setMaxLength(2)
        self.Edit_timer_ss.setValidator(self.Validator)

        # Создание текста для показания инфы о загрузке
        self.start_time_label = QLabel(self)
        self.start_time_label.setGeometry(245, 0, 320, 60)

        # Создание текста для ошибок
        self.warning_label = QLabel(self)
        self.warning_label.setStyleSheet('color: rgb(255, 0, 0);')
        self.warning_label.setGeometry(245, 122, 220, 60)

        # Создание текста подсказок
        self.text_with_hints = QLabel(self)
        self.text_with_hints.setText('Чтобы вызвать мини\n версию таймера '
                                     '2 раза\n кликните по виджету\n таймера!')
        self.text_with_hints.setGeometry(245, 165, 220, 65)

        # Комбобокс, где нужно будет выбирать иконки
        self.combobox_icon = QComboBox(self)
        self.combobox_icon.setGeometry(245, 115, 55, 26)
        self.combobox_icon.setIconSize(QSize(28, 28))
        self.combobox_icon.setMaxVisibleItems(7)
        # Добавление в combobox иконок для их выбора
        print(f'2. Загрузка Иконок {perf_counter() - start_time:0.6f}')
        # Выводит сообщение об ошибке если нет директории с иконками
        try:
            for i in os.listdir(path=directory_icons):
                self.combobox_icon.setEditable(False)
                icon = QIcon(f"{directory_icons}//{i}")
                self.combobox_icon.addItem(icon, "")
        except:
            self.criticalMessage('Создайте в одной директории с таймером\nпапку "Icon" и загрузите в него иконки')

        print(f'3. Загружено - {self.combobox_icon.count()} иконок за {perf_counter() - start_time:0.6f}')

        # Создание пространства, где будут виджеты (Таймера)
        self.ListWidget = QListWidget(self)
        self.ListWidget.setGeometry(5, 5, 235, 375)

        # Создание кнопок
        self.btn_add_new_timer = QPushButton(self)
        self.btn_add_new_timer.setGeometry(330, 58, 60, 22)
        self.btn_add_new_timer.setText('Добавить')

        # Здесь назначается функция для кнопки, где собирается инфа и создается таймер
        self.btn_add_new_timer.clicked.connect(self.check_line_edits)

        # Выводит сообщение об ошибке если нет в директории конфига
        try:
            # Загрузка таймеров из конфига
            self.loading_timers_from_config()
        except:
            self.criticalMessage(
                'Создайте в одной директории с таймером\nфайл "TimerConfig.json" и запишите в нем "[]"\nлибо скачайте его с github')

        # Создано для создания тест таймеров
        # self.Test_func()

    # Функция для вывода диалогового окна с ошибкой
    def criticalMessage(self, text):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('Ошибка')
        msgBox.setText(text)
        msgBox.exec()
        sys.exit()

    # Создано для создания тест таймеров
    def Test_func(self):
        for i in range(20):
            self.create_timer_widget('app.ico', f'Test{i}', '00:00:10')

    # Функция загрузки таймеров из конфига
    def loading_timers_from_config(self):
        config = File.read_file(directory_config)
        # Перебирает все таймера, получает данные и создает таймера
        for Timer in config:
            time = Timer["Time"]
            timername = Timer["TimerName"]
            icon = Timer["Icon"]
            self.create_timer_widget(icon, timername, time, Timer_new=False)

    # Проверки лайнедитов на логику и создания таймеров
    def check_line_edits(self):
        if self.Edit_timer_hh.text() == "":
            hh = '00'
        if self.Edit_timer_mm.text() == "":
            mm = '00'
        if self.Edit_timer_ss.text() == "":
            ss = '00'
        if self.Edit_timer_hh.text() != "":
            if 10 > int(self.Edit_timer_hh.text()) >= 0:
                hh = f'0{self.Edit_timer_hh.text()}'
            elif int(self.Edit_timer_hh.text()) > 24:
                hh = '24'
            else:
                hh = int(self.Edit_timer_hh.text())
        if self.Edit_timer_mm.text() != "":
            if 10 > int(self.Edit_timer_mm.text()) >= 0:
                mm = f'0{self.Edit_timer_mm.text()}'
            elif int(self.Edit_timer_mm.text()) > 60:
                mm = '60'
            else:
                mm = int(self.Edit_timer_mm.text())
        if self.Edit_timer_ss.text() != "":
            if 10 > int(self.Edit_timer_ss.text()) >= 0:
                ss = f'0{self.Edit_timer_ss.text()}'
            elif int(self.Edit_timer_ss.text()) > 60:
                ss = '60'
            else:
                ss = int(self.Edit_timer_ss.text())
        list2 = File.read_file(directory_config)
        list_new = []
        for i in list2:
            list_new.append(i['TimerName'])
        if self.Edit_timer_name.text() in list_new:
            self.warning_label.setText('Такое имя уже есть!')
        elif self.Edit_timer_name.text() == "":
            self.warning_label.setText('Заполни строчку названия')
        elif len(self.Edit_timer_name.text()) < 2:
            self.warning_label.setText('Одного символа мало')
        else:
            self.warning_label.setText('')
            information = self.get_info_for_timer()
            self.create_timer_widget(icon=information[1], Name=information[0], time=f'{hh}:{mm}:{ss}')

    # Функция для сбора переменных и отправки в другую функцию
    def get_info_for_timer(self):
        global directory_icons
        # Берет текст
        timer_name = self.Edit_timer_name.text()
        # Использует класс, "File", чтобы получить полное имя с директорией иконки
        timer_icon = File.get_icon_name(file=directory_icons, index=self.combobox_icon.currentIndex())
        # Функция для создания виджетов таймера
        return timer_name, timer_icon

    # Функция создания таймера по кнопке
    def create_timer_widget(self, icon, Name, time, Timer_new=True):
        # Создает виджет и берет его как переменную
        new_timer = Timer_widget.Widget(icon=icon, Timer_Name=Name, Time=time)

        # Добавляет виджет в лист на основном окне и также настраивает его размеры
        my_item = QListWidgetItem(self.ListWidget)
        my_item.setSizeHint(QtCore.QSize(220, 50))
        self.ListWidget.setItemWidget(my_item, new_timer)
        # Кнопка удалить конектится к функции удаления виджекта по индексу
        new_timer.delete_timer.connect(self.delete_timer_on_main_window)
        if Timer_new:
            File.write_file(directory_config, Name, icon, time, self.ListWidget.count() - 1)

    # Удаление таймера на основном окне по кнопке (Нужно имя таймера, чтобы удалять)
    @Slot()
    def delete_timer_on_main_window(self, TimerName):
        list1 = File.read_file(directory_config)
        for i in list1:
            index = i['id']
            name = i["TimerName"]
            if name == TimerName:
                self.ListWidget.takeItem(index)
                File.delete_file(directory_config, TimerName)
                del index
        print('Удалил таймер')


if __name__ == '__main__':
    # Функция для поиска директории в Temp, нужна если прогу конвертируешь в exe и засовываешь в onefile и добавляешь свои файлы
    # Функцию спиздил в инете сами разбирайтесь как работает
    def resource_path(relative_path):
        # Get absolute path to resource, works for dev and for PyInstaller
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)


    # Различные переменные
    directory_config = 'TimerConfig.json'
    directory_icons = 'Icon'

    # Переменная для вычесления времени запуска
    start_time = perf_counter()
    print('1. Начало запуска таймера', f'{perf_counter() - start_time:0.6f}')

    # Хуй знает зачем, но очень важно, читайте документацию
    app = QApplication(sys.argv)

    # Добавления стиля приложения и иконки
    print(resource_path('Style.qss'))
    app.setStyleSheet(open(resource_path('Style.qss'), 'r').read())
    app.setWindowIcon(QtGui.QIcon(resource_path('app.ico')))

    # Создание окна + показывает его
    w = MainWindow()
    w.show()
    print('4. Приложение запущено', f'{perf_counter() - start_time:0.6f}')
    # Текстик меняю у label'a
    w.start_time_label.setText(f'Приложение запущено за\n{perf_counter() - start_time:0.6f} секунд')
    # Хуй знает зачем, но очень важно, читайте документацию долбаебы
    sys.exit(app.exec())
