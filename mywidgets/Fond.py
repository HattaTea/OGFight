# coding : utf-8

from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image

from kivy.graphics import Rectangle


class Fond(GridLayout):

    def __init__(self, **kwargs):
        super(Fond, self).__init__(**kwargs)
        self.rect = Rectangle(pos = self.pos, size = self.size)

        self.bind(size = self._update_rect, pos = self._update_rect)

        with self.canvas.before:
            self.image = Image(source = "Fond_espace.jpg", allow_stretch  = True, keep_ratio = False)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

        try:
            self.image.size = self.parent.size
        except:
            pass
