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
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.checkbox import CheckBox

from kivy.properties import StringProperty, BooleanProperty

from mywidgets import MyDropDown, Label_Button, FGridLayout


class Param_simu(FGridLayout):

    nb_simu = StringProperty("50")
    prc_pillage = StringProperty("50")
    limite_ff = StringProperty("25")

    vitesse_uni = StringProperty("1")
    conso_uni = StringProperty("100")
    prc_cdr = StringProperty("30")
    prc_defcdr = StringProperty("0")
    nb_gal = StringProperty("5")
    nb_ss = StringProperty("499")
    deut_cdr = BooleanProperty(False)
    coef = BooleanProperty(True)

    def __init__(self, **kwargs):
        super(Param_simu, self).__init__(**kwargs)

        self.cols = 1
        self.spacing = [10, 10]

        self.titre = Label(text = "PARAMETRES", size_hint = (1, None), height = 60)
        self.add_widget(self.titre)

        ## Paramètre Simulation ##
        self.sparam = ScrollView()
        self.add_widget(self.sparam)

        self.sfparam = GridLayout(cols = 1, size_hint = (1, None), height = 450)
        self.sparam.add_widget(self.sfparam)

        self.fsaisi = GridLayout(cols = 1, spacing = [10, 10], size_hint = (1, None), height = 120)
        self.sfparam.add_widget(self.fsaisi)

        self.fsimu = GridLayout(rows = 4)
        self.lsimu = Label(text = "SIMULATION", size_hint = (1, None), height = 40)
        self.fsimu.add_widget(self.lsimu)

        # simulation
        self.fnbs = GridLayout(cols = 2, size_hint = (1, None), height = 30)
        self.lnbs = Label(text = "Nombre de simulation :")
        self.enbs = TextInput(text = "50", size_hint = (None, 1), width = 40)
        self.enbs.bind(text = self.setter("nb_simu"))
        self.fnbs.add_widget(self.lnbs)
        self.fnbs.add_widget(self.enbs)
        self.fsimu.add_widget(self.fnbs)


        self.fpillage = GridLayout(cols = 2, size_hint = (1, None), height = 30)
        self.lpillage = Label(text = "Pourcentage de  pillage :")
        self.vpillage = MyDropDown()

        for x in range(3):
            btn = Label_Button(text = str(50+25*x), size_hint_y = None, height = 30)
            btn.bind(on_release = lambda btn: self.vpillage.select(btn.text))
            self.vpillage.add_widget(btn)

        self.epillage = Button(text = "50", size_hint = (None, 1), width = 40)
        self.epillage.bind(text = self.setter("prc_pillage"))
        self.epillage.bind(on_release = self.vpillage.open)
        self.vpillage.bind(on_select=lambda instance, x: setattr(self.epillage, 'text', x))
        self.fpillage.add_widget(self.lpillage)
        self.fpillage.add_widget(self.epillage)
        self.fsimu.add_widget(self.fpillage)


        self.fff = GridLayout(cols = 2, size_hint = (1, None), height = 30)
        self.lff = Label(text = "Pourcentage max du recyclage faucheur :")
        self.eff = TextInput(text = "25", size_hint = (None, 1), width = 40)
        self.eff.bind(text = self.setter("limite_ff"))
        self.fff.add_widget(self.lff)
        self.fff.add_widget(self.eff)
        self.fsimu.add_widget(self.fff)

        self.fsaisi.add_widget(self.fsimu)


        # Univers
        self.funi = GridLayout(cols = 1, padding = [0, 20], size_hint = (1, None), height = 240)
        self.luni = Label(text = "UNIVERS", size_hint = (1, None), height = 40)
        self.funi.add_widget(self.luni)

        self.fvuni = GridLayout(cols = 1)
        self.fvituni = GridLayout(cols = 2, size_hint = (1, None), height = 30)
        self.lvituni = Label(text = "Vitesse de l'univers :")
        self.evituni = TextInput(text = "1", size_hint = (None, 1), width = 40)
        self.evituni.bind(text = self.setter("vitesse_uni"))
        self.fvituni.add_widget(self.lvituni)
        self.fvituni.add_widget(self.evituni)
        self.fvuni.add_widget(self.fvituni)

        self.fcuni = GridLayout(cols = 2, size_hint = (1, None), height = 30)
        self.lcuni = Label(text = "Facteur de consommation de l'univers :")
        self.ecuni = TextInput(text = "1", size_hint = (None, 1), width = 40)
        self.ecuni.bind(text = self.setter("conso_uni"))
        self.fcuni.add_widget(self.lcuni)
        self.fcuni.add_widget(self.ecuni)
        self.fvuni.add_widget(self.fcuni)

        self.fpcdr = GridLayout(cols = 2, size_hint = (1, None), height = 30)
        self.lpcdr = Label(text = "Pourcentage de flotte dans le cdr :")
        self.epcdr = TextInput(text = "30", size_hint = (None, 1), width = 40)
        self.epcdr.bind(text = self.setter("prc_cdr"))
        self.fpcdr.add_widget(self.lpcdr)
        self.fpcdr.add_widget(self.epcdr)
        self.fvuni.add_widget(self.fpcdr)

        self.fpdef = GridLayout(cols = 2, size_hint = (1, None), height = 30)
        self.lpdef = Label(text = "Pourcentage de défense dans le cdr :")
        self.epdef = TextInput(text = "0", size_hint = (None, 1), width = 40)
        self.epdef.bind(text = self.setter("prc_defcdr"))
        self.fpdef.add_widget(self.lpdef)
        self.fpdef.add_widget(self.epdef)
        self.fvuni.add_widget(self.fpdef)
        
        self.fngal = GridLayout(cols = 2, size_hint = (1, None), height = 30)
        self.lngal = Label(text = "Nombre de galaxie :")
        self.engal = TextInput(text = "5", size_hint = (None, 1), width = 40)
        self.engal.bind(text = self.setter("nb_gal"))
        self.fngal.add_widget(self.lngal)
        self.fngal.add_widget(self.engal)
        self.fvuni.add_widget(self.fngal)

        self.fnss = GridLayout(cols = 2, size_hint = (1, None), height = 30)
        self.lnss = Label(text = "Nombre de systèmes solaires :")
        self.enss = TextInput(text = "499", size_hint = (None, 1), width = 40)
        self.enss.bind(text = self.setter("nb_ss"))
        self.fnss.add_widget(self.lnss)
        self.fnss.add_widget(self.enss)
        self.fvuni.add_widget(self.fnss)

        self.fdcdr = GridLayout(cols = 2, size_hint = (1, None), height = 30)
        self.ldcdr = Label(text = "Deutérium dans le cdr :")
        self.edcdr = CheckBox(active = False, size_hint = (None, 1), width = 40)
        self.edcdr.bind(active = self.setter("deut_cdr"))
        self.fdcdr.add_widget(self.ldcdr)
        self.fdcdr.add_widget(self.edcdr)
        self.fvuni.add_widget(self.fdcdr)
        
        self.fcoef = GridLayout(cols = 2, size_hint = (1, None), height = 30)
        self.lcoef = Label(text = "Appliquer un coef :")
        self.ecoef = CheckBox(active = True, size_hint = (None, 1), width = 40)
        self.ecoef.bind(active = self.setter("coef"))
        self.fcoef.add_widget(self.lcoef)
        self.fcoef.add_widget(self.ecoef)
        self.fvuni.add_widget(self.fcoef)
        
        
        """
        self.fswitch = GridLayout(cols = 2, size_hint = (1, None), height = 30)
        self.lswitch = Label(text = "Inverser Attaquants / Défenseurs :")
        self.bswitch = Button(text = "Inverser", size_hint = (None, 1), width= 40)
        self.bswitch.bind(on_press = lambda e : self.switch())
        self.fswitch.add_widget(self.lswitch)
        self.fswitch.add_widget(self.bswitch)
        self.fvuni.add_widget(self.fswitch)
        """
        self.funi.add_widget(self.fvuni)
        self.sfparam.add_widget(self.funi)

        ## pillage ##
        self.fpillage = GridLayout(cols = 1)
        self.lpillage = Label(text = "PILLAGE", size_hint = (1, None), height = 60)
        self.fpillage.add_widget(self.lpillage)

        self.fvpillage = GridLayout(cols = 3)
        
        # pillé
        self.frpille = GridLayout(cols = 1)
        self.frpille.add_widget(Label(text = "Pillé", size_hint = (1, None), height = 40))

        self.frrpille = GridLayout(cols = 2)
        self.frpille.add_widget(self.frrpille)
        
        self.lmrp = Label(text = "M", size_hint = (None, 1), width = 10)
        self.emrp = Label(text = "0")
        self.lcrp = Label(text = "C", size_hint = (None, 1), width = 10)
        self.ecrp = Label(text = "0")
        self.ldrp = Label(text = "D", size_hint = (None, 1), width = 10)
        self.edrp = Label(text = "0")
        self.ltrp = Label(text = "=", size_hint = (None, 1), width = 10)
        self.etrp = Label(text = "0")


        self.frrpille.add_widget(self.lmrp)
        self.frrpille.add_widget(self.emrp)
        self.frrpille.add_widget(self.lcrp)
        self.frrpille.add_widget(self.ecrp)
        self.frrpille.add_widget(self.ldrp)
        self.frrpille.add_widget(self.edrp)
        self.frrpille.add_widget(self.ltrp)
        self.frrpille.add_widget(self.etrp)

        # pillage possible
        self.fppille = GridLayout(cols = 1)
        self.fppille.add_widget(Label(text = "Pillage possible", size_hint = (1, None), height = 40))

        self.fpppille = GridLayout(cols = 2)
        self.fppille.add_widget(self.fpppille)
        
        self.lmrpp = Label(text = "M", size_hint = (None, 1), width = 10)
        self.emrpp = Label(text = "0")
        self.lcrpp = Label(text = "C", size_hint = (None, 1), width = 10)
        self.ecrpp = Label(text = "0")
        self.ldrpp = Label(text = "D", size_hint = (None, 1), width = 10)
        self.edrpp = Label(text = "0")
        self.ltrpp = Label(text = "=", size_hint = (None, 1), width = 10)
        self.etrpp = Label(text = "0")
        self.etrpp.bind(text = self.actu)

        self.fpppille.add_widget(self.lmrpp)
        self.fpppille.add_widget(self.emrpp)
        self.fpppille.add_widget(self.lcrpp)
        self.fpppille.add_widget(self.ecrpp)
        self.fpppille.add_widget(self.ldrpp)
        self.fpppille.add_widget(self.edrpp)
        self.fpppille.add_widget(self.ltrpp)
        self.fpppille.add_widget(self.etrpp)

        # vaisseaux
        self.liatt = []
        self.livai = []
        self.ftpille = GridLayout(cols = 1, spacing = [10, 10])
        self.ftpille.add_widget(Label(text = "Selectionner un joueur\net un vaisseau", halign = "center"))
        # joueur
        self.dpjoueur = MyDropDown()
        self.bpjoueur = Button(text = "")
        self.ftpille.add_widget(self.bpjoueur)
        self.bpjoueur.bind(on_release = self.dpjoueur.open)        
        self.dpjoueur.bind(on_select=lambda instance, x: setattr(self.bpjoueur, 'text', x))        
        # vaisseau
        self.dpvaiss = MyDropDown()
        self.bpvaiss = Button(text = "")
        self.ftpille.add_widget(self.bpvaiss)
        self.bpvaiss.bind(on_release = self.dpvaiss.open)        
        self.dpvaiss.bind(on_select=lambda instance, x: setattr(self.bpvaiss, 'text', x))          
        # = 
        self.lpnb = Label(text = "0")
        self.ftpille.add_widget(self.lpnb)

        self.fvpillage.add_widget(self.frpille)
        self.fvpillage.add_widget(self.fppille)
        self.fvpillage.add_widget(self.ftpille)
        
        self.fpillage.add_widget(self.fvpillage)
        
        self.add_widget(self.fpillage) # pillage)
        
        # Boutons
        self.fopt = GridLayout(cols = 3, size_hint = (1, None), height = 70, spacing = [20, 10])
        self.add_widget(self.fopt)
        self.b_prec = Button(text = "VAGUE PREC")
        self.l_vague = Label(text = "VAGUE 1")
        self.b_suiv = Button(text = "VAGUE SUIV")

        self.b_bilan = Button(text = "BILAN")
        self.b_recyclage = Button(text = "RECYCLAGE")
        self.b_recap = Button(text = "RECAP")
        
        self.fopt.add_widget(self.b_prec)
        self.fopt.add_widget(self.l_vague)
        self.fopt.add_widget(self.b_suiv)

        self.fopt.add_widget(self.b_bilan)
        self.fopt.add_widget(self.b_recyclage)
        self.fopt.add_widget(self.b_recap)

        self.b_simu = Button(text = "SIMULER", size_hint = (1, None), height = 60)
        self.add_widget(self.b_simu)

        
    def actu(self, *arg):
        pass

    def switch(self, *arg):
        pass
