import pyglet
import cocos
from source.TimeWalk import TimeWalk
from source.TimeWalk.mouse import MouseDisplay


if(__name__=="__main__"):


    cocos.director.director.init(fullscreen=False)
    game = TimeWalk()
