#!/usr/bin/env python3

import os
import SecondOrderGameObject as s
from BehaviourScripts import BehaviourScripts as b


class SceneLoader:
    def __init__(self):
        pass

    def create_object(self):
        return None

    def get_path_to_scene_sprite(self):
        return None


class FirstSceneLoader(SceneLoader):
    def create_object(self):
        path_to_sprites = os.path.join('Sprites', '')

        game_objects = []
        main_tower = s.MainTower('MainTower', 1500, 300, 200, 200,
                                 path_to_sprites + 'main_tower.png')
        main_tower.get_component('HealthSystem').set_health(3000)
        game_objects.append(main_tower)
        game_objects.append(s.VisibleGameObject('UIBackround', 800, 800,
                                                1600, 200, path_to_sprites + 'background_for_ui.png'))

        enemys_manager = s.InvisibleGameObject('EnemysManager', 0, 0, 0, 0)
        controller = b.Manager()
        controller.set_max_enemys(5)
        enemys_manager.add_behaviour(controller)
        game_objects.append(enemys_manager)

        gold_manager = s.InvisibleGameObject('GoldManager', 0, 0, 0, 0)
        gold_manager.add_behaviour(b.GoldManager())
        game_objects.append(gold_manager)

        game_objects.append(s.SceneManager('SceneManager', 0, 0, 0, 0))

        tower1 = s.DefenceTower('DefenceTower1', 0, 0,
                                64, 64, path_to_sprites + 'defence_tower\\')
        tower2 = s.DefenceTower('DefenceTower2', 0, 0,
                                64, 64, path_to_sprites + 'defence_tower\\')

        tower1.get_component('DefenceTowerAttack').set_attack_radius(150)
        tower1.get_component('DefenceTowerAttack').set_damage(3)
        tower2.get_component('DefenceTowerAttack').set_attack_radius(200)
        tower2.get_component('DefenceTowerAttack').set_damage(5)

        tower1.get_component('ValuableObject').set_cost(30)
        tower2.get_component('ValuableObject').set_cost(40)

        game_objects.append(s.TowerLabel('TowerLabel_1', 300, 800,
                                         100, 180, path_to_sprites + 'tower_label_1.png', 'tower_label_enable_1.png',
                                         tower1))
        game_objects.append(s.TowerLabel('TowerLabel_2', 500, 800,
                                         100, 180, path_to_sprites + 'tower_label_2.png', 'tower_label_enable_2.png',
                                         tower2))
        game_objects.append(s.UILabel('GoldLabel', 75, 750, 100, 50))

        restart_button = s.VisibleGameObject('RestartButton', 64, 64, 64, 64, path_to_sprites + 'defence_tower_2.png')
        restart_button.add_behaviour(b.RestartButton())

        game_objects.append(restart_button)

        return game_objects

    def get_path_to_scene_sprite(self):
        return os.path.join('Sprites', 'scene_1.png')

class MainMenuSceneLoader(SceneLoader):
    def create_object(self):
        path_to_sprites = os.path.join('Sprites', '')
        game_objects = []

        first_level_button = s.LevelLoadButton('FirstLevelButton', 150, 300, 160, 90, path_to_sprites + 'level_1.png',
                                               FirstSceneLoader())
        game_objects.append(first_level_button)

        return game_objects

    def get_path_to_scene_sprite(self):
        return os.path.join('Sprites', 'main_menu.png')