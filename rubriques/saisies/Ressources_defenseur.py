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


class Ressources_defenseur(GridLayout):

    metal = StringProperty("0")
    cristal = StringProperty("0")
    deuterium = StringProperty("0")

    def __init__(self, **kwargs):
        super(Ressources_defenseur, self).__init__(**kwargs)
        self.cols = 3
        self.spacing = [5, 5]
        self.size_hint = (1, None)
        self.height = 65

        ress = ["Métal", "Cristal", "Dutérium"]
        for r in ress:
            lab = Label(text = r, size_hint = (1, None), height = 30)
            self.add_widget(lab)

        self.emetal = TextInput(size_hint = (1, None), height = 30)
        self.emetal.bind(text = self.setter("metal"))
        self.add_widget(self.emetal)

        self.ecristal = TextInput(size_hint = (1, None), height = 30)
        self.ecristal.bind(text = self.setter("cristal"))
        self.add_widget(self.ecristal)

        self.edeuterium = TextInput(size_hint = (1, None), height = 30)
        self.edeuterium.bind(text = self.setter("deuterium"))
        self.add_widget(self.edeuterium)
        
