#!/usr/bin/env python3

import os
import Interfaces as i
import SecondOrderGameObject as s
from PyQt5.QtCore import QPoint
from CrotysEngine import GameObjects, Constants


class LabelForCreateObject(i.IBehaviour):
    def __init__(self, obj, path_to_enable_object):
        self.path_to_enable_object = path_to_enable_object
        self.name = 'LabelForCreateObject'
        self.object = obj
        self.cost = obj.get_component('ValuableObject').get_cost()

    def start(self, session, game_object):
        self.path_to_default_object = game_object.path_to_sprite
        self.scene_manager = session.get_object_by_name('SceneManager')\
            .get_component('SceneManager')
        self.gold_manager = session.get_object_by_name('GoldManager')\
            .get_component('GoldManager')

    def update(self, session, game_object):
        if session.input.get_right_button_scene_down(session):
            self.scene_manager.stop_tracking()
            game_object.path_to_sprite = self.path_to_default_object

    def on_mouse_down(self, session, game_object):
        if self.gold_manager.get_gold() >= self.cost:
            game_object.path_to_sprite = self.path_to_enable_object
            self.scene_manager.set_creating_object(self.object, self.cost)
            self.scene_manager.start_tracking()


class SceneManager(i.IBehaviour):
    def __init__(self):
        self.name = 'SceneManager'

    def start(self, session, game_object):
        self.gold_manager = session.get_object_by_name('GoldManager') \
            .get_component('GoldManager')
        self.object = None
        self.tracking = False
        self.cost = 0

    def update(self, session, game_object):
        if not self.tracking:
            return

        if session.input.get_left_button_scene_down(session) and self.gold_manager.get_gold() >= self.cost:
            pos = session.input.get_click_pos(session)
            x = pos.x()
            y = pos.y()

            object = GameObjects.instantiate(self.object)

            object.x = x
            object.y = y

            session.add_game_object(object)
            self.gold_manager.change_gold(-self.cost)

    def set_creating_object(self, object, cost):
        self.object = object
        self.cost = cost

    def start_tracking(self):
        self.tracking = True

    def stop_tracking(self):
        self.tracking = False
        self.cost = 0


class HealthSystem(i.IBehaviour):
    def __init__(self):
        self.name = 'HealthSystem'

    def start(self, session, game_object):
        self.health = 300

    def update(self, session, game_object):
        if self.health <= 0:
            session.destroy_object(game_object)

    def change_health(self, delta):
        self.health += delta

    def set_health(self, value):
        self.health = value


class AIController(i.IBehaviour):
    def __init__(self):
        self.name = 'AIController'

    def start(self, session, game_object):
        self.speed = 3
        self.count_of_passed_point = 0
        self.manager = session.get_object_by_name('EnemysManager')
        self.ai_points = self.manager.get_component('Manager').get_ai_points()
        self.target = self.ai_points[0]
        self.finish = False

    def update(self, session, game_object):
        if self.finish:
            return

        distance = GameObjects.\
            get_distance_between_game_objects(game_object, self.target)
        if (self.count_of_passed_point < len(self.ai_points) - 1 and
                distance < 50):
            self.count_of_passed_point += 1
            try:
                self.target = self.ai_points[self.count_of_passed_point]
            except Exception:
                return
        else:
            if (self.count_of_passed_point == len(self.ai_points) - 1 and
                    distance < 50):
                self.finish = True
                return

            dx = self.target.x - game_object.x
            dy = self.target.y - game_object.y

            speedX = int((dx / distance) * self.speed)
            speedY = int((dy / distance) * self.speed)

            game_object.x += speedX
            game_object.y += speedY

    def destroy(self, session, game_object):
        session.get_object_by_name('GoldManager') \
            .get_component('GoldManager') \
            .change_gold(game_object.get_component('ValuableObject') \
                         .get_cost())
        session.get_object_by_name('EnemysManager') \
            .get_component('Manager').on_destroy_enemy()


