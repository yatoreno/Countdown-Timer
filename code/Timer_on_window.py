from PySide6.QtCore import Qt, Slot, QPointF
from PySide6.QtGui import QPixmap, QFont, QColor
from PySide6.QtWidgets import QWidget, QLabel, QGraphicsDropShadowEffect


class Timer_on_top(QWidget):

    def __init__(self, Boss_name, time, icon, parent=None):
        super(Timer_on_top, self).__init__(parent)
        self.setGeometry(5, 150, 300, 100)
        font = QFont('Times', 12)
        self.setFont(font)

        # Флаги окна
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        flags = self.windowFlags() | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool
        self.setWindowFlags(flags)
        # Название босса
        self.Title_label = QLabel(self)
        self.Title_label.setText(Boss_name)
        self.Title_label.setStyleSheet('color: rgb(255, 255, 255);')
        self.Title_label.move(40, 0)
        # Настройка черной тени для белового текста
        shadow = QGraphicsDropShadowEffect(self,
                                           blurRadius=5.0,
                                           color=QColor("#000"),
                                           offset=QPointF(0.0, 0.0)
                                           )
        self.Title_label.setGraphicsEffect(shadow)
        # Время
        self.Time_label = QLabel(self)
        self.Time_label.setText(str(time))
        self.Time_label.move(40, 20)
        # Настройка белой тени для черного/красного времени
        shadow = QGraphicsDropShadowEffect(self,
                                           blurRadius=2.0,
                                           color=QColor("#fff"),
                                           offset=QPointF(0.0, 0.0)
                                           )
        self.Time_label.setGraphicsEffect(shadow)
        # Установка размера текста
        self.Time_label.setFont(QFont('Times', 12))

        # Иконка
        self.icon_label = QLabel(self)
        self.pixmap = QPixmap(str(icon))
        self.pixmap = self.pixmap.scaled(35, 35)
        self.icon_label.setPixmap(self.pixmap)
        self.icon_label.move(0, 0)

        self.press = False

    # Хуй знает что за код дальше, в инете нашел
    def mouseMoveEvent(self, event):
        if self.press:
            self.move(event.globalPos() - self.last_pos)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.press = True

        self.last_pos = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.press = False

    # Нужно, чтобы менять время и цвет
    @Slot(str)
    def set_time(self, time, word=None):
        print(time)
        self.Time_label.setText(time)
        if word == 'Стоп':
            self.Time_label.setStyleSheet('color: rgb(200, 0, 0);')
        elif word == 'Старт':
            self.Time_label.setStyleSheet('color: rgb(0, 0, 0);')

