#!/usr/bin/env python3

import UIManager as ui_manager
import SceneLoader as o
import FirstOrderGameObject as f
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer


class GameSession:
    def __init__(self, scene_loader, debug):
        self.run = False
        self.paused = False
        self.need_to_restart = False
        self.need_to_load_next_scene = False
        self.need_to_pause = False
        self.need_to_continue = False
        self.next_scene_loader = None
        self.objects_for_create = []
        self._load_scene(scene_loader)
        self.input = Input()
        if not debug:
            self.window = ui_manager.MainWindow(1600, 900, True)
            self.window.show_scene(self.scene)
            self.create_level(self.current_scene_loader.create_object())

    def load_scene(self, scene_loader):
        self.need_to_load_next_scene = True
        self.stop_game()
        self.next_scene_loader = scene_loader

    def _load_scene(self, scene_loader):
        self.current_scene_loader = scene_loader
        self.scene = f.Scene(self.current_scene_loader.get_path_to_scene_sprite())

    def pause(self):
        self.need_to_pause = True

    def _pause(self):
        self.paused = True
        self.need_to_pause = False

    def continue_game(self):
        self.need_to_continue = True

    def _continue_game(self):
        self.paused = False
        self.need_to_continue = False

    def _load_next_scene(self):
        self._stop_game()
        self.upload_scene()
        self._load_scene(self.next_scene_loader)
        self.window.show_scene(self.scene)
        self.create_level(self.current_scene_loader.create_object())
        self.start_game()

    def upload_scene(self):
        self.scene = None
        self.current_scene_loader = None

    def create_level(self, objects):
        for object in objects:
            self._add_game_object(object)

    def get_object_by_name(self, name):
        return self.scene.get_object_by_name(name)

    def add_game_object(self, game_object):
        self.objects_for_create.append(game_object)

    def _add_game_object(self, game_object):
        self.scene.add_game_object(game_object)
        if game_object.visible:
            self.window.draw_game_object(game_object)

    def start_objects(self):
        for name in self.scene.game_objects:
            game_object = self.scene.get_object_by_name(name)
            if not game_object.started:
                for nameBehaviour in game_object.behaviour:
                    game_object.behaviour[nameBehaviour].start(self, game_object)
                game_object.started = True

    def destroy_object(self, game_object):
        game_object.destroyed = True

    def _destroy_object(self, game_object):
        self.scene.destroy_object_by_name(game_object.name)
        if game_object.visible:
            self.window.destroy_object(game_object.name)

    def get_objects_by_tag(self, tag):
        return self.scene.get_objects_by_tag(tag)

    def turn(self):
        self.objects_for_create.clear()
        objects = []

        for name in self.scene.game_objects:
            gameObject = self.scene.get_object_by_name(name)
            if gameObject is None:
                continue

            if (gameObject.x > self.window.window_width or gameObject.x < 0 or
                    gameObject.y > self.window.window_height or gameObject.y < 0):
                self.scene.destroy_object_by_name(name)
                self.window.destroy_object(name)
                continue
            for nameB in gameObject.behaviour:
                if (gameObject.visible and
                        self.input.left_mouse_button_down(self, gameObject)):
                    gameObject.behaviour[nameB].on_mouse_down(self, gameObject)
                if not self.paused:
                    gameObject.behaviour[nameB].update(self, gameObject)


            if gameObject.visible:
                self.window.destroy_object(gameObject.name)

            if not gameObject.destroyed:
                objects.append(gameObject)
            else:
                for nameBehaviour in gameObject.behaviour:
                    gameObject.behaviour[nameBehaviour].destroy(self, gameObject)

        for gameObject in self.objects_for_create:
            objects.append(gameObject)

        self.scene.delete_all_objects()

        for gameObject in objects:
            self._add_game_object(gameObject)

        self.start_objects()
        self.window.pass_event()

        if not self.run:
            self._stop_game()

        if self.need_to_restart:
            self._restart_game()
        elif self.need_to_load_next_scene:
            self._load_next_scene()
        elif self.need_to_pause:
            self._pause()
        elif self.need_to_continue:
            self._continue_game()

    def start_game(self):
        self.start_objects()
        self.timer = QTimer()
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.turn)
        self.timer.start(30)
        self.run = True
        self.need_to_restart = False
        self.need_to_load_next_scene = False
        self.need_to_pause = False
        self.need_to_continue = False

    def stop_game(self):
        self.run = False

    def restart_game(self):
        self.run = False
        self.need_to_restart = True

    def _restart_game(self):
        self._continue_game()
        scene_loader = self.current_scene_loader
        self.upload_scene()
        self._load_scene(scene_loader)
        self.create_level(self.current_scene_loader.create_object())
        self.start_game()

    def _stop_game(self):
        self.run = False
        self.timer.stop()
        self.scene.delete_all_objects()
        for obj in self.window.game_objects:
            self.window.destroy_object(obj)


class Input:
    def left_mouse_button_down(self, session, object):
        return session.window.object_left_click(object)

    def get_left_button_scene_down(self, session):
        return session.window.get_left_button_down()

    def get_right_button_scene_down(self, session):
        return session.window.get_right_button_down()

    def get_left_mouse_button_down_event(self, session):
        return session.window.get_mouse_event()

    def get_click_pos(self, session):
        return session.window.get_mouse_click_pos()

    def get_mouse_pos(self, session):
        return session.window.get_mouse_pos()


def main():
    app = QApplication(sys.argv)

    session = GameSession(o.MainMenuSceneLoader(), False)

    session.start_game()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
