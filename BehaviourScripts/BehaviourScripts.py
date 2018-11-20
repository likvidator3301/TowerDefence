#!/usr/bin/env python3

import os
import Interfaces as i
import SecondOrderGameObject as s
from PyQt5.QtWidgets import QInputDialog
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

    def on_mouse_down(self, session, game_object):
        if self.gold_manager.get_gold() >= self.cost:
            game_object.path_to_sprite = self.path_to_enable_object
            self.scene_manager.set_creating_object(self.object, self.cost)
            mouse_pos = session.input.get_mouse_pos_by_object(session, game_object)
            x = int(game_object.x + mouse_pos.x() - game_object.width / 2)
            y = int(game_object.y + mouse_pos.y() - game_object.height / 2)
            self.scene_manager.set_mouse_pos(x, y)
            self.scene_manager.set_label(game_object, self.path_to_default_object)
            self.scene_manager.start_tracking()


class SceneManager(i.IBehaviour):
    def __init__(self):
        self.name = 'SceneManager'

    def start(self, session, game_object):
        self.end_game = False
        self.session = session
        self.gold_manager = session.get_object_by_name('GoldManager') \
            .get_component('GoldManager')
        self.object = None
        self.tracking = False
        self.cost = 0
        self.need_to_create_radius = False
        self.mouse_x = 0
        self.mouse_y = 0
        self.session = session
        self.label = None
        self.path_to_default_sprite = ''

    def set_label(self, label, path_to_default_sprite):
        self.label = label
        self.path_to_default_sprite = path_to_default_sprite

    def set_default_label(self):
        self.label.path_to_sprite = self.path_to_default_sprite

    def build_tower(self, x, y):
        if self.gold_manager.get_gold() >= self.cost:
            object = GameObjects.instantiate(self.object)

            object.x = x
            object.y = y

            self.session.add_game_object(object)
            self.gold_manager.change_gold(-self.cost)

    def set_creating_object(self, object, cost):
        self.object = object
        self.cost = cost

    def start_tracking(self):
        self.tracking = True
        self.need_to_create_radius = True
        attack_radius = self.object.get_component('DefenceTowerAttack').get_radius()
        radius_sprite = s.VisibleGameObject('RadiusSprite', self.mouse_x, self.mouse_y, attack_radius, attack_radius, os.path.join('Sprites', 'radius_' + str(attack_radius) + '.png'))
        radius_sprite.add_behaviour(RadiusSprite())
        self.session.add_game_object(radius_sprite)

    def stop_tracking(self):
        self.tracking = False
        self.cost = 0
        self.mouse_x = 0
        self.mouse_y = 0
        self.label = None
        self.path_to_default_sprite = None

    def set_mouse_pos(self, x, y):
        self.mouse_x = x
        self.mouse_y = y


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
        main_tower = session.get_object_by_name('MainTower')
        dist = GameObjects.get_distance_between_game_objects(game_object, main_tower)
        score = int(50 * dist / 900)
        session.get_object_by_name('SceneManager').get_component('RecordsController').change_score(score)

