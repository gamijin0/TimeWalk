from cocos.layer import Layer
from cocos.sprite import Sprite
import pyglet

class PlayerLayer(Layer):
    is_event_handler = True
    def __init__(self):
        super(PlayerLayer,self).__init__()
        rocket = pyglet.image.load(pyglet.resource.get_script_home()+'\..\static\doge.png')
        self.sprite=Sprite(rocket)
        self.sprite.position=320,240
        self.add(self.sprite)
