#!/usr/bin/env python3

import math
import SecondOrderGameObject as s

NUMBER_OF_CLONE = 0


def get_distance_between_game_objects(first, second):
    dx = math.fabs(first.x - second.x)
    dy = math.fabs(first.y - second.y)

    return math.sqrt(dx * dx + dy * dy)


def instantiate(object):
    global NUMBER_OF_CLONE
    NUMBER_OF_CLONE += 1
    name = object.name + 'Clone' + str(NUMBER_OF_CLONE)
    new_object = s.GameObject(name, object.x, object.y,
                              object.width, object.height)
    if object.visible:
        new_object.visible = True
        new_object.set_path_to_sprite(object.path_to_sprite)
    new_object.set_tag(object.tag)
    for nameB in object.behaviour:
        beh = object.get_component(nameB).__class__
        new_object.add_behaviour(beh())
    return new_object
