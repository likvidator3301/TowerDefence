#!/usr/bin/env python3

import unittest
import GameEngine
import FirstOrderGameObject as f
import SecondOrderGameObject as s
import pytest

from BehaviourScripts import BehaviourScripts as b
from CrotysEngine import Constants


class TestBehaviours:
    def test_label_for_create_object(self):
        scene = f.Scene('Sprites' + Constants.DELIMITER + 'scene_1.png')
        self.session = GameEngine.GameSession(scene, True)
        self.object = s.GameObject('GameObject', 0, 0, 0, 0)

        self.object.add_behaviour(b.ValuableObject())
        beh = b.LabelForCreateObject(self.object)

        gold_manager = s.InvisibleGameObject('GoldManager', 0, 0, 0, 0)
        gold_manager.add_behaviour(b.GoldManager())
        scene_manager = s.SceneManager('SceneManager', 0, 0, 0, 0)

        self.session.scene._add_game_object(gold_manager)
        self.session.scene._add_game_object(scene_manager)

        beh.start(self.session, self.object)

        assert beh.object == self.object
        assert beh.name == 'LabelForCreateObject'
        assert beh.cost == self.object.\
            get_component('ValuableObject').get_cost()
        assert beh.gold_manager == gold_manager.get_component('GoldManager')
        assert beh.scene_manager == scene_manager.get_component('SceneManager')

    def test_scene_manager(self):
        scene = f.Scene('Sprites' + Constants.DELIMITER + 'scene_1.png')
        self.session = GameEngine.GameSession(scene, True)
        self.object = s.GameObject('GameObject', 0, 0, 0, 0)
        self.session._add_game_object(s.GameObject('GoldManager', 0, 0, 0, 0))

        beh = b.SceneManager()
        beh.start(self.session, self.object)
        beh.set_creating_object(self.object, 100)

        assert beh.name == 'SceneManager'
        assert beh.object == self.object
        assert not beh.tracking

        beh.start_tracking()

        assert beh.tracking

    def test_health_system(self):
        scene = f.Scene('Sprites' + Constants.DELIMITER + 'scene_1.png')
        self.session = GameEngine.GameSession(scene, True)
        self.object = s.GameObject('GameObject', 0, 0, 0, 0)

        beh = b.HealthSystem()
        beh.start(self.session, self.object)

        assert beh.health == 300

        beh.set_health(400)
        assert beh.health == 400

        beh.change_health(-200)
        assert beh.health == 200

    def test_ai_controller(self):
        scene = f.Scene('Sprites' + Constants.DELIMITER + 'scene_1.png')
        self.session = GameEngine.GameSession(scene, True)
        self.object = s.GameObject('GameObject', 0, 0, 0, 0)

        enemys_manager = s.InvisibleGameObject('EnemysManager', 0, 0, 0, 0)
        controller = b.Manager()
        controller.set_max_enemys(5)
        enemys_manager.add_behaviour(controller)
        self.session._add_game_object(enemys_manager)

        beh = b.AIController()

        controller.start(self.session, self.object)
        beh.start(self.session, self.object)

        assert beh.ai_points == controller.ai_points

    def test_enemys_manager(self):
        scene = f.Scene('Sprites' + Constants.DELIMITER + 'scene_1.png')
        self.session = GameEngine.GameSession(scene, True)
        self.object = s.GameObject('GameObject', 0, 0, 0, 0)

        beh = b.Manager()
        beh.start(self.session, self.object)

        assert beh.name == 'Manager'
        assert beh.count_of_enemys == 0
        assert beh.max_count_of_enemys == 0
        assert beh.enemy_id == 0

        beh.count_of_enemys_on_scene = 5
        beh.on_destroy_enemy()
        assert beh.count_of_enemys_on_scene == 4

    def test_gold_label(self):
        scene = f.Scene('Sprites' + Constants.DELIMITER + 'scene_1.png')
        self.session = GameEngine.GameSession(scene, True)
        self.object = s.GameObject('GameObject', 0, 0, 0, 0)

        beh = b.GoldLabel()
        beh.start(self.session, self.object)

        assert beh.name == 'GoldLabel'
        assert beh.text == 'Gold: '

        beh.set_text('gaaaaaaaaameeeeeeeee')

        assert beh.text == 'gaaaaaaaaameeeeeeeee'

    def test_move_point(self):
        scene = f.Scene('Sprites' + Constants.DELIMITER + 'scene_1.png')
        self.session = GameEngine.GameSession(scene, True)
        self.object = s.GameObject('GameObject', 0, 0, 0, 0)

        beh = b.MovePoint()
        assert beh.name == 'MovePoint'

    def test_gold_manager(self):
        scene = f.Scene('Sprites' + Constants.DELIMITER + 'scene_1.png')
        self.session = GameEngine.GameSession(scene, True)
        self.object = s.GameObject('GameObject', 0, 0, 0, 0)

        beh = b.GoldManager()

        assert beh.name == 'GoldManager'

        beh.set_gold(100)
        assert beh.gold == 100

        beh.change_gold(100)
        assert beh.gold == 200

    def test_valueable_object(self):
        scene = f.Scene('Sprites' + Constants.DELIMITER + 'scene_1.png')
        self.session = GameEngine.GameSession(scene, True)
        self.object = s.GameObject('GameObject', 0, 0, 0, 0)

        beh = b.ValuableObject()

        assert beh.name == 'ValuableObject'
        assert beh.cost == 0

        beh.set_cost(100)
        assert beh.cost == 100

    def test_defence_tower_attack(self):
        scene = f.Scene('Sprites' + Constants.DELIMITER + 'scene_1.png')
        self.session = GameEngine.GameSession(scene, True)
        self.object = s.GameObject('GameObject', 0, 0, 0, 0)

        beh = b.DefenceTowerAttack()

        assert beh.name == 'DefenceTowerAttack'
        assert beh.attack_radius == 150
        beh.set_attack_radius(100)
        assert beh.attack_radius == 100
        assert beh.damage == 3
        beh.set_damage(5)
        assert beh.damage == 5

    def test_enemy_attack(self):
        scene = f.Scene('Sprites' + Constants.DELIMITER + 'scene_1.png')
        self.session = GameEngine.GameSession(scene, True)
        self.object = s.GameObject('GameObject', 0, 0, 0, 0)

        beh = b.EnemyAttack()

        assert beh.name == 'EnemyAttack'
        assert beh.attack_radius == 400
        beh.set_attack_radius(100)
        assert beh.attack_radius == 100
        assert beh.damage == 1
        beh.set_damage(5)
        assert beh.damage == 5
