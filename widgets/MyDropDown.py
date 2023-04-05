# coding : utf-8

from kivy.uix.dropdown import DropDown
from kivy.graphics import Color, Rectangle


class MyDropDown(DropDown):

    def __init__(self, **kwargs):
        super(MyDropDown, self).__init__(**kwargs)
        self.spacing = [0, 0]
        with self.canvas.before:
            Color(0, 0, 0, 1)
            self.rect = Rectangle(pos = self.pos, size = self.size)
        self.bind(size = self._update_rect, pos = self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
