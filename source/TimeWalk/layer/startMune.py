from cocos.layer import Layer
from cocos.text import  Label
from cocos.menu import *
import pyglet
from cocos.actions import *
from cocos.director import director
from cocos.scene import *
from .palyer import PlayerLayer
from .background import BackGround


class StartMenuLayer(Menu):
    def __init__( self ):
        super( StartMenuLayer, self ).__init__("Time Walker" )

        self.menu_valign = CENTER
        self.menu_halign = CENTER



        # then add the items
        items = [
            (MenuItem('Start Fighting', self.go_next_scene)),
            ( MenuItem('Exit ', exit) ),
        ]

        self.create_menu( items, selected_effect=shake()+zoom_in(),
                          unselected_effect=zoom_out())
        self.player = pyglet.media.Player()
        start_background_sound = pyglet.media.load("../static/sounds/start_background.wav")
        self.player.queue(start_background_sound)
        self.player.play()

    def on_quit(self):
        self.player.delete()
        director.replace(Scene(BackGround(),PlayerLayer(next_scene=Scene(BackGround(),StartMenuLayer()))))

    def go_next_scene(self):
        self.do(FadeOutTRTiles(grid=(36,22), duration=1)+CallFunc(self.on_quit))


