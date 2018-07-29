#!/usr/bin/env python3

import GameEngine
import FirstOrderGameObject as f
import SecondOrderGameObject as s
import pytest

from BehaviourScripts import BehaviourScripts as b
from CrotysEngine import Constants


class TestScene:

    def test_create_scene(self):
        scene = f.Scene('path')

        assert scene.background == 'path'
        assert scene.game_objects == {}

    def test_add_object(self):
        obj = s.GameObject('GameObject', 0, 0, 0, 0)
        scene = f.Scene('path')
        scene.add_game_object(obj)

        assert scene.game_objects.__len__() == 1

    def test_clear_scene(self):
        obj = s.GameObject('GameObject', 0, 0, 0, 0)
        scene = f.Scene('path')
        scene.add_game_object(obj)

        assert scene.game_objects.__len__() == 1
        scene.delete_all_objects()
        assert scene.game_objects.__len__() == 0

    def test_get_object(self):
        obj = s.GameObject('GameObject', 0, 0, 0, 0)
        scene = f.Scene('path')
        scene.add_game_object(obj)

        assert obj == scene.get_object_by_name(obj.name)
        assert scene.get_object_by_name('blablabla') is None

    def test_destroy_object(self):
        obj = s.GameObject('GameObject', 0, 0, 0, 0)
        scene = f.Scene('path')
        scene.add_game_object(obj)

        assert scene.game_objects.__len__() == 1
        assert obj == scene.get_object_by_name(obj.name)
        scene.destroy_object_by_name(obj.name)
        assert scene.get_object_by_name(obj.name) is None

if __name__ == '__main__':
    pytest.main('SceneFunctionTest.py')