class Manager(i.IBehaviour):
    def __init__(self):
        self.name = 'Manager'
        self.max_count_of_enemys = 0
        self.ai_points = []
        self.spawn_point = None
        self.first_damage_rule = lambda enemy, damage, tower: damage * tower.get_component('DefenceTowerAttack').tower_type
        self.second_damage_rule = lambda enemy, damage, tower: 200 / GameObjects.get_distance_between_game_objects(enemy, tower) * damage

    def start(self, session, game_object):
        self.player_win = False
        self.enemy_id = 0
        self.count_of_enemys = 0
        self.count_of_enemys_on_scene = 0
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
            enemy = self.create_enemy()
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

    def create_enemy(self):
        name = 'Enemy' + str(self.enemy_id)
        if self.enemy_id % 2 == 0:
            enemy = s.Enemy(name, self.spawn_point.x, self.spawn_point.y,
                            64, 64, os.path.join('Sprites', 'enemy_1.png'))
            enemy.get_component('EnemyDamageController').set_rule(self.first_damage_rule)
        else:
            enemy = s.Enemy(name, self.spawn_point.x, self.spawn_point.y,
                            64, 64, os.path.join('Sprites', 'enemy_2.png'))
            enemy.get_component('EnemyDamageController').set_rule(self.second_damage_rule)
        enemy.get_component('ValuableObject').set_cost(10)
        return enemy

    def win_game(self, session):
        session.add_game_object(s.VisibleGameObject('GameWin', 800, 450, 800, 250,
                                                    os.path.join('Sprites', 'game_win_label.png')))
        self.player_win = True

    def get_ai_points(self):
        return self.ai_points

    def add_ai_point(self, point):
        self.ai_points.append(point)

    def set_spawn_point(self, spawn_point):
        self.spawn_point = spawn_point

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
        self.tower_type = 0

    def start(self, session, game_object):
        self.attack = False
        self.animator = game_object.get_component('Animator')

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
            if self.animator.playing:
                self.animator.stop()
                self.animator.to_start()
            return

        self.animator.play()
        damage_controller = target.get_component('EnemyDamageController')
        if damage_controller is not None:
            damage_controller.take_damage(target, self.damage, game_object)

    def set_attack_radius(self, value):
        self.attack_radius = value

    def get_radius(self):
        return self.attack_radius

    def set_damage(self, value):
        self.damage = value

    def set_type(self, tower_type):
        self.tower_type = tower_type

    def set_attack_radius_sprite(self, obj):
        self.attack_radius_sprite = obj


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
        main_tower = session.get_object_by_name('MainTower')
        if main_tower is None or session.get_object_by_name('EnemysManager').get_component('Manager').player_win:
            session.restart_game()
        else:
            window = s.VisibleGameObject('ConfirmWindow', 800, 450, 500, 200,
                                                        os.path.join('Sprites', 'ask.png'))
            confirm_button = s.VisibleGameObject('ConfirmButton', 680, 470, 160, 90,
                                                 os.path.join('Sprites', 'yes'))
            confirm_button.add_behaviour(ConfirmRestartButton())
            denial_button = s.VisibleGameObject('DenialButton', 920, 470, 160, 90,
                                                 os.path.join('Sprites', 'no'))
            denial_bitton_controller = DenialRestartButton()
            denial_bitton_controller.set_window_and_button(window, confirm_button)
            denial_button.add_behaviour(denial_bitton_controller)

            session.add_game_object(window)
            session.add_game_object(confirm_button)
            session.add_game_object(denial_button)

            session.pause()

class ConfirmRestartButton(i.IBehaviour):
    def __init__(self):
        self.name = 'ConfirmRestartButton'

    def on_mouse_down(self, session, game_object):
        session.restart_game()


class DenialRestartButton(i.IBehaviour):
    def __init__(self):
        self.name = 'DenialRestartButton'

    def set_window_and_button(self, window, confirm_button):
        self.window_and_button = [window, confirm_button]

    def on_mouse_down(self, session, game_object):
        for obj in self.window_and_button:
            session.destroy_object(obj)
        session.continue_game()
        session.destroy_object(game_object)


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
        self.game_object = game_object

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

    def to_start(self):
        self.game_object.path_to_sprite = self.pathes_to_sprites[0]
        self.number_of_frame = 0

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


class DefenceTowerUpgrade(i.IBehaviour):
    def __init__(self):
        self.name = 'DefenceTowerUpgrade'
        self.cost = 0
        self.next_tower = None
        self.can_upgrade = False

    def start(self, session, game_object):
        self.gold_manager = session.get_object_by_name('GoldManager') \
            .get_component('GoldManager')

    def upgrade(self, session, game_object):
        session.destroy_object(game_object)
        new_tower = GameObjects.instantiate(self.next_tower)
        new_tower.x = game_object.x
        new_tower.y = game_object.y
        session.add_game_object(new_tower)

    def set_next_tower(self, new_tower):
        self.next_tower = new_tower

    def set_cost(self, cost):
        self.cost = cost

    def activate(self):
        self.can_upgrade = True

    def on_mouse_down(self, session, game_object):
        if not self.can_upgrade or \
                self.gold_manager.get_gold() < self.cost:
            return
        self.upgrade(session, game_object)
        self.gold_manager.change_gold(-self.cost)


