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
from kivy.uix.popup import Popup

from kivy.properties import DictProperty


class Fdv_manuel(Popup):

    fdv = DictProperty({"Renforcement du général des Mechas" : 0,
                        "Renforcement d'explorateur Kaelesh" : 0,
                        "Renfort du collecteur Rocta" : 0,
                        "Récupération de chaleur" : 0,
                        "Module doptimisation" : 0,
                        "Moteur à plasma" : 0,
                        "Moteurs à fusion" : 0,
                        "Extension despace fret (vaisseaux civils)" : 0,
                        "Compresseur neuromodal" : 0,
                        "Révision complète (chasseur léger)" : 0,
                        "Chasseur léger Mk II" : 0,
                        "Renforcement à cristaux ioniques (chasseurs lourds)" : 0,
                        "Surcadençage (chasseur lourd)" : 0,
                        "Révision complète (croiseur)" : 0,
                        "Croiseur Mk II" : 0,
                        "Révision complète (vaisseau de bataille)" : 0,
                        "Surcadençage (vaisseau de bataille)" : 0,
                        "Révision complète (traqueur)" : 0,
                        "Traqueur Mk II" : 0,
                        "Bombardier Mk II" : 0,
                        "Révision complète (bombardier)" : 0,
                        "Destructeur Mk II" : 0,
                        "Révision complète (destructeur)" : 0,
                        "Surcadençage (grand transporteur)" : 0,
                        "Technique de recyclage expérimental" : 0,
                        "Intensification du bouclier à lobsidienne" : 0} )

    def __init__(self, **kwargs):
        super(Fdv_manuel, self).__init__(**kwargs)
        self.title = "Formes de vie"
        self.content = GridLayout(cols = 2, spacing = [20, 10])
        self.size_hint = (None, None)
        self.size = (900, 700)  

        self.vals = {}

        for t in self.fdv:
            ft = GridLayout(cols = 2, size_hint = (1, None), height = 30)
            lt = Label(text = t)
            et = TextInput(size_hint = (None, 1), width = 40)
            self.vals[t] = et
            et.bind(text = self.set_val)
            ft.add_widget(lt)
            ft.add_widget(et)
            self.content.add_widget(ft)

    def set_val(self, *arg):
        for tech in self.vals:
            try:
                self.fdv[tech] = int(self.vals[tech].text)
            except:
                pass    
