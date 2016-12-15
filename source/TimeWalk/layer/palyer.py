from cocos.layer import Layer
from cocos.sprite import *
from cocos.director import *
from cocos.actions import *
import pyglet

class PlayerLayer(Layer):
    is_event_handler = True

    def __init__(self):

        super(PlayerLayer,self).__init__()
        rocket = pyglet.image.load(pyglet.resource.get_script_home()+'\..\static\\rocket-ship-2.png')
        self.sprite=Sprite(rocket)
        self.sprite.scale=0.1
        self.sprite.position=320,240

        self.add(self.sprite)

    def on_mouse_click(self, x, y, buttons, modifiers):

        follow_action = Delay(0.1)+MoveTo([x,y],1)

        self.sprite.do(action=follow_action)