class EnemyDamageController(i.IBehaviour):
    def __init__(self):
        self.name = 'EnemyDamageController'
        self.rule = None

    def start(self, session, game_object):
        self.health_system = game_object.get_component('HealthSystem')

    def set_rule(self, rule):
        self.rule = rule

    def take_damage(self, enemy, damage, tower):
        self.health_system.change_health(-self.rule(enemy, damage, tower))


class ReinforcementTower(i.IBehaviour):
    def __init__(self):
        self.name = 'ReinforcementTower'

    def start(self, session, game_object):
        attack_manager = game_object.get_component('DefenceTowerAttack')
        radius = attack_manager.attack_radius
        near_towers = []
        for obj in session.get_objects_by_tag('DefenceTower'):
            if GameObjects.get_distance_between_game_objects(game_object, obj) < radius:
                near_towers.append(obj)
                radius += 50
        for obj in near_towers:
            attack_manager.set_attack_radius(radius)
            obj.get_component('DefenceTowerAttack').set_attack_radius(radius)


class RadiusSprite(i.IBehaviour):
    def __init__(self):
        self.name = 'RadiusSprite'

    def start(self, session, game_object):
        self.manager = session.get_object_by_name('SceneManager').get_component('SceneManager')

    def update(self, session, game_object):
        mouse_pos = session.input.get_mouse_pos_by_object(session, game_object)
        if mouse_pos is None:
            mouse_pos = session.input.get_mouse_pos(session)
            if mouse_pos is None:
                return
            game_object.x = mouse_pos.x()
            game_object.y = mouse_pos.y()
            return

        x = mouse_pos.x()
        y = mouse_pos.y()

        x = int(game_object.x - game_object.width / 2 + x)
        y = int(game_object.y - game_object.height / 2 + y)
        if x < 0 or y < 0:
            x = 0
            y = 0
        game_object.x = x
        game_object.y = y

    def on_mouse_down(self, session, game_object):
        self.manager.build_tower(game_object.x, game_object.y)

    def on_right_mouse_down(self, session, game_object):
        self.manager.set_default_label()
        self.manager.stop_tracking()
        session.destroy_object(game_object)


class RecordsController(i.IBehaviour):
    def __init__(self):
        self.name = 'RecordsController'
        
    def start(self, session, game_object):
        self.main_tower = session.get_object_by_name('MainTower')
        self.enemys_manager = session.get_object_by_name('EnemysManager').get_component('Manager')
        self.active = True
        self.score = 0
        with open('records.txt', 'r') as f:
            records = f.readlines()
        records.sort(key=lambda x: int(x.split('-')[1][0:-1]))
        session.get_object_by_name('RecordsButton').get_component('RecordsTableButton').set_records(records)

    def update(self, session, game_object):
        if self.active and (self.main_tower is None or self.enemys_manager.player_win):
            text, ok = session.read_info_from_user('Record', 'Your score is ' + str(self.score) + '\nEnter your name')
            if ok:
                with open('records.txt', 'a') as f:
                    f.write(text + '-' + str(self.score) + '\n')
            self.active = False

    def change_score(self, delta):
        self.score += delta

class RecordsTableButton(i.IBehaviour):
    def __init__(self):
        self.name = 'RecordsTableButton'
        self.records = []
        self.records_label = []
        self.visible = False

    def on_mouse_down(self, session, game_object):
        if self.visible:
            for lbl in self.records_label:
                session.destroy_object(lbl)
            session.continue_game()
            self.visible = False
        else:
            session.pause()
            i = 1
            for record in self.records:
                if i == 11:
                    break
                lbl = s.TextLabel('RecordLabel' + str(i), 800, 100 + 50 * i, 800, 50, record)
                i += 1
                session.add_game_object(lbl)
                self.records_label.append(lbl)
            self.visible = True

    def set_records(self, records):
        self.records = records


