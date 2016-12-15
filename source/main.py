import pyglet
import cocos

from source.TimeWalk import TimeWalk
from source.TimeWalk.mouse import MouseDisplay


if(__name__=="__main__"):


    cocos.director.director.init(fullscreen=True)
    cocos.director.director.window.set_mouse_visible(False)
    game = TimeWalk()