class Manager(i.IBehaviour):
    def __init__(self):
        self.name = 'Manager'
        self.max_count_of_enemys = 0

    def start(self, session, game_object):
        self.player_win = False
        self.enemy_id = 0
        self.count_of_enemys = 0
        self.count_of_enemys_on_scene = 0
        self.spawn_point = s.GameObject('spawn_point', 100, 470, 0, 0)
        self.ai_points = []
        self.ai_points.append(s.GameObject('AIPoint1', 375, 470, 0, 0))
        self.ai_points.append(s.GameObject('AIPoint2', 1135, 240, 0, 0))
        self.ai_points.append(s.GameObject('AIPoint3', 1400, 240, 0, 0))
        game_object.started = True
        self.timer = 350
        self.first_wave = True
        self.second_wave = False
        self.third_wave = False
        self.first_interval = 90
        self.second_interval = 75
        self.third_interval = 60
        self.first_count = 2
        self.second_count = 3
        self.third_count = 4

    def update(self, session, game_object):
        count_of_enemys = 0
        interval = 0
        if self.first_wave:
            count_of_enemys = self.first_count
            interval = self.first_interval
        elif self.second_wave:
            count_of_enemys = self.second_count
            interval = self.second_interval
        elif self.third_wave:
            count_of_enemys = self.third_count
            interval = self.third_interval
        elif self.count_of_enemys_on_scene == 0 and not self.player_win:
            self.win_game(session)

        if self.count_of_enemys < count_of_enemys and self.timer > interval:
            name = 'Enemy' + str(self.enemy_id)
            enemy = s.Enemy(name, self.spawn_point.x, self.spawn_point.y,
                 64, 64, os.path.join('Sprites', 'enemy_1.png'))
            enemy.get_component('ValuableObject').set_cost(10)
            session.add_game_object(enemy)
            self.enemy_id += 1
            self.count_of_enemys += 1
            self.count_of_enemys_on_scene += 1
            self.timer = 0
        elif self.count_of_enemys == count_of_enemys:
            if not self.third_wave:
                self.count_of_enemys = 0

            self.timer = -150
            if self.first_wave:
                self.first_wave = False
                self.second_wave = True
            elif self.second_wave:
                self.second_wave = False
                self.third_wave = True
            elif self.third_wave:
                self.third_wave = False
        self.timer += 1

    def win_game(self, session):
        session.add_game_object(s.VisibleGameObject('GameWin', 800, 450, 800, 250,
                                                    os.path.join('Sprites', 'game_win_label.png')))
        self.player_win = True

    def get_ai_points(self):
        return self.ai_points

    def on_destroy_enemy(self):
        self.count_of_enemys_on_scene -= 1


class GoldLabel(i.IBehaviour):
    def __init__(self):
        self.name = 'GoldLabel'
        self.text = 'Gold: '
        self.started = False

    def start(self, session, game_object):
        self.label = game_object
        self.started = True

    def set_text(self, text):
        if self.started:
            self.text = text
            self.label.text = text

    def get_text(self):
        return self.text


class MovePoint(i.IBehaviour):
    def __init__(self):
        self.name = 'MovePoint'

class GoldManager(i.IBehaviour):
    def __init__(self):
        self.name = 'GoldManager'

    def start(self, session, game_object):
        self.gold = 100
        self.label = session.get_object_by_name('GoldLabel')\
            .get_component('GoldLabel')
        self.label.set_text('Gold: ' + str(self.gold))

    def update(self, session, game_object):
        self.label.set_text('Gold: ' + str(self.gold))

    def set_gold(self, count):
        self.gold = count

    def get_gold(self):
        return self.gold

    def change_gold(self, delta):
        self.gold += delta


class ValuableObject(i.IBehaviour):
    def __init__(self):
        self.name = 'ValuableObject'
        self.cost = 0

    def set_cost(self, cost):
        self.cost = cost

    def get_cost(self):
        return self.cost


class DefenceTowerAttack(i.IBehaviour):
    def __init__(self):
        self.name = 'DefenceTowerAttack'
        self.attack_radius = 150
        self.damage = 3

    def update(self, session, game_object):
        target = None
        min_dist = 5000
        for name in session.scene.game_objects:
            object = session.get_object_by_name(name)
            if object is None or object.tag != 'Enemy':
                continue
            dist = GameObjects\
                .get_distance_between_game_objects(game_object, object)
            if dist < min_dist and dist <= self.attack_radius:
                target = object
                min_dist = dist
        if target is None:
            return

        health_system = target.get_component('HealthSystem')
        if health_system is not None:
            health_system.change_health(-self.damage)

    def set_attack_radius(self, value):
        self.attack_radius = value

    def set_damage(self, value):
        self.damage = value


