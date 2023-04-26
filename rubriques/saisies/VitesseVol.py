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
from kivy.uix.button import Button

from kivy.properties import NumericProperty

from mywidgets import MyDropDown, Label_Button


class VitesseVol(GridLayout):

    nb_inter = NumericProperty(10)
    vitesse = NumericProperty(100)

    def __init__(self, **kwargs):
        super(VitesseVol, self).__init__(**kwargs)

        self.cols = 4
        self.size_hint = (1, None)
        self.height = 30

        self.add_widget(Label(text = " "))


        self.lvit = Label(text = "Vitesse :", size_hint = (None, 1), width = 60)
        self.add_widget(self.lvit)
        self.vitchoice = MyDropDown()

        self.load_inter()
        
        self.vit = Button(text = "100", size_hint = (None, 1), width = 30)
        self.vit.bind(text = self.setter("vitesse"))
        self.vit.bind(on_release = self.vitchoice.open)
        self.vitchoice.bind(on_select=lambda instance, x: setattr(self.vit, 'text', x))
        
        self.add_widget(self.vit)
        self.add_widget(Label(text = " "))
        
        self.bind(nb_inter = self.load_inter)


    def load_inter(self, *arg):
        self.vitchoice.clear_widgets()
        for x in range(self.nb_inter):
            btn = Label_Button(text = str(x*100//self.nb_inter+100//self.nb_inter), size_hint_y = None, height = 30)
            btn.bind(on_release = lambda btn: self.vitchoice.select(btn.text))
            self.vitchoice.add_widget(btn)
