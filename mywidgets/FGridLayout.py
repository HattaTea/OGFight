# coding : utf-8

from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle



class FGridLayout(GridLayout):
    def __init__(self, **kwargs):
        super(FGridLayout, self).__init__(**kwargs)
        with self.canvas.before:
            Color(0, 0, 0, 0.8)
            self.rect = Rectangle(pos = self.pos, size = self.size)
        self.bind(size = self._update_rect, pos = self._update_rect)
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
