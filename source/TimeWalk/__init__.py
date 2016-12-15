import cocos
import pyglet
from .mouse import MouseDisplay
from ..config import STATIC_RESOURCES_PATH
from .scene.startMenu import StartMenu

class TimeWalk():
    def __init__(self):
        self.start_menu = StartMenu()
        cocos.director.director.run(self.start_menu.createStartMenuScene())

