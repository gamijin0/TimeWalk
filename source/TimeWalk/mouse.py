import cocos
class MouseDisplay(cocos.layer.Layer):

    is_event_handler = True     #: enable director.window events

    def __init__(self):
        super( MouseDisplay, self ).__init__()

        self.posx = 100
        self.posy = 240
        self.text = cocos.text.Label('No mouse events yet', font_size=18, x=self.posx, y=self.posy )
        self.add( self.text )

    def update_text (self, x, y):
        text = 'Mouse @ %d,%d' % (x, y)
        self.text.element.text = text
        self.text.element.x = self.posx
        self.text.element.y = self.posy

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        """Called when the mouse moves over the app window with no button pressed

        (x, y) are the physical coordinates of the mouse
        (dx, dy) is the distance vector covered by the mouse pointer since the
          last call.
        """
        print(dx,dy)
        self.update_text(dx, dy)