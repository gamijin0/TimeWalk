import cocos
from cocos.layer import Layer
from cocos.sprite import *
from cocos.director import *
import time
from cocos.actions import *
import cocos.collision_model as cm
import cocos.euclid as eu
import os
import pyglet



# 飞船发射的子弹
class Bullet(Sprite):
    def __init__(self,start_x,start_y,speed = 50,team = 1):
        self.team = team #队，1:友方 2:敌方

        if(self.team==1):
            self.bullet_image = pyglet.image.load(os.path.normpath("../static/jupiter.png"))
        if(self.team==2):
            self.bullet_image = pyglet.image.load(os.path.normpath("../static/sun.png"))
        super(Bullet, self).__init__(self.bullet_image)

        self.speed = speed
        self.position = start_x,start_y
        self.scale=0.03

        self.fly()


    def fly(self):
        fly_action = MoveBy([0,self.speed],duration=0.1)
        self.do(Repeat(fly_action))

    #判断是否击中一个目标
    def hit(self,taraget,length=400):
        return (((self.x-taraget.x)**2+(self.y-taraget.y)**2)<length) and (self.team!=taraget.team)


#敌人
class EnemySprite(Sprite):
    #敌人
    def __init__(self,x,y):
        enemy_file_list = [
            "space-ship","space-ship","rocket-ship-2","space-shuttle-2","ufo"
        ]
        from random import randint

        self.team = 2
        self.ship_image = pyglet.image.load(os.path.normpath("../static/%s.png" % (enemy_file_list[randint(0,len(enemy_file_list)-1)]) ))
        super(EnemySprite, self).__init__(self.ship_image)
        self.scale=0.2 #大小
        self.do(Rotate(180,duration=0))

        self.position=x,y #初始位置
        self.shake_action = ScaleBy(1.1, duration=0.7) + Reverse(ScaleBy(1.1, duration=0.5))  # 抖动特效
        self.do(Repeat(self.shake_action))  #开启抖动
        self.actionValue = 0

    def shoot(self):
        from random import randint
        bullet  = Bullet(self.x,self.y-50,speed=-30-randint(0,20),team=2)
        return bullet

    def fly(self,target,speed=60):
        import math
        dx = target.x-self.x
        dy = target.y-self.y
        hy=math.hypot(dx, dy)

        fly_action = MoveBy([dx*1.0*speed/hy,dy*1.0*speed/hy],duration=0.1)

        self.do(Repeat(fly_action))


# 玩家控制的飞船
class ShipSprite(Sprite):
    def __init__(self):

        self.team = 1
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
        bullet  = Bullet(self.x,self.y+50,speed=50+randint(0,30),team=1)
        return bullet


#血条
class BloodLine(Sprite):
    def __init__(self):
        self.bloodPercent = 100
        self.bloodLine_image = pyglet.image.load(os.path.normpath("../static/bloodline.png"))
        super(BloodLine,self).__init__(self.bloodLine_image)
        self.anchor_x = 0

        self.position = 1400,50
        self.scale_x = 1.8
        self.scale_y = 0.8

    def lossBlood(self,d_bloodPercent):
        self.bloodPercent-=d_bloodPercent
        if(self.bloodPercent>0 and d_bloodPercent>0):
            # loss_blood_action = ScaleBy(float((self.bloodPercent-d_bloodPercent))/self.bloodPercent,0.1)
            self.scale_x *= float((self.bloodPercent-d_bloodPercent)/self.bloodPercent)
            # self.do(loss_blood_action)


#游戏控制
class PlayerLayer(Layer):

    is_event_handler = True
    bullet_set = list()
    enemy_set = list()
    time = 0


    def __init__(self):

        super(PlayerLayer,self).__init__()
        self.shipSprite = ShipSprite()
        self.add(self.shipSprite)

        self.bloodline = BloodLine()
        self.add(self.bloodline)


        self.schedule(self.check_hit)

        #分数显示
        self.score = 0
        self.scoreLabel = cocos.text.Label(
            'Score: \t0 ',
            font_name='Times New Roman',
            font_size=32,
            anchor_x='center', anchor_y='center'
        )
        self.scoreLabel.position = 1700,100
        self.add(self.scoreLabel)

    #鼠标移动时触发
    def on_mouse_motion(self,x,y,dx,dy):
        move_action = MoveTo((x,y),duration=1)
        self.shipSprite.do(move_action)

    #鼠标按下时触发
    def on_mouse_press(self, x, y, buttons, modifiers):
        one_bullet = self.shipSprite.shoot()
        self.add(one_bullet)
        self.bullet_set.append(one_bullet)

    #产生敌人
    def generateEnemy(self):
        from random import randint
        one_enemy = EnemySprite(randint(200,1200),1300)
        self.add(one_enemy)
        self.enemy_set.append(one_enemy)
        one_enemy.fly(self.shipSprite)

    #删除敌人
    def deleteEnemy(self,en):
        self.remove(en)
        self.enemy_set.remove(en)
        en.delete()
    #删除子弹
    def deleteBullet(self,bu):
        self.remove(bu)
        self.bullet_set.remove(bu)
        bu.delete()

    def Scored(self,value):
        if(value>0):
            self.score+=value
            self.scoreLabel.element.text = "Score: \t%d" % (self.score)

    #用于检测撞击
    def check_hit(self,*args,**kwargs):
        self.time +=1
        if(self.time%20==0):
            self.generateEnemy()

        for b in self.bullet_set:
            if(b.y>1700 or b.y <0):
                self.deleteBullet(b)

            for en in self.enemy_set:

                if(b.hit(en)):
                    self.deleteBullet(b)
                    #击中
                    self.Scored(20)
                    self.deleteEnemy(en)

            if(b.hit(self.shipSprite,length=800)):
                self.shipSprite.do(Blink(1,0.1))
                self.deleteBullet(b)
                self.bloodline.lossBlood(10)


        for en in self.enemy_set:
            en.actionValue+=1
            if(en.actionValue%35==0):
                one_bullet = en.shoot()
                self.add(one_bullet)
                self.bullet_set.append(one_bullet)

            if(en.y<-10):
                self.deleteEnemy(en)
