import cocos
from cocos.layer import Layer,ColorLayer
from cocos.sprite import *
from cocos.director import *
import time
from cocos.actions import *
from cocos.particle_systems import *
import cocos.collision_model as cm
import cocos.euclid as eu
import os
import pyglet
from cocos.scene import Scene
from .background import BackGround

# 飞船发射的子弹
class Bullet(Sprite):
    def __init__(self,start_x,start_y,speed=50,team = 1):
        self.team = team #队，1:友方 2:敌方

        if(self.team==1):
            self.bullet_image = pyglet.image.load(os.path.normpath("../static/jupiter.png"))
        if(self.team==2):
            self.bullet_image = pyglet.image.load(os.path.normpath("../static/mars.png"))
        super(Bullet, self).__init__(self.bullet_image)

        self.speed = speed
        self.position = start_x,start_y
        self.scale=0.03

        self.fly(self.speed)


    def fly(self,speed):
        self.speed = speed
        fly_action = MoveBy([0,self.speed],duration=0.1)
        self.do(Repeat(fly_action))

    #判断是否击中一个目标
    def hit(self,taraget,length=400):
        return (((self.x-taraget.x)**2+(self.y-taraget.y)**2)<length) and (self.team!=taraget.team)


#敌人
class EnemySprite(Sprite):
    enemy_file_list = [
        "space-ship", "space-ship", "rocket-ship-2", "space-shuttle-2", "ufo", "space-station", "space-station-1"
    ]
    #敌人
    def __init__(self,x,y,type:int):

        self.team = 2
        self.speed = 60
        self.ship_image = pyglet.image.load(os.path.normpath("../static/%s.png" % (self.enemy_file_list[type%len(self.enemy_file_list)]) ))
        super(EnemySprite, self).__init__(self.ship_image)
        self.scale=0.14 #大小
        self.do(Rotate(180,duration=0))

        self.position=x,y #初始位置
        self.birth_position = self.position #记录下出生位置
        self.shake_action = ScaleBy(1.1, duration=0.7) + Reverse(ScaleBy(1.1, duration=0.5))  # 抖动特效
        self.do(Repeat(self.shake_action))  #开启抖动
        self.actionValue = 0

    def shoot(self,speed=0):
        from random import randint
        if(speed==0):
            bullet = Bullet(self.x, self.y - 50, speed=-60 - randint(0, 20), team=2)
        else:
            bullet = Bullet(self.x, self.y - 50, speed=speed, team=2)
        return bullet

    def fly(self,target,speed=60):

        self.target = target
        self.speed = speed
        import math
        if (isinstance(target, Sprite)):
            dx = self.target.x-self.x
            dy = self.target.y-self.y
        else:
            dx = self.target[0] - self.birth_position[0]
            dy = self.target[1] - self.birth_position[1]

        hy=math.hypot(dx, dy)

        self.fly_action = MoveBy([dx*1.0*self.speed/hy,dy*1.0*self.speed/hy],duration=0.1)

        self.do(Repeat(self.fly_action))


# 玩家控制的飞船
class ShipSprite(Sprite):
    def __init__(self):

        self.team = 1
        self.ship_image = pyglet.image.load(os.path.normpath("../static/space-shuttle-1.png"))

        super(ShipSprite,self).__init__(self.ship_image)
        self.tailFire = Fire()
        self.tailFire.size = 40

        self.scale=0.2 #大小
        self.position=320,240 #初始位置
        self.tailFire.position=0,-300
        self.tailFire.angle= 270
        self.add(self.tailFire)
        self.shake_action = ScaleBy(1.2, duration=0.7) + Reverse(ScaleBy(1.2, duration=0.5))  # 抖动特效

        self.do(Repeat(self.shake_action))  #开启抖动



    def explode(self):
        explode_sounds = pyglet.media.load("../static/sounds/explode.wav")
        self.do(
            MoveTo((director.window.width/2,director.window.height/2),duration = 1.8)
            +CallFunc(explode_sounds.play)
            +Shaky3D(grid=(36,22), duration=1)
            +StopGrid()
        )

    def shoot(self,speed = 0):
        shoot_sounds = pyglet.media.load("../static/sounds/shoot.wav")
        shoot_sounds.play()
        from random import randint
        if(speed==0):
            bullet  = Bullet(self.x,self.y+50,speed=50+randint(0,30),team=1)
        else:
            bullet = Bullet(self.x, self.y + 50, speed=speed, team=1)
        return bullet



