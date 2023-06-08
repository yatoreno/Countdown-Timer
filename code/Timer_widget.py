from PySide6 import QtGui
from PySide6.QtCore import Signal, Slot, QThread, QRect, Qt
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QGroupBox, QSlider
import Timer_on_window

from my_Notification import Notification


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

        # Настройка размера и шрифта текста (Сразу всех виджетов)
        self.setFont(QFont('Times', 10))

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
        self.Timer_label.setGeometry(QRect(42, 12, 60, 22))

        # Создание + настройка слайдера, который нужен для корректировки времени
        # (например, если босс был мертв и нужно поставить таймер с меньшим временем)
        self.slider = QSlider(Qt.Orientation.Horizontal, self.groupbox)
        self.slider.setGeometry(QRect(39, 33, 52, 6))
        self.slider.setPageStep(1)

        # Коннект слайдера при каждом его изменении
        self.slider.valueChanged[int].connect(self.slider_change_time)
        # Вызов функции для установки значения и максимума слайдера
        self.change_slider()

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

    # Создание уведомления
    def create_notification(self):
        print(f'Сработало уведомление "{self.Timer_Name}"')
        self.var_notif = Notification(Title=self.Timer_Name, message='Возрадиться через 01:30 секунд', icon=self.icon, time=5)
        self.var_notif.show()

    # Функция в которой в соотношение со временем устанавливается позиция слайдера и его максимум
    def change_slider(self):
        hour = int(self.Time[0:2])
        minute = int(self.Time[3:5])
        count_minute = int(hour * 60 + minute)
        self.slider.setMaximum(count_minute)
        self.slider.setSliderPosition(count_minute)

    # Функция, где при изменении слайдера меняется время
    def slider_change_time(self, value):
        hour = int(self.Time[0:2])
        minute = int(self.Time[3:5])
        second = int(self.Time[6:8])
        count_minute = int(hour * 60 + minute)
        new_hour = 0
        new_count_minute = count_minute - value
        count_minute = count_minute - new_count_minute
        while count_minute > 60:
            new_hour += 1
            count_minute -= 60
        new_label = '{:02d}:{:02d}:{:02d}'.format(int(new_hour), int(count_minute), int(second))
        self.Timer_label.setText(new_label)

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
            # сигнал на создание уведомления
            self.thread.notifcation_signal.connect(self.create_notification)
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
    notifcation_signal = Signal()

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
            # Создает уведомление за полторы минуты до окончания таймера
            if time_format == '00:01:30':
                self.notifcation_signal.emit()
            QThread.msleep(1000)
