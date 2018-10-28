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
        main_tower = s.MainTower('MainTower', 1500, 250, 200, 200,
                                 path_to_sprites + 'main_tower.png')
        main_tower.get_component('HealthSystem').set_health(3000)
        game_objects.append(main_tower)
        game_objects.append(s.VisibleGameObject('UIBackround', 800, 800,
                                                1600, 200, path_to_sprites + 'background_for_ui.png'))

        enemys_manager = s.InvisibleGameObject('EnemysManager', 0, 0, 0, 0)
        controller = b.Manager()
        controller.add_ai_point(s.GameObject('AIPoint1', 375, 470, 0, 0))
        controller.add_ai_point(s.GameObject('AIPoint2', 1135, 240, 0, 0))
        controller.add_ai_point(s.GameObject('AIPoint3', 1400, 240, 0, 0))
        controller.set_spawn_point(s.GameObject('spawn_point', 100, 470, 0, 0))
        enemys_manager.add_behaviour(controller)
        game_objects.append(enemys_manager)

        gold_manager = s.InvisibleGameObject('GoldManager', 0, 0, 0, 0)
        gold_manager.add_behaviour(b.GoldManager())
        game_objects.append(gold_manager)

        game_objects.append(s.SceneManager('SceneManager', 0, 0, 0, 0))

        tower1 = s.DefenceTower('DefenceTower1', 0, 0,
                                64, 64, os.path.join(path_to_sprites + 'defence_tower_1', ''))
        tower1_level2 = s.DefenceTower('DefenceTower1', 0, 0,
                                       64, 64, os.path.join(path_to_sprites + 'defence_tower_1_2', ''))

        tower1.get_component('DefenceTowerAttack').set_attack_radius(100)
        tower1.get_component('DefenceTowerAttack').set_damage(1)
        tower1.get_component('DefenceTowerAttack').set_type(1)
        tower1_level2.get_component('DefenceTowerAttack').set_attack_radius(150)
        tower1_level2.get_component('DefenceTowerAttack').set_damage(3)
        tower1_level2.get_component('DefenceTowerAttack').set_type(1)
        tower1_upgrade_manager = tower1.get_component('DefenceTowerUpgrade')
        tower1_upgrade_manager.activate()
        tower1_upgrade_manager.set_cost(60)
        tower1_upgrade_manager.set_next_tower(tower1_level2)
        tower1.get_component('ValuableObject').set_cost(30)

        tower2 = s.DefenceTower('DefenceTower1', 0, 0,
                                64, 64, os.path.join(path_to_sprites + 'defence_tower_1', ''))
        tower2.add_behaviour(b.ReinforcementTower())
        tower2_level2 = s.DefenceTower('DefenceTower1', 0, 0,
                                       64, 64, os.path.join(path_to_sprites + 'defence_tower_1_2', ''))
        tower1_level2.add_behaviour(b.ReinforcementTower())
        tower2.get_component('DefenceTowerAttack').set_attack_radius(150)
        tower2.get_component('DefenceTowerAttack').set_damage(2)
        tower2.get_component('DefenceTowerAttack').set_type(2)
        tower2_level2.get_component('DefenceTowerAttack').set_attack_radius(200)
        tower2_level2.get_component('DefenceTowerAttack').set_damage(4)
        tower2_level2.get_component('DefenceTowerAttack').set_type(2)
        tower2_upgrade_manager = tower2.get_component('DefenceTowerUpgrade')
        tower2_upgrade_manager.activate()
        tower2_upgrade_manager.set_cost(100)
        tower2_upgrade_manager.set_next_tower(tower2_level2)
        tower2.get_component('ValuableObject').set_cost(40)

        game_objects.append(s.TowerLabel('TowerLabel_1', 300, 800,
                                         200, 180, path_to_sprites + 'tower_label_1.png', 'tower_label_enable_1.png',
                                         tower1))
        game_objects.append(s.TowerLabel('TowerLabel_2', 550, 800,
                                         200, 180, path_to_sprites + 'tower_label_2.png', 'tower_label_enable_2.png',
                                         tower2))
        game_objects.append(s.UILabel('GoldLabel', 75, 750, 100, 50))

        restart_button = s.VisibleGameObject('RestartButton', 50, 30, 80, 45, path_to_sprites + 'restart_button.png')
        restart_button.add_behaviour(b.RestartButton())

        game_objects.append(restart_button)

        return game_objects

    def get_path_to_scene_sprite(self):
        return os.path.join('Sprites', 'scene_1.png')


