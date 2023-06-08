from PySide6.QtCore import QPropertyAnimation, QRect, QBasicTimer
from PySide6.QtGui import Qt, QPixmap
from PySide6.QtWidgets import QWidget, QLabel, QProgressBar


class Notification(QWidget):

    def __init__(self, Title: str, message: str, icon: str, time: int, parent=None):
        super(Notification, self).__init__(parent)

        # Title текст
        self.Title_label = QLabel(self)
        self.Title_label.setText(Title)
        self.Title_label.move(40, 10)
        # Сообщение текст
        self.message_label = QLabel(self)
        self.message_label.setText(message)
        self.message_label.move(40, 30)
        # Прогресс бар
        self.progressbar = QProgressBar(self)
        self.progressbar.setGeometry(0, 52, 220, 3)
        self.step = 0
        # Таймер для прогресбара
        self.timer = QBasicTimer()
        self.progressbar_count = 0
        # Иконка (png)
        self.icon_label = QLabel(self)
        self.pixmap = QPixmap(str(icon))
        self.pixmap = self.pixmap.scaled(32, 32)
        self.icon_label.setPixmap(self.pixmap)
        self.icon_label.move(3, 10)
        # Флаги для окна
        self.setWindowOpacity(0.94)
        flags = self.windowFlags() | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool
        self.setWindowFlags(flags)
        # Изменяет цвет фона
        self.setStyleSheet("background-color: rgb(194, 199, 213)")
        # Настройки координат для анимации
        self.x = 10
        self.y = 0
        # Анимация
        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setStartValue(QRect(self.x, self.y, 0, 55))
        self.anim.setEndValue(QRect(self.x, self.y, 220, 55))
        self.anim.setDuration(350)
        self.anim.start()
        self.start_proggers(time)

    # Закрывает уведомление по клику
    def mousePressEvent(self, event):
        self.close()

    # Закрывает уведомление через время
    def start_proggers(self, time: int):
        self.progressbar_count = time * 100
        self.progressbar.setMaximum(self.progressbar_count)
        if not self.timer.isActive():
            self.timer.start(10, self)

    def timerEvent(self, e):
        if self.step >= self.progressbar_count:
            self.timer.stop()
            self.hide()
            return
        self.step += 1
        self.progressbar.setValue(self.step)
