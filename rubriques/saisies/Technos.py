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
from kivy.clock import Clock

from kivy.properties import StringProperty

import time

class Technos(GridLayout):

    arme = StringProperty("0")
    bouclier = StringProperty("0")
    coque = StringProperty("0")

    combu = StringProperty("0")
    impu = StringProperty("0")
    prop = StringProperty("0")

    hyperespace = StringProperty("0")

    def __init__(self, **kwargs):
        super(Technos, self).__init__(**kwargs)

        self.rows = 2
        self.size_hint = (1, None)
        self.height = 180
        self.spacing = [0, 10]

        # combat + vitesse
        self.ftcv = GridLayout(cols = 1, spacing = [0, 10])
        self.add_widget(self.ftcv)
        
        # combat
        self.fftc = GridLayout(cols = 1)
        self.ltc = Label(text = "COMBAT")
        self.fftc.add_widget(self.ltc)

        self.ftc = GridLayout(rows = 1)
        self.fftc.add_widget(self.ftc)

        self.farme = GridLayout(cols = 4)
        self.larme = Label(text = "Arme :", size_hint = (None, 1), width = 80)
        self.earme = TextInput(text = "0", size_hint = (None, 1), width = 30)
        self.earme.bind(text = self.setter("arme"))
        self.farme.add_widget(Label(text = " "))
        self.farme.add_widget(self.larme)
        self.farme.add_widget(self.earme)
        self.farme.add_widget(Label(text = " "))
        self.ftc.add_widget(self.farme)

        self.fbou = GridLayout(cols = 4)
        self.lbou = Label(text = "Bouclier :", size_hint = (None, 1), width = 80)
        self.ebou = TextInput(text = "0", size_hint = (None, 1), width = 30)
        self.ebou.bind(text = self.setter("bouclier"))
        self.fbou.add_widget(Label(text = " "))
        self.fbou.add_widget(self.lbou)
        self.fbou.add_widget(self.ebou)
        self.fbou.add_widget(Label(text = " "))
        self.ftc.add_widget(self.fbou)

        self.fcoque = GridLayout(cols = 4)
        self.lcoque = Label(text = "Coque :", size_hint = (None, 1), width = 80)
        self.ecoque = TextInput(text = "0", size_hint = (None, 1), width = 30)
        self.ecoque.bind(text = self.setter("coque"))
        self.fcoque.add_widget(Label(text = " "))
        self.fcoque.add_widget(self.lcoque)
        self.fcoque.add_widget(self.ecoque)
        self.fcoque.add_widget(Label(text = " "))
        self.ftc.add_widget(self.fcoque)
        
        self.ftcv.add_widget(self.fftc)

        # vitesse
        self.fftv = GridLayout(cols = 1)
        self.ltv = Label(text = "VITESSE")
        self.fftv.add_widget(self.ltv)

        self.ftv = GridLayout(rows = 1)
        self.fftv.add_widget(self.ftv)

        self.fcombu = GridLayout(cols = 4)
        self.lcombu = Label(text = "Combustion :", size_hint = (None, 1), width = 100)
        self.ecombu = TextInput(text = "0", size_hint = (None, 1), width = 30)
        self.ecombu.bind(text = self.setter("combu"))
        self.fcombu.add_widget(Label(text = " "))
        self.fcombu.add_widget(self.lcombu)
        self.fcombu.add_widget(self.ecombu)
        self.fcombu.add_widget(Label(text = " "))
        self.ftv.add_widget(self.fcombu)

        self.fimpu = GridLayout(cols = 4)
        self.limpu = Label(text = "Impulsion :", size_hint = (None, 1), width = 100)
        self.eimpu = TextInput(text = "0", size_hint = (None, 1), width = 30)
        self.eimpu.bind(text = self.setter("impu"))
        self.fimpu.add_widget(Label(text = " "))
        self.fimpu.add_widget(self.limpu)
        self.fimpu.add_widget(self.eimpu)
        self.fimpu.add_widget(Label(text = " "))
        self.ftv.add_widget(self.fimpu)

        self.fprop = GridLayout(cols = 4)
        self.lprop = Label(text = "Propulsion :", size_hint = (None, 1), width = 100)
        self.eprop = TextInput(text = "0", size_hint = (None, 1), width = 30)
        self.eprop.bind(text = self.setter("prop"))
        self.fprop.add_widget(Label(text = " "))
        self.fprop.add_widget(self.lprop)
        self.fprop.add_widget(self.eprop)
        self.fprop.add_widget(Label(text = " "))
        self.ftv.add_widget(self.fprop)

        self.ftcv.add_widget(self.fftv)

        self.fhyper = GridLayout(cols = 4, size_hint = (1, None), height = 30)
        self.lhyper = Label(text = "Hyperespace (fret) :", size_hint = (None, 1), width = 140)
        self.ehyper = TextInput(text = "0", size_hint = (None, 1), width = 30)
        self.ehyper.bind(text = self.setter("hyperespace"))
        self.fhyper.add_widget(Label(text = " "))
        self.fhyper.add_widget(self.lhyper)
        self.fhyper.add_widget(self.ehyper)
        self.fhyper.add_widget(Label(text = " "))

        self.add_widget(self.fhyper)

        self.inputs = [self.earme, self.ebou, self.ecoque, self.ecombu, self.eimpu, self.eprop, self.ehyper]
        for i in self.inputs:
            i.keyboard_on_key_down = self.go_tab
            i.bind(text = lambda i, v : Clock.schedule_once(lambda e, ii = i, vv = v : self.e_number(ii, vv), -1))

    def e_number(self, i, v):
        if v != "":
            try:
                int(v)
            except:
                vi = i.cursor_index()
                i.text = i.text[:vi-1]+i.text[vi:]
                if vi == i.cursor_index():
                    i.do_cursor_movement("cursor_left")
                return

    def go_tab(self, window, keycode, text, modifier):
        if keycode[1] == "tab":
            for i in range(len(self.inputs)):
                if self.inputs[i].focus:
                    if i+1 < len(self.inputs):
                        self.inputs[i+1].focus = True
                        break
                    else:
                        self.go_nextab()
            return True
        
        elif keycode[1] == "backspace":
            for i in range(len(self.inputs)):
                if self.inputs[i].focus:
                    vi = self.inputs[i].cursor_index()
                    self.inputs[i].text = self.inputs[i].text[:vi-1]+self.inputs[i].text[vi:]
                    if vi == self.inputs[i].cursor_index():
                        self.inputs[i].do_cursor_movement("cursor_left")
                    break
            return True
        
        elif keycode[1] == "delete":
            for i in range(len(self.inputs)):
                if self.inputs[i].focus:
                    vi = self.inputs[i].cursor_index()
                    self.inputs[i].text = self.inputs[i].text[:vi]+self.inputs[i].text[vi+1:]
                    nvi = self.inputs[i].cursor_index()
                    if vi != nvi:
                        for x in range(nvi-vi+1):
                            self.inputs[i].do_cursor_movement("cursor_left")
                    break
            return True 

        elif keycode[1] == "left":
            for i in range(len(self.inputs)):
                if self.inputs[i].focus:                   
                    self.inputs[i].do_cursor_movement("cursor_left")
                    break
            return True
        
        elif keycode[1] == "right":
            for i in range(len(self.inputs)):
                if self.inputs[i].focus:                   
                    self.inputs[i].do_cursor_movement("cursor_right")
                    break
            return True        
        

    def go_nextab(self):
        pass
