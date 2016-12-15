from cocos.scene import Scene
from cocos.director import director
from cocos.collision_model import CollisionManager
from .layer.startMune import StartMenuLayer
from .layer.palyer import PlayerLayer
import pyglet
from .mouse import MouseDisplay

collisionManager = CollisionManager()

class TimeWalk():
    def __init__(self):
        self.collisionManager = collisionManager

        # director.run(scene=Scene(StartMenuLayer()))
        director.run(scene=Scene(PlayerLayer()))

