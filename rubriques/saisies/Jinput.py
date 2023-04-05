# coding : utf-8

from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from kivy.properties import StringProperty

from .Espio_Input import Espio_Input


class Jinput(GridLayout):

    pseudo = StringProperty("")

    def __init__(self, num, **kwargs):
        super(Jinput, self).__init__(*kwargs)

        self.cols = 1
        self.size_hint = (1, None)
        self.height = 120

        self.pseudo = str(num)

        self.fname = GridLayout(cols = 2, size_hint = (1, None), height = 30)
        self.lpseu = Label(text = "Pseudo : ")
        self.epseu = TextInput(text = str(num))
        self.epseu.bind(text = self.setter("pseudo"))
        self.fname.add_widget(self.lpseu)
        self.fname.add_widget(self.epseu)
        self.add_widget(self.fname)

        self.espio = Espio_Input()
        self.add_widget(self.espio)
