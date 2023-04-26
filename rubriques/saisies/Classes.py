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

from mywidgets import MyCheckBox

from kivy.properties import StringProperty


class Classes(GridLayout):
    num = []
    ally = StringProperty("")
    classe = StringProperty("")

    def __init__(self, **kwargs):
        super(Classes, self).__init__(**kwargs)
        self.rows = 2
        self.size_hint = (1, None)
        self.height = 120

        self.dic_ally =  ["Marchand", "Guerrier", "Chercheur"]
        self.dic_class = ["Collecteur", "Général", "Explorateur"]
        
        # ally
        self.fally = GridLayout(rows = 2, height = 60, size_hint = (1, None))
        self.lally = Label(text = "Classe d'alliance : ", size_hint = (0.4, 1))
        self.fally.add_widget(self.lally)
        self.boxally = MyCheckBox("ally{}".format(len(self.num)), self.dic_ally)
        self.boxally.bind(value = self.setter("ally"))
        self.fally.add_widget(self.boxally)
        
        # joueur
        self.fclass = GridLayout(rows = 2, height = 60, size_hint = (1, None))
        self.lclass = Label(text = "Classe du joueur : ", size_hint = (0.4, 1))
        self.fclass.add_widget(self.lclass)
        self.boxclass = MyCheckBox("classe{}".format(len(self.num)), self.dic_class)
        self.boxclass.bind(value = self.setter("classe"))
        self.fclass.add_widget(self.boxclass)        

        self.add_widget(self.fally)
        self.add_widget(self.fclass)        
        self.num.append(0)