#血条
class BloodLine(Layer):
    def __init__(self):


        #===================self==================================
        super(BloodLine,self).__init__()
        self.bloodPercent = 100
        self.bloodLine_image = pyglet.image.load(os.path.normpath("../static/bloodline.png"))

        #===================bg==================================
        self.bloodLine_bg = Sprite(self.bloodLine_image,anchor=(0,self.bloodLine_image.height/2))
        self.bloodLine_bg.position = int(director.window.width * 0.3), int(director.window.height * 0.05)
        # self.bloodLine_bg.image_anchor_x = self.bloodLine_bg.position[0]
        self.bloodLine_bg.color = (153, 56, 100)
        self.bloodLine_bg.scale_x = 1.8
        self.bloodLine_bg.scale_y = 0.8
        self.add(self.bloodLine_bg)

        #===================front==================================
        self.bloodLine = Sprite(self.bloodLine_image,anchor=(0,self.bloodLine_image.height/2))
        self.bloodLine.position = self.bloodLine_bg.position
        self.bloodLine.scale_x = 1.8
        self.bloodLine.scale_y = 0.8
        self.add(self.bloodLine)




    def lossBlood(self,d_bloodPercent):

        loss_blood_sound  = pyglet.media.load("../static/sounds/loss_blood.wav")
        loss_blood_sound.play()

        self.bloodPercent-=d_bloodPercent
        if(self.bloodPercent>0 and d_bloodPercent>0):
            self.bloodLine.do(Scale_X_To(1.8/100.0*self.bloodPercent,duration = 1))




