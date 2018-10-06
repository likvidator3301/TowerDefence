#!/usr/bin/env python3

import os
from BehaviourScripts import BehaviourScripts as b


class GameObject:
    def __init__(self, name, x, y, width, height):
        self.name = name
        self.tag = 'Untagged'
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.behaviour = {}
        self.started = False
        self.visible = False
        self.destroyed = False

    def add_behaviour(self, behaviour):
        self.behaviour[behaviour.name] = behaviour

    def get_component(self, name):
        if name in self.behaviour:
            return self.behaviour[name]
        return None

    def set_tag(self, tag):
        self.tag = tag

    def set_path_to_sprite(self, path):
        self.path_to_sprite = path


class VisibleGameObject(GameObject):
    def __init__(self, name, x, y, width, height, path_to_sprite):
        super().__init__(name, x, y, width, height)
        self.visible = True
        self.path_to_sprite = path_to_sprite


class InvisibleGameObject(GameObject):
    def __init__(self, name, x, y, width, height):
        super().__init__(name, x, y, width, height)


class MainTower(GameObject):
    def __init__(self, name, x, y, width, height, path_to_sprite):
        super().__init__(name, x, y, width, height)
        self.add_behaviour(b.HealthSystem())
        self.add_behaviour(b.HealthLabel())
        self.add_behaviour(b.MainTowerController())
        self.visible = True
        self.path_to_sprite = path_to_sprite


class AIPoint(GameObject):
    def __init__(self, name, x, y, width, height):
        super().__init__(name, x, y, width, height)
        self.add_behaviour(b.MovePoint())
        self.static = True


class Enemy(GameObject):
    def __init__(self, name, x, y, width, height, path_to_sprite):
        super().__init__(name, x, y, width, height)
        self.visible = True
        self.add_behaviour(b.AIController())
        self.add_behaviour(b.HealthSystem())
        self.add_behaviour(b.ValuableObject())
        self.add_behaviour(b.EnemyAttack())
        self.add_behaviour(b.HealthLabel())
        self.path_to_sprite = path_to_sprite
        self.set_tag('Enemy')


class TowerLabel(GameObject):
    def __init__(self, name, x, y, width, height, path_to_default_sprite, path_to_enable_sprite, object):
        super().__init__(name, x, y, width, height)
        self.visible = True
        self.path_to_sprite = path_to_default_sprite
        self.add_behaviour(b.LabelForCreateObject(object, os.path.join('Sprites', path_to_enable_sprite)))


class DefenceTower(GameObject):
    def __init__(self, name, x, y, width, height, path_to_sprite):
        super().__init__(name, x, y, width, height)
        self.visible = True
        self.path_to_sprite = path_to_sprite
        self.add_behaviour(b.ValuableObject())
        self.add_behaviour(b.DefenceTowerAttack())


class SceneManager(GameObject):
    def __init__(self, name, x, y, width, height):
        super().__init__(name, x, y, width, height)
        self.add_behaviour(b.SceneManager())


class UILabel(GameObject):
    def __init__(self, name, x, y, width, height):
        super().__init__(name, x, y, width, height)
        self.visible = True
        self.set_tag('UI')
        controller = b.GoldLabel()
        self.add_behaviour(controller)
        self.text = controller.get_text()


class LevelLoadButton(GameObject):
    def __init__(self, name, x, y, width, height, path_to_sprite, scene_loader):
        super().__init__(name,  x, y, width, height)
        self.visible = True
        self.path_to_sprite = path_to_sprite
        controller = b.LevelLoaderButton()
        controller.set_scene_loader(scene_loader)
        self.add_behaviour(controller)
