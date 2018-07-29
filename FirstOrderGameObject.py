#!/usr/bin/env python3

import sys
import UIManager as ui_manager
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QApplication
from PyQt5.QtGui import QPixmap


class Scene:
    def __init__(self, background):
        self.background = background
        self.game_objects = {}

    def add_game_object(self, game_object):
        self.game_objects[game_object.name] = game_object

    def delete_all_objects(self):
        self.game_objects = {}

    def get_object_by_name(self, name):
        if name in self.game_objects:
            return self.game_objects[name]
        return None

    def destroy_object_by_name(self, name):
        self.game_objects[name] = None


if __name__ == '__main__':
    pass
