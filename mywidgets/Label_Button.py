# coding : utf-8

from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior



class Label_Button(ButtonBehavior, Label):
    def __init__(self, back_color = None, **kwargs):
        super(Label_Button, self).__init__(**kwargs)

    def on_release(self, *args):
        pass
