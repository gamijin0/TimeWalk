import cocos

class TimeWalk(cocos.layer.Layer):

    def __init__(self):
        super(TimeWalk,self).__init__()

        label = cocos.text.Label(
            'TimeWalk',
            font_name='Times New Roman',
            font_size=32,
            anchor_x='center', anchor_y='center'
        )
        label.position = 320, 240
        self.add(label)