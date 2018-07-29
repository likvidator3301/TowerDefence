#!/usr/bin/env python3

import pytest
import SecondOrderGameObject as s
from CrotysEngine import GameObjects


class TestGameInstantiate:

    def test_instantiate(self):
        obj = s.AIPoint('AIPoint', 100, 100, 50, 50)
        obj2 = GameObjects.instantiate(obj)
        assert obj2.name == 'AIPointClone1'
        assert obj.tag == obj2.tag
        assert len(obj.behaviour) == len(obj2.behaviour)