class SecondSceneLoader(SceneLoader):
    def create_object(self):
        path_to_sprites = os.path.join('Sprites', '')

        game_objects = []
        main_tower = s.MainTower('MainTower', 1340, 500, 200, 200,
                                 path_to_sprites + 'main_tower.png')
        main_tower.get_component('HealthSystem').set_health(3000)
        game_objects.append(main_tower)
        game_objects.append(s.VisibleGameObject('UIBackround', 800, 800,
                                                1600, 200, path_to_sprites + 'background_for_ui.png'))

        enemys_manager = s.InvisibleGameObject('EnemysManager', 0, 0, 0, 0)
        controller = b.Manager()
        controller.set_spawn_point(s.GameObject('SpawnPoint', 225, 680, 0, 0))
        controller.add_ai_point(s.GameObject('AIPoint1', 225, 165, 0, 0))
        controller.add_ai_point(s.GameObject('AIPoint2', 545, 165, 0, 0))
        controller.add_ai_point(s.GameObject('AIPoint3', 545, 580, 0, 0))
        controller.add_ai_point(s.GameObject('AIPoint4', 850, 580, 0, 0))
        controller.add_ai_point(s.GameObject('AIPoint5', 850, 165, 0, 0))
        controller.add_ai_point(s.GameObject('AIPoint6', 1340, 165, 0, 0))
        controller.add_ai_point(s.GameObject('AIPoint7', 1340, 350, 0, 0))
        enemys_manager.add_behaviour(controller)
        game_objects.append(enemys_manager)

        gold_manager = s.InvisibleGameObject('GoldManager', 0, 0, 0, 0)
        gold_manager.add_behaviour(b.GoldManager())
        game_objects.append(gold_manager)

        game_objects.append(s.SceneManager('SceneManager', 0, 0, 0, 0))

        tower1 = s.DefenceTower('DefenceTower1', 0, 0,
                                64, 64, os.path.join(path_to_sprites + 'defence_tower_1', ''))
        tower1_level2 = s.DefenceTower('DefenceTower1', 0, 0,
                                       64, 64, os.path.join(path_to_sprites + 'defence_tower_1_2', ''))

        tower1.get_component('DefenceTowerAttack').set_attack_radius(100)
        tower1.get_component('DefenceTowerAttack').set_damage(1)
        tower1_level2.get_component('DefenceTowerAttack').set_attack_radius(150)
        tower1_level2.get_component('DefenceTowerAttack').set_damage(3)
        tower1_upgrade_manager = tower1.get_component('DefenceTowerUpgrade')
        tower1_upgrade_manager.activate()
        tower1_upgrade_manager.set_cost(60)
        tower1_upgrade_manager.set_next_tower(tower1_level2)
        tower1.get_component('ValuableObject').set_cost(30)

        tower2 = s.DefenceTower('DefenceTower1', 0, 0,
                                64, 64, os.path.join(path_to_sprites + 'defence_tower_1', ''))
        tower2.add_behaviour(b.ReinforcementTower())
        tower2_level2 = s.DefenceTower('DefenceTower1', 0, 0,
                                       64, 64, os.path.join(path_to_sprites + 'defence_tower_1_2', ''))
        tower1_level2.add_behaviour(b.ReinforcementTower())
        tower2.get_component('DefenceTowerAttack').set_attack_radius(150)
        tower2.get_component('DefenceTowerAttack').set_damage(2)
        tower2_level2.get_component('DefenceTowerAttack').set_attack_radius(200)
        tower2_level2.get_component('DefenceTowerAttack').set_damage(4)
        tower2_upgrade_manager = tower2.get_component('DefenceTowerUpgrade')
        tower2_upgrade_manager.activate()
        tower2_upgrade_manager.set_cost(100)
        tower2_upgrade_manager.set_next_tower(tower2_level2)
        tower2.get_component('ValuableObject').set_cost(40)

        game_objects.append(s.TowerLabel('TowerLabel_1', 300, 800,
                                         200, 180, path_to_sprites + 'tower_label_1.png', 'tower_label_enable_1.png',
                                         tower1))
        game_objects.append(s.TowerLabel('TowerLabel_2', 550, 800,
                                         200, 180, path_to_sprites + 'tower_label_2.png', 'tower_label_enable_2.png',
                                         tower2))
        game_objects.append(s.UILabel('GoldLabel', 75, 750, 100, 50))

        restart_button = s.VisibleGameObject('RestartButton', 50, 30, 80, 45, path_to_sprites + 'restart_button.png')
        restart_button.add_behaviour(b.RestartButton())

        game_objects.append(restart_button)

        return game_objects

    def get_path_to_scene_sprite(self):
        return os.path.join('Sprites', 'scene_2.png')


class MainMenuSceneLoader(SceneLoader):
    def create_object(self):
        path_to_sprites = os.path.join('Sprites', '')
        game_objects = []

        first_level_button = s.LevelLoadButton('FirstLevelButton', 120, 200, 160, 90, path_to_sprites + 'level_1.png',
                                               FirstSceneLoader())
        second_level_button = s.LevelLoadButton('SecondLevelButton', 300, 200, 160, 90, path_to_sprites + 'level_2.png',
                                                SecondSceneLoader())
        game_objects.append(second_level_button)
        game_objects.append(first_level_button)

        return game_objects

    def get_path_to_scene_sprite(self):
        return os.path.join('Sprites', 'main_menu.png')


class TestSceneLoader(SceneLoader):
    def create_object(self):
        return []

    def get_path_to_scene_sprite(self):
        return os.path.join('Sprites', 'main_menu.png')