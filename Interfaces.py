#!/usr/bin/env python3


from abc import ABCMeta, abstractmethod, abstractproperty


class IBehaviour:
    __metaclass__ = ABCMeta

    @abstractmethod
    def start(self, session, game_object):
        """Start method"""

    @abstractmethod
    def update(self, session, game_object):
        """Called every frame"""

    @abstractmethod
    def on_mouse_down(self, session, game_object):
        """Called when mouse down"""

    def destroy(self, session, game_object):
        """Called when object is destroyed"""
        session.destroy_object(game_object)
