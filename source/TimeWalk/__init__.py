from cocos.scene import Scene
from cocos.director import director
from cocos.collision_model import CollisionManager
from .layer.startMune import StartMenuLayer
from .layer.palyer import PlayerLayer
import pyglet
import cocos
from  .layer.background import BackGround
from .mouse import MouseDisplay


class TimeWalk():
    def __init__(self):
        self.score = 0
        cocos.director.director.window.set_mouse_visible(True)
        director.run(Scene(BackGround(),StartMenuLayer()))
