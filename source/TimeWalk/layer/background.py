import cocos
from cocos.layer import Layer
from cocos.sprite import Sprite
from cocos.director import  director
from random import randint
import pyglet
from cocos.actions import *
import os


class MapItemSprite(Sprite):
    def __init__(self,name:str,fartherMap,distance=None):
        self.fartherMap = fartherMap
        self.itemImage = pyglet.image.load(os.path.normpath("../static/%s.png" % (name)))
        super(MapItemSprite,self).__init__(self.itemImage)
        if(distance is not None):
            self.distance = distance
            self.scale = 0.03 *randint(2,6)
        else:
            self.distance = randint(7,17)
            self.scale = 0.03 * (self.distance)
        self.position = (randint(int(director.window.width*0.01),int(director.window.width*0.9)),director.window.height+50)


class BackGround(Layer):

    is_event_handler = True

    def __init__(self):
        self.time = 0
        super(BackGround,self).__init__()
        self.itemNames = ["destroyed-planet","galaxy","jupiter","mars",
                         "moon","planet","planet-earth","uranus","saturn"]

        self.mapItems = list()
        self.schedule(self.check)

        for i in range(randint(5,8)):
            self.addMapItems(
                randint(0,len(self.itemNames)),
                position=(randint(int(director.window.width*0.1),int(director.window.width*0.9)),randint(int(director.window.height*0.1),int(director.window.height*0.9))),
                distance=0
            )

        for i in range(randint(1,3)):
            self.addMapItems(
                randint(0,len(self.itemNames)),
                position=(randint(int(director.window.width*0.1),int(director.window.width*0.9)),randint(int(director.window.height*0.1),int(director.window.height*0.9))),
                distance=None
            )



    def rollMap(self,step=10,dx=0,dy=0):
        #卷动地图
        for item in self.mapItems:
            if(item.distance != 0 ):
                if(step!=0):
                    item.do(MoveTo((item.x,item.y-step-0.2*item.distance),0.1))

    def addMapItems(self,num,position=None,distance = None):
        #向背景中添加物体
        if(num>=0 and num <len(self.itemNames)):
            if(distance is not None):
                itemSprite = MapItemSprite(name=self.itemNames[num],fartherMap=self,distance=distance)
            else:
                itemSprite = MapItemSprite(name=self.itemNames[num], fartherMap=self)
            if(position is not None):
                itemSprite.position = position
            self.mapItems.append(itemSprite)
            self.add(itemSprite)

    def deleteItems(self,item:MapItemSprite):
        self.mapItems.remove(item)
        self.remove(item)
        item.delete()

    def on_mouse_motion(self,x,y,dx,dy):
        self.rollMap(step=0,dx=dx,dy=dy)

    def check(self,*args,**kwargs):
        self.time+=1
        #每帧都调用
        for item in self.mapItems:
            if(item.y<0):
                self.deleteItems(item)

        if(self.time%(500)==0):
            self.addMapItems(randint(0,len(self.itemNames)))

        self.rollMap(step=2)