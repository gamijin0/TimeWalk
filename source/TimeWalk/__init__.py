from cocos.scene import Scene
from cocos.director import director
from cocos.collision_model import CollisionManager
from .layer.startMune import StartMenuLayer
from .layer.palyer import PlayerLayer
import pyglet
import cocos
from  .layer.background import BackGround
from .mouse import MouseDisplay

collisionManager = CollisionManager()

class TimeWalk():
    def __init__(self):
        self.collisionManager = collisionManager

        backGroungLayer = BackGround()
        director.run(scene=Scene(backGroungLayer,StartMenuLayer()))

        from source.TimeWalk.mouse import MouseDisplay
        cocos.director.director.window.set_mouse_visible(False)
        director.run(scene=Scene(backGroungLayer,PlayerLayer()))

