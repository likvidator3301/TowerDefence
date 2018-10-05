#!/usr/bin/env python3

import sys
import SecondOrderGameObject as s
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout,\
    QLabel, QApplication
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QPixmap, QImage, QPalette, QBrush
from PyQt5.QtCore import QSize, Qt, QRect
from PyQt5.Qt import QCursor
from PyQt5 import QtWidgets


class MainWindow(QWidget):
    def __init__(self, width, height, fullscreen):
        super().__init__()
        self.window_height = height
        self.window_width = width
        self.initUI(fullscreen)
        self.mouse_down = False
        self.setMouseTracking(True)

    def initUI(self, fullscreen):
        self.setWindowTitle('MyGameEngine')
        if fullscreen:
            self.showFullScreen()
        else:
            self.show()

    def show_scene(self, scene):
        self.close()
        self.game_objects = {}
        self.static_game_object = {}
        self.scene_label = SceneLabel(self)
        pixmap = QPixmap(scene.background)
        self.scene_label.move(0, 0)
        self.scene_label.resize(pixmap.width(), pixmap.height())
        self.scene_label.setPixmap(pixmap)
        self.showFullScreen()

    def draw_game_object(self, game_object):
        x = int(game_object.x - game_object.width / 2)
        y = int(game_object.y - game_object.height / 2)
        if x >= self.window_width or y >= self.window_height or x < 0 or y < 0:
            return

        self.scene_label.close()

        if game_object.tag == 'UI':
            lbl = ObjectLabel(self.scene_label, game_object.name)
            lbl.move(x, y)
            lbl.setText(game_object.text)
            lbl.resize(game_object.width, game_object.height)
            self.game_objects[game_object.name] = lbl
        else:
            lbl = ObjectLabel(self.scene_label, game_object.name)
            pixmap = QPixmap(game_object.path_to_sprite)
            lbl.resize(game_object.width, game_object.height)
            lbl.move(x, y)
            lbl.resize(game_object.width, game_object.height)
            lbl.setPixmap(pixmap)
            self.game_objects[game_object.name] = lbl

        self.scene_label.showFullScreen()

    def destroy_object(self, name):
        if name in self.game_objects and not self.game_objects[name] is None:
            self.game_objects[name].deleteLater()
            self.game_objects[name] = None

    def get_left_button_down(self):
        return self.scene_label.mouse_down

    def get_right_button_down(self):
        return self.scene_label.right_mouse_down

    def object_left_click(self, game_object):
        if not self.game_objects[game_object.name] is None:
            return self.game_objects[game_object.name].left_mouse_down
        return False

    def pass_event(self):
        self.scene_label.mouse_down = False
        self.scene_label.mouse_event = None
        self.scene_label.click_pos = None
        self.scene_label.right_mouse_down = False

    def get_mouse_click_pos(self):
        return self.scene_label.click_pos

    def get_mouse_event(self):
        try:
            return self.scene_label.mouse_event
        except:
            return None


class SceneLabel(QLabel):
    def __init__(self, parrent):
        super().__init__(parrent)
        self.mouse_down = False
        self.right_mouse_down = False

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            self.mouse_down = True
        elif QMouseEvent.button() == Qt.RightButton:
            self.right_mouse_down = True
        self.mouse_event = QMouseEvent
        self.click_pos = QMouseEvent.pos()


class ObjectLabel(QLabel):
    def __init__(self, parrent, name):
        super().__init__(parrent)
        self.left_mouse_down = False

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.left_mouse_down = True


if __name__ == "__main__":
    pass
