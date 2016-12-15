import cocos
import pyglet
from .mouse import MouseDisplay
from ..config import STATIC_RESOURCES_PATH
from .scene.startMenu import StartMenu

class TimeWalk():
    start_menu = StartMenu()
    def __init__(self):
        cocos.director.director.run(self.start_menu.createStartMenuScene())

