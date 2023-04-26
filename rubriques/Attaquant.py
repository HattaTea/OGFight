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

from kivy.properties import ListProperty

from mywidgets import FGridLayout
from .saisies import Attaquant


class Attaquants(FGridLayout):

    values = ListProperty([])

    def __init__(self, **kwargs):
        super(Attaquants, self).__init__(**kwargs)

        self.vaisseaux = ["Petit Transporteur", "Grand Transporteur", "Chasseur Leger", "Chasseur Lourd",
                          "Croiseur", "Vaisseau de Bataille", "Vaisseau de Colo", "Recycleur", "Sonde",
                          "Bombardier", "Destructeur", "RIP", "Traqueur", "Faucheur", "Eclaireur"]      

        self.cols = 1

        self.frame = GridLayout(cols = 1)
        self.latt = Label(text = "ATTAQUANT", size_hint = (1, None), height = 60)
        self.frame.add_widget(self.latt)

        self.fbut = GridLayout(cols = 2, size_hint = (1, None), height = 30)
        self.bajout = Button(text = "Ajouter")
        self.bajout.bind(on_release = self.add_attaquant)
        self.bdel = Button(text = "Effacer")
        self.bdel.bind(on_release = self.del_attaquant)
        
        self.fbut.add_widget(self.bajout)
        self.fbut.add_widget(self.bdel)
        self.frame.add_widget(self.fbut)

        self.ftabs = GridLayout(cols = 5, size_hint = (1, None), height = 90)
        self.frame.add_widget(self.ftabs)

        self.fvdis = GridLayout(cols = 1, spacing = [0, 20])
        self.frame.add_widget(self.fvdis)

        self.add_widget(self.frame)

        self.vagues = []
        self.nvague = 0

        #self.add_attaquant()


    def add_attaquant(self, slot = None, *arg):
        self.fvdis.clear_widgets()

        if isinstance(slot, Button) or not slot:
            natt = Attaquant(len(self.values)+1)
        else :
            natt = slot
        self.fvdis.add_widget(natt)
        natt.ftechs.bind(hyperespace = self.actu_pillage)
        natt.maj_tvc = self.maj_tvc

        vtab = Button(text = "A{}".format(len(self.values)+1))
        natt.finput.bind(pseudo = vtab.setter("text"))
        vtab.bind(on_release = lambda e, i = len(self.values) : self.show_attaquant(i))
        self.ftabs.add_widget(vtab)

        self.values.append(natt)

    def show_attaquant(self, index):
        self.fvdis.clear_widgets()
        self.fvdis.add_widget(self.values[index])
        # pb check buttons

    def del_attaquant(self, *arg):
        if len(self.values) > 1:
            index = len(self.values) - self.values.index(self.fvdis.children[0]) -1
            if index < 0:
                index = 0
            self.values.remove(self.fvdis.children[0])

            self.fvdis.remove_widget(self.fvdis.children[0])
            self.ftabs.remove_widget(self.ftabs.children[index])

            self.show_attaquant(index-1)

    def actu_pillage(self, *arg):
        pass

    def maj_tvc(self, *arg):
        pass

    def vague_suiv(self, *arg):
        if self.nvague == 0 and len(self.vagues) == 0:
            prec = [v for v in self.values]
            suiv = []
            for a in self.values:
                na = Attaquant(a.finput.pseudo)

                na.fclasses.boxally.value = a.fclasses.ally
                na.fclasses.boxclass.value = a.fclasses.classe 

                na.ftechs.earme.text = a.ftechs.earme.text
                na.ftechs.ebou.text = a.ftechs.ebou.text
                na.ftechs.ecoque.text = a.ftechs.ecoque.text

                na.ftechs.ecombu.text = a.ftechs.ecombu.text
                na.ftechs.eimpu.text = a.ftechs.eimpu.text
                na.ftechs.eprop.text = a.ftechs.eprop.text
                na.ftechs.ehyper.text = a.ftechs.ehyper.text

                na.fcoord.galaxie.text = a.fcoord.galaxie.text
                na.fcoord.ss.text = a.fcoord.ss.text
                na.fcoord.position = a.fcoord.position

                for v in a.fflotte.avaisseaux:
                    try:
                        wq = float(a.fflotte.restants[a.fflotte.avaisseaux[v]].text.split(" ")[-1])
                        if v in a.fflotte.vaisseaux:
                            wz = str(round(wq))
                        else:
                            wz = str(round(wz*0.7)) # Ingénieur
                    except:
                        wz = "0"
                    na.fflotte.vals[v].text = wz

                for tf in a.cfdv.vals:
                    na.cfdv.vals[tf].text = a.cfdv.vals[tf].text

                suiv.append(na)
        
            self.vagues.append(prec)
            self.vagues.append(suiv)

            self.afficher_vague(len(self.vagues)-1)
            return

        if self.nvague+1 == len(self.vagues) and len(self.vagues) > 0:
            suiv = []
            for a in self.values:
                na = Attaquant(a.finput.pseudo)
                na.fclasses.boxally.value = a.fclasses.ally
                na.fclasses.boxclass.value = a.fclasses.classe 

                na.ftechs.earme.text = a.ftechs.earme.text
                na.ftechs.ebou.text = a.ftechs.ebou.text
                na.ftechs.ecoque.text = a.ftechs.ecoque.text

                na.ftechs.ecombu.text = a.ftechs.ecombu.text
                na.ftechs.eimpu.text = a.ftechs.eimpu.text
                na.ftechs.eprop.text = a.ftechs.eprop.text
                na.ftechs.ehyper.text = a.ftechs.ehyper.text

                na.fcoord.galaxie.text = a.fcoord.galaxie.text
                na.fcoord.ss.text = a.fcoord.ss.text
                na.fcoord.position = a.fcoord.position

                for v in a.fflotte.avaisseaux:
                    try:
                        wq = float(a.fflotte.restants[a.fflotte.avaisseaux[v]].text.split(" ")[-1])
                        if v in a.fflotte.vaisseaux:
                            wz = str(round(wq))
                        else:
                            wz = str(round(wz*0.7)) # Ingénieur?
                    except:
                        wz = "0"
                    na.fflotte.vals[v].text = wz

                for tf in a.cfdv.vals:
                    na.cfdv.vals[tf].text = a.cfdv.vals[tf].text

                suiv.append(na)

            self.vagues.append(suiv)
            self.afficher_vague(len(self.vagues)-1)
            return

        else:
            self.afficher_vague(self.nvague+1)



    def afficher_vague(self, ind, *arg):
        if ind >= 0:
            self.fvdis.clear_widgets()
            self.ftabs.clear_widgets()
                        
            for x in range(len(self.values)):
                self.values.remove(self.values[0])

            for s in self.vagues[ind]:
                self.add_attaquant(slot = s)
            self.nvague = ind
