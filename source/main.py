import pyglet
import cocos

from source.TimeWalk import TimeWalk



if(__name__=="__main__"):


    cocos.director.director.init(fullscreen=True)
    # cocos.director.director.init(fullscreen=False)
    game = TimeWalk()
