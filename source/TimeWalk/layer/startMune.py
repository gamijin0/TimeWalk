from cocos.layer import Layer
from cocos.text import  Label
from cocos.menu import *
import pyglet
from cocos.director import director


class StartMenuLayer(Menu):
    def __init__( self ):
        super( StartMenuLayer, self ).__init__("Timer Walker" )

        self.menu_valign = CENTER
        self.menu_halign = CENTER



        # then add the items
        items = [
            (MenuItem('Start Fighting', self.on_quit)),
            ( MenuItem('Exit ', exit) ),
        ]

        self.create_menu( items, selected_effect=shake()+zoom_in(),
                          unselected_effect=zoom_out())

    def on_quit( self ):
        pyglet.app.exit()
