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

class EnemySprite(Sprite):
    #敌人
    def __init__(self,x,y):
        enemy_file_list = [
            "space-ship","space-ship","rocket-ship-2","space-shuttle-2","ufo"
        ]
        from random import randint

        self.ship_image = pyglet.image.load(os.path.normpath("../static/%s.png" % (enemy_file_list[randint(0,len(enemy_file_list)-1)]) ))
        super(EnemySprite, self).__init__(self.ship_image)
        self.scale=0.2 #大小
        self.do(Rotate(180,duration=0))

        from random import randint
        self.position=x,y #初始位置
        self.shake_action = ScaleBy(1.1, duration=0.7) + Reverse(ScaleBy(1.1, duration=0.5))  # 抖动特效
        self.do(Repeat(self.shake_action))  #开启抖动



    def fly(self,target,speed=60):
        import math
        dx = target.x-self.x
        dy = target.y-self.y
        hy=math.hypot(dx, dy)

        fly_action = MoveBy([dx*1.0*speed/hy,dy*1.0*speed/hy],duration=0.1)

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
    bullet_set = list()
    enemy_set = list()
    time = 0


    def __init__(self):

        super(PlayerLayer,self).__init__()
        self.shipSprite = ShipSprite()
        self.add(self.shipSprite)

        self.schedule(self.check_hit)



    def on_mouse_motion(self,x,y,dx,dy):
        move_action = MoveTo((x,y),duration=1)
        self.shipSprite.do(move_action)

    def on_mouse_press(self, x, y, buttons, modifiers):
        one_bullet = self.shipSprite.shoot()
        self.add(one_bullet)
        self.bullet_set.append(one_bullet)

    def generateEnemy(self):
        from random import randint
        one_enemy = EnemySprite(randint(200,1200),1300)
        self.add(one_enemy)
        self.enemy_set.append(one_enemy)
        one_enemy.fly(self.shipSprite)

    def deleteEnemy(self,en):
        self.remove(en)
        self.enemy_set.remove(en)
        en.delete()

    def deleteBullet(self,bu):
        self.remove(bu)
        self.bullet_set.remove(bu)
        bu.delete()

    #用于检测撞击
    def check_hit(self,*args,**kwargs):
        self.time +=1
        if(self.time>10):
            self.generateEnemy()
            self.time=0

        for b in self.bullet_set:
            if(b.y>1700):
                self.deleteBullet(b)

            for en in self.enemy_set:
                if(((b.x-en.x)**2+(b.y-en.y)**2)<400):
                    #击中
                    self.deleteBullet(b)
                    self.deleteEnemy(en)

        for en in self.enemy_set:
            if(en.y<-100):
                self.deleteEnemy(en)