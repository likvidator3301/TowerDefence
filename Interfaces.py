#!/usr/bin/env python3


from abc import ABCMeta, abstractmethod


class IBehaviour:

    def start(self, session, game_object):
        """Start method"""

    def update(self, session, game_object):
        """Called every frame"""

    def on_mouse_down(self, session, game_object):
        """Called when mouse down"""

    def on_right_mouse_down(self, session, game_object):
        """Called when right mouse button down"""

    def destroy(self, session, game_object):
        """Called when object is destroyed"""
