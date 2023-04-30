from PySide6 import QtGui
from PySide6.QtCore import Signal, Slot, QThread, QRect
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QGroupBox

import Timer_on_window


class Widget(QWidget):
    delete_timer = Signal(str)
    time_signal_to_top = Signal(str, str)

    # Туть создается сам виджет
    def __init__(self, icon=None, Timer_Name=None, Time=None, parent=None):
        super(Widget, self).__init__(parent)

        # Имя таймера, нужно для его удаления
        self.Timer_Name = Timer_Name
        # Время таймера
        self.Time = Time
        # Данные о месторасположение иконки
        self.icon = icon

        # Нужно для проверки возможности открытия мини таймера
        self.timer_on_top = True

        # Группа, где находятся весь виджет, + имя
        self.groupbox = QGroupBox(self)
        self.groupbox.setTitle(str(self.Timer_Name))
        self.groupbox.setGeometry(QRect(1, 0, 224, 50))

        # Текст который потом будет иконкой
        self.icon_label = QLabel(self.groupbox)
        self.icon_label.setGeometry(QRect(5, 15, 32, 32))

        # Создание/добавление иконки + настройка размера иконки
        self.pixmap = QPixmap(str(self.icon))
        self.pixmap = self.pixmap.scaled(32, 32)
        # Здесь иконка натягивается на текст
        self.icon_label.setPixmap(self.pixmap)

        # Текст времени таймера
        self.Timer_label = QLabel(self.groupbox)
        self.Timer_label.setText(self.Time)
        self.Timer_label.setGeometry(QRect(40, 18, 60, 22))

        # Настройка кнопки удаление
        self.btn_delete_timer = QPushButton(self.groupbox)
        self.btn_delete_timer.setGeometry(QRect(155, 18, 60, 20))
        self.btn_delete_timer.setText('Удалить')

        # Настройка кнопки запуска/стопа
        self.btn_start_timer = QPushButton(self.groupbox)
        self.btn_start_timer.setGeometry(QRect(95, 18, 55, 20))
        self.btn_start_timer.setText('Старт')

        # Привязка кнопки удаления к функции
        self.btn_delete_timer.clicked.connect(self.delete_widget)
        # Привязка кнопки запуска таймера
        self.btn_start_timer.clicked.connect(self.start_timer)

    # Функция, в которой создается мини окошко поверх всех окон (Мини таймер) Сами разбирайтесь с этой хуйней
    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent):
        mouse_btn = str(event.buttons())
        if mouse_btn == 'MouseButton.LeftButton' and self.timer_on_top == True:
            self.Timer_window = Timer_on_window.Timer_on_top(Boss_name=self.Timer_Name, time=self.Time, icon=self.icon)
            self.time_signal_to_top.connect(self.Timer_window.set_time)
            self.Timer_window.show()

            self.timer_on_top = False
        elif mouse_btn == 'MouseButton.LeftButton' and self.timer_on_top == False:
            self.Timer_window.close()
            self.time_signal_to_top.disconnect(self.Timer_window.set_time)

            self.timer_on_top = True

    # Туть запускается таймер по кнопке
    def start_timer(self):
        if self.btn_start_timer.text() == 'Старт':
            # Создание/Запуск потока + привязка сигнала
            self.thread = Thread_timer(int(self.Timer_label.text()[0:2]), int(self.Timer_label.text()[3:5]),
                                       int(self.Timer_label.text()[6:8]))
            self.thread.threadSignal.connect(self.change_time_label)
            self.thread.start()
            # Изменяет цвет текста на красный
            self.Timer_label.setStyleSheet('color: rgb(255, 0, 0);')
            self.btn_start_timer.setText('Стоп')
        elif self.btn_start_timer.text() == 'Стоп':
            self.stop_timer()

    # Функция, которая меняет текст во время работы таймера через сигнал
    def change_time_label(self, time):
        self.Timer_label.setText(time)

        # Отсылает сигнал со временем для маленького окна, которое будет находиться сверху
        self.time_signal_to_top.emit(time, self.btn_start_timer.text())
        if time == '00:00:00':
            self.stop_timer()

    # Функция, которая киляет поток
    def stop_timer(self):
        print('stop')
        self.thread.terminate()
        # Изменяет цвет текста обратно на стандартный (черный)
        self.Timer_label.setStyleSheet('color: rgb(0, 0, 0);')
        self.btn_start_timer.setText('Старт')
        self.Timer_label.setText(self.Time)
        # Отсылает последнии данные если функция выключилась в мини окошко
        self.time_signal_to_top.emit(self.Time, self.btn_start_timer.text())

    # Функция, которая удаляет данный виджет, через отправку сигнала
    @Slot()
    def delete_widget(self):
        # Отправляет сигнал для удаления (отправляет имя босса)
        self.delete_timer.emit(self.Timer_Name)

        # Выключает таймер если он запущен
        if self.btn_start_timer.text() == 'Стоп':
            if self.thread.isRunning():
                self.stop_timer()


# Класс для работы в потоке (Потоки нужны, чтобы блять твоя прога не зависала нахуй)
class Thread_timer(QThread):
    threadSignal = Signal(str)

    def __init__(self, h, m, s):
        super().__init__()
        self.h = h
        self.m = m
        self.s = s

    # Функция, которая запускается при использовании класса
    def run(self):
        while True:
            # Хуйня, которая делает "00:00:00" такой формат
            time_format = '{:02d}:{:02d}:{:02d}'.format(self.h, self.m, self.s)
            self.s -= 1
            if self.s < 0:
                self.m -= 1
                self.s += 60
                if self.m < 0:
                    self.h -= 1
                    self.m += 60
            print(time_format)
            # Отправляет сигнал, чтобы менять время текста
            self.threadSignal.emit(time_format)
            QThread.msleep(1000)
