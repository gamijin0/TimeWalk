import cocos
import pyglet



class StartMenuText(cocos.layer.Layer):
    #开始菜单文字层
    is_event_handler = True

    def __init__(self):
        super(StartMenuText,self).__init__()

        start_game_lable = cocos.text.Label(
            'Start Game',
            font_name='Times New Roman',
            font_size=32,
            anchor_x='center', anchor_y='center'
        )
        start_game_lable.position = 320,240

        exit_lable = cocos.text.Label(
            "Exit",
            font_name='Times New Roman',
            font_size=32,
            anchor_x='center', anchor_y='center'
        )
        exit_lable.position = 420,240

        self.add(start_game_lable)
        self.add(exit_lable)




class GameBackGround(cocos.layer.Layer):
    #游戏背景层
    def __init__(self):
        super(GameBackGround,self).__init__()
        pass




class StartMenu():

    def __init__(self):
        self.start_menu_scene = cocos.scene.Scene(StartMenuText())

    def createStartMenuScene(self):
        return self.start_menu_scene