class PlayerLayer(Layer):

    is_event_handler = True
    bullet_set = list()
    enemy_set = list()
    time = 0



    def __init__(self,next_scene):
        # print("Creaete one player layer")
        cocos.director.director.window.set_mouse_visible(False)
        super(PlayerLayer,self).__init__()
        self.next_scene = next_scene
        self.shipSprite = ShipSprite()
        self.add(self.shipSprite)

        self.bloodline = BloodLine()
        self.add(self.bloodline)

        self.time_speed = 10 #时间流速

        self.schedule(self.check_hit) #每一帧都检测

        #分数显示
        self.score = 0
        self.scoreLabel = cocos.text.Label(
            'Score: \t0 ',
            font_name='Times New Roman',
            font_size=32,
            anchor_x='center', anchor_y='center'
        )
        self.scoreLabel.position = int(director.window.width*0.9),int(director.window.height*0.1)


        self.add(self.scoreLabel)

        self.wave = 0  #当前关卡数

        self.waveLabel = cocos.text.Label(
            'Wave: \t0 ',
            font_name='Times New Roman',
            font_size=32,
            anchor_x='center', anchor_y='center'
        )
        self.waveLabel.position = int(director.window.width * 0.9), int(director.window.height * 0.8)

        self.add(self.waveLabel)
        self.player = pyglet.media.Player()

    #鼠标移动时触发
    def on_mouse_motion(self,x,y,dx,dy):
        move_action = MoveTo((x,y),duration=1+0.5/(self.time_speed))

        self.shipSprite.do(move_action)

    #鼠标按下时触发
    def on_mouse_press(self, x, y, buttons, modifiers):
        if(buttons==1):
            #左键
            if(self.time_speed>1):
                one_bullet = self.shipSprite.shoot()
            else:
                one_bullet = self.shipSprite.shoot(speed=50*self.time_speed)
            self.add(one_bullet)
            self.bullet_set.append(one_bullet)
        if(buttons==4 ):
            #右键

            # self.player.queue(time_slow_sound)
            # self.player.

            time_slow = pyglet.media.load("../static/sounds/time_slow_1.wav")
            time_slow.play()

            if(self.time_speed>1):
                self.do(Waves( waves=1, hsin=True, vsin=True,
                          grid=(36,20), duration=1))
            else:
                self.do(Waves( waves=1, hsin=True, vsin=True,grid=(36,20), duration=1)+StopGrid())

            self.time_speed = 1.0/self.time_speed

            for en in self.enemy_set:
                en.fly(en.target,en.speed*self.time_speed)
            for bu in self.bullet_set:
                bu.fly(bu.speed*self.time_speed)

    #产生敌人
    def generateEnemy(self):
        from random import randint
        one_enemy = EnemySprite(randint(200,1200),1300,type=self.wave%len(EnemySprite.enemy_file_list))
        self.add(one_enemy)
        self.enemy_set.append(one_enemy)
        one_enemy.fly(
            (randint(int(director.window.width*0.2),int(director.window.width*0.7)),0),
            self.enemy_set[0].speed
        )

    #删除敌人
    def deleteEnemy(self,en):
        self.enemy_set.remove(en)
        self.remove(en)
    #删除子弹
    def deleteBullet(self,bu):
        self.bullet_set.remove(bu)
        self.remove(bu)

    #得分
    def Scored(self,value):
        if(value>0):
            self.score+=value
            self.scoreLabel.element.text = "Score: \t%d" % (self.score)
            self.waveLabel.element.text = "Wave: \t%d" % (self.wave-1)


    #用于检测撞击
    def check_hit(self,*args,**kwargs):

        self.time +=1

        self.wave = int(self.score/100) + 1

        #定时产生敌人
        if (self.time_speed < 1):
            enemy_generate_frequence = int(10/ self.time_speed)
        else:
            enemy_generate_frequence = 20
        if(self.time%(enemy_generate_frequence)==0):
            self.generateEnemy()

        for b in self.bullet_set:
            for en in self.enemy_set:
            #检查是否击中敌人
                if(b.hit(en)):
                    self.deleteBullet(b)
                    self.Scored(20)
                    self.deleteEnemy(en)

            #检查自己是否被击中
            if(b.hit(self.shipSprite,length=800)):
                self.shipSprite.do(Shaky3D(grid=(36,22), duration=0.2)+StopGrid())
                self.deleteBullet(b)
                self.bloodline.lossBlood(30)
                if(self.bloodline.bloodPercent<=0):
                    director.window.remove_handlers(self) #取消鼠标控制
                    self.on_quit()
            #删除无效子弹
            if(b.y>1700 or b.y <0):
                self.deleteBullet(b)

        for en in self.enemy_set:
            from random import randint
            en.actionValue+=randint(1,4)

            enemy_shoot_frequence = 50.0
            if(self.time_speed<1):
                enemy_shoot_frequence =  int(enemy_shoot_frequence/self.time_speed)
            else:
                pass

            if(en.actionValue%(enemy_shoot_frequence)==0):
                #敌人间歇性发射子弹
                one_bullet = en.shoot()
                if(self.time_speed<1):
                    one_bullet.fly(one_bullet.speed*self.time_speed)
                self.add(one_bullet)
                self.bullet_set.append(one_bullet)

            #删除无效敌人
            if(en.y<-10):
                self.deleteEnemy(en)

    def go_next_scene(self):
        director.window.remove_handlers(self)  # 取消鼠标控制
        for c in self.get_children():
            self.remove(c)
        cocos.director.director.window.set_mouse_visible(True)
        director.replace(self.next_scene)

    def on_quit(self):
        director.window.remove_handlers(self)  # 取消鼠标控制
        self.pause_scheduler()
        self.bullet_set.clear()
        self.enemy_set.clear()

        self.shipSprite.explode()
        director.scene.do(Shaky3D(grid=(24,16), duration=3)+FadeOutTRTiles(grid=(24,16), duration=3)+CallFunc(self.go_next_scene))

class Scale_X_To(IntervalAction):
    """Scales a `CocosNode` object to a zoom factor by modifying it's scale attribute.

    Example::

        # scales the sprite to 5x in 2 seconds
        action = ScaleTo(5, 2)
        sprite.do(action)
    """
    def init(self, scale_x, duration=5):
        """Init method.

        :Parameters:
            `scale` : float
                scale factor
            `duration` : float
                Duration time in seconds
        """
        self.end_scale_x = scale_x
        self.duration = duration

    def start(self):
        self.start_scale_x = self.target.scale_x
        self.delta = self.end_scale_x - self.start_scale_x

    def update(self, t):
        self.target.scale_x = self.start_scale_x + self.delta*t
