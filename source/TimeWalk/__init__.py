import cocos
import pyglet
from ..config import STATIC_RESOURCES_PATH

class TimeWalk(cocos.layer.Layer):

    def __init__(self):
        super(TimeWalk,self).__init__()

        label = cocos.text.Label(
            'TimeWalk',
            font_name='Times New Roman',
            font_size=32,
            anchor_x='center', anchor_y='center'
        )
        label.position = 780, 840
        self.add(label)

        doge = pyglet.image.load(STATIC_RESOURCES_PATH+"doge.png")

        sprite = cocos.sprite.Sprite(doge)
        sprite.position  = 620,240
        sprite.scale = 1

        self.add(sprite)