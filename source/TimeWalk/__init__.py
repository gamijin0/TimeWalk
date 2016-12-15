from cocos.scene import Scene
from cocos.director import director
from .layer.startMune import StartMenuLayer
from .layer.palyer import PlayerLayer
import pyglet
from .mouse import MouseDisplay

class TimeWalk():
    def __init__(self):
        # director.run(scene=Scene(StartMenuLayer()))
        director.run(scene=Scene(PlayerLayer()))