class EnemyAttack(i.IBehaviour):
    def __init__(self):
        self.name = 'EnemyAttack'
        self.attack_radius = 400
        self.damage = 1

    def start(self, session, game_object):
        self.main_tower = session.get_object_by_name('MainTower')
        if self.main_tower is None:
            self.active = False
            return
        else:
            self.active = True
        self.main_tower_health_system = self\
            .main_tower.get_component('HealthSystem')

    def update(self, session, game_object):
        if not self.active:
            return
        dist = GameObjects\
            .get_distance_between_game_objects(game_object, self.main_tower)
        if dist <= self.attack_radius:
            self.main_tower_health_system.change_health(-self.damage)

    def set_attack_radius(self, value):
        self.attack_radius = value

    def set_damage(self, value):
        self.damage = value

    def stop(self):
        self.active = False

class HealthLabel(i.IBehaviour):
    count = 0

    def __init__(self):
        self.name = 'HealthLabel'

    def start(self, session, game_object):
        self.label_name = 'HealthLabel_' + str(HealthLabel.count)
        HealthLabel.count += 1
        self.health_system = game_object.get_component('HealthSystem')
        self.max_health = self.health_system.health
        self.one_sixed_part = int(self.max_health / 6)
        self.part_of_max_health = 0
        self.drawed = False

    def update(self, session, game_object):
        part_of_max_health = int(self.health_system.health / self.one_sixed_part) + 1
        if part_of_max_health > 6:
            part_of_max_health = 6
        if part_of_max_health != self.part_of_max_health:
            if self.drawed:
                session.destroy_object(self.label)
            self.label = s.VisibleGameObject(self.label_name, game_object.x,
                                             int(game_object.y - game_object.height / 2 - 10),
                                             60, 6, os.path.join('Sprites',
                                                                 'health_' + str(part_of_max_health) + '.png'))
            self.part_of_max_health = part_of_max_health
            self.drawed = True
            session.add_game_object(self.label)

        self.label.x = game_object.x
        self.label.y = int(game_object.y - game_object.height / 2 - 10)

    def destroy(self, session, game_object):
        session.destroy_object(self.label)


class MainTowerController(i.IBehaviour):
    def __init__(self):
        self.name = 'MainTowerController'

    def destroy(self, session, game_object):
        session.add_game_object(s.VisibleGameObject('GameOver', 800, 450, 800, 250,
                                                    os.path.join('Sprites', 'game_over_label.png')))
        enemys = session.scene.get_objects_by_tag('Enemy')
        for enemy in enemys:
            enemy.get_component('EnemyAttack').stop()

class RestartButton(i.IBehaviour):
    def __init__(self):
        self.name = 'RestartButton'

    def on_mouse_down(self, session, game_object):
        session.restart_game()

class LevelLoaderButton(i.IBehaviour):
    def __init__(self):
        self.name = 'LevelLoaderButton'

    def on_mouse_down(self, session, game_object):
        session.load_scene(self.scene_loader)

    def set_scene_loader(self, scene_loader):
        self.scene_loader = scene_loader

class Animator(i.IBehaviour):
    def __init__(self):
        self.name = 'Animator'
        self.path_to_animation = ''
        self.pathes_to_sprites = []
        self.timeout_in_frame = 1
        self.counter = 0
        self.number_of_frame = 1

    def start(self, session, game_object):
        self.playing = True

    def set_path_to_animation(self, game_object, path_to_animation):
        self.pathes_to_sprites = os.listdir(path_to_animation)
        for i in range(0, len(self.pathes_to_sprites)):
            self.pathes_to_sprites[i] = path_to_animation + self.pathes_to_sprites[i]
        game_object.path_to_sprite = self.pathes_to_sprites[0]

    def set_speed(self, speed_frame_per_second):
        self.timeout_in_frame = 33 // speed_frame_per_second

    def play(self):
        self.playing = True

    def stop(self):
        self.playing = False

    def update(self, session, game_object):
        if not self.playing:
            return

        if self.counter >= self.timeout_in_frame:
            if self.number_of_frame >= len(self.pathes_to_sprites) - 1:
                self.number_of_frame = 0
            else:
                self.number_of_frame += 1
            game_object.path_to_sprite = self.pathes_to_sprites[self.number_of_frame]
            self.counter = 0
        self.counter += 1
