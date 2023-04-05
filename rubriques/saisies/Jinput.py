# coding : utf-8

"""
    OGFight - Simulateur de combat pour Ogame FDV
    Copyright (C) 2023  HattaTea

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

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
