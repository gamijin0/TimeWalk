from cocos.layer import Layer
from cocos.sprite import *
from cocos.director import *
import time
from cocos.actions import *
import cocos.collision_model as cm
import cocos.euclid as eu
import os
import pyglet

class Bullet(Sprite):
    #飞船发射的子弹
    def __init__(self,start_x,start_y,speed = 50):

        self.bullet_image = pyglet.image.load(os.path.normpath("../static/jupiter.png"))
        super(Bullet, self).__init__(self.bullet_image)

        self.speed = speed
        self.position = start_x,start_y
        self.scale=0.03

        self.cshape = cm.CircleShape(eu.Vector2(self.x,self.y),5) #子弹碰撞半径

        self.fly()


    def fly(self):
        fly_action = MoveBy([0,self.speed],duration=0.1)
        self.do(Repeat(fly_action))





class ShipSprite(Sprite):
    #玩家控制的飞船
    def __init__(self):

        self.ship_image = pyglet.image.load(os.path.normpath("../static/space-shuttle-1.png"))

        super(ShipSprite,self).__init__(self.ship_image)

        self.scale=0.2 #大小
        self.position=320,240 #初始位置

        self.shake_action = ScaleBy(1.2, duration=0.7) + Reverse(ScaleBy(1.2, duration=0.5))  # 抖动特效
        self.explode_action = ScaleBy(1.1, duration=0.4) + Reverse(ScaleBy(1.2, duration=0.3)) #爆炸特效

        self.do(Repeat(self.shake_action))  #开启抖动

    def explode(self):

        self.do(Repeat(self.explode_action))
        self.delete()

    def shoot(self):
        from random import randint
        bullet  = Bullet(self.x,self.y+50,speed=50+randint(0,30))
        return bullet



class PlayerLayer(Layer):
    is_event_handler = True

    def __init__(self):

        super(PlayerLayer,self).__init__()
        self.shipSprite = ShipSprite()
        self.add(self.shipSprite)


    def on_mouse_motion(self,x,y,dx,dy):
        move_action = MoveTo((x,y),duration=1)
        self.shipSprite.do(move_action)

    def on_mouse_press(self, x, y, buttons, modifiers):
        self.add(self.shipSprite.shoot())