from cocos.layer import Layer
from cocos.text import  Label

class StartMenuLayer(Layer):

    is_event_handler = True

    def __init__(self):
        super(StartMenuLayer,self).__init__()

        start_game_lable = Label(
            'Start Game',
            font_name='Times New Roman',
            font_size=32,
            anchor_x='center', anchor_y='center'
        )
        start_game_lable.position = 420,340

        exit_lable = Label(
            "Exit",
            font_name='Times New Roman',
            font_size=32,
            anchor_x='center', anchor_y='center'
        )
        exit_lable.position = 420,240

        self.add(start_game_lable)
        self.add(exit_lable)