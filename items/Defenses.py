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

import random 


livaisseaux = ["Petit Transporteur", "Grand Transporteur", "Chasseur Leger", "Chasseur Lourd",
               "Croiseur", "Vaisseau de Bataille", "Vaisseau de Colo", "Recycleur", "Sonde",
               "Bombardier", "Destructeur", "RIP", "Traqueur", "Faucheur", "Eclaireur",
               "Lanceur de missiles", "Artillerie laser legere", "Artillerie laser lourde", 
               "Canon de Gauss", "Artillerie a ions", "Lanceur de plasma", "Petit bouclier",
               "Grand bouclier", "Satellite solaire", "Foreuse"]      

class Defense:

    def __init__(self):
        self.ress = [0, 0, 0]
        self.structure = 0
        self.bouclier = 0
        self.attaque = 0

        self.priority = 5

        self.rf = {}

        self.sfdv = {"Intensification du bouclier à lobsidienne" : 0.005}


    def with_tech(self, combat = {"arme" : 0, "bouclier" : 0, "protec" : 0}, 
                        vitesse = {"combu" : 0, "impu" : 0, "prop" : 0}, 
                        hyperespace = 0, 
                        classes = {"ally" : "", "joueur" : ""}, 
                        fdv = {}):
        ncombat = self.tech_fight(combat, classes, fdv)
        return [ncombat, None, None, None]


    def tech_fight(self, combat, classes, fdv):
        # combat
        bsfdv = 0
        for vt in self.sfdv:
            bsfdv += fdv[vt]*self.sfdv[vt]

        na = self.attaque * (1 + combat["arme"]*0.1)
        naf = self.attaque * bsfdv
        nafc = self.attaque*1.2 * fdv["Renforcement du général des Mechas"]*0.002 if classes["joueur"] == "Général" else 0
        nva = na + naf + nafc

        nb = self.bouclier * (1 + combat["bouclier"]*0.1)
        nbf = self.bouclier * bsfdv
        nbfc = self.bouclier*1.2 * fdv["Renforcement du général des Mechas"]*0.002 if classes["joueur"] == "Général" else 0
        nvb = nb + nbf + nbfc

        nc = self.structure * (1+ combat["protec"]*0.1)*0.1
        ncf = self.structure * bsfdv
        ncfc = self.structure*1.2 * fdv["Renforcement du général des Mechas"]*0.002 if classes["joueur"] == "Général" else 0
        nvc = nc + ncf + ncfc

        ncombat = {"attaque" : nva, "bouclier" : nvb, "protec" : nvc}
        
        return ncombat


    def prepare_battle(self, combat = {"arme" : 0, "bouclier" : 0, "protec" : 0}, 
                             vitesse = {"combu" : 0, "impu" : 0, "prop" : 0}, 
                             hyperespace = 0, 
                             classes = {"ally" : "", "joueur" : ""}, 
                             meme_ally = False,
                             conso = 100,
                            fdv = {},
                            pseudo = ""):
        
        techs = self.tech_fight(combat, classes, fdv)

        self.structure = techs["protec"]
        self.bouclier = techs["bouclier"]
        self.attaque = techs["attaque"]

        self.w_structure = techs["protec"]
        self.w_bouclier = techs["bouclier"]
        self.marked_dead = False

        self.fret = 0

        self.pseudo = pseudo
        return [livaisseaux.index(self.__class__.__name__.replace("_", " ")),self.attaque, self.bouclier, self.w_bouclier, self.structure, self.w_structure, self.fret, self.pseudo, 0, self.priority]


    def next_turn(self):
        self.w_bouclier = self.bouclier


    def get_fired(self, val):
        #tir 
        #print("\n\nget shot : ", self.pseudo, "\ntir de : ", val, "\nboulier : ", self.w_bouclier, "\nstructure : ", self.w_structure)
        if val > self.w_bouclier*0.01:
            self.w_bouclier -= val
            if self.w_bouclier < 0:
                self.w_structure += self.w_bouclier
                self.w_bouclier = 0
        
        #print("\netat final : ", self.w_structure, " / ", self.structure)
        self.is_dead()
    
    
    def is_dead(self):
        if self.w_structure <= self.structure*0.7:
            #print("will explose ?\n")
            prc = self.w_structure / self.structure
            verdict = random.random()
            if prc < verdict:
                self.marked_dead = True
                #print("is dead\n")




class Lanceur_de_missiles(Defense):

    def __init__(self, **kwargs):
        super(Lanceur_de_missiles, self).__init__(**kwargs)
        self.ress = [2000, 0, 0]
        self.structure = 2000
        self.bouclier = 20
        self.attaque = 80

        self.rf = {}



class Artillerie_laser_legere(Defense):

    def __init__(self, **kwargs):
        super(Artillerie_laser_legere, self).__init__(**kwargs)
        self.ress = [1500, 500, 0]
        self.structure = 2000
        self.bouclier = 25
        self.attaque = 100

        self.rf = {}



class Artillerie_laser_lourde(Defense):

    def __init__(self, **kwargs):
        super(Artillerie_laser_lourde, self).__init__(**kwargs)
        self.ress = [6000, 2000, 0]
        self.structure = 8000
        self.bouclier = 100
        self.attaque = 250

        self.rf = {}

        

class Canon_de_Gauss(Defense):

    def __init__(self, **kwargs):
        super(Canon_de_Gauss, self).__init__(**kwargs)
        self.ress = [20000, 15000, 2000]
        self.structure = 35000
        self.bouclier = 200
        self.attaque = 1100

        self.rf = {}



class Artillerie_a_ions(Defense):

    def __init__(self, **kwargs):
        super(Artillerie_a_ions, self).__init__(**kwargs)
        self.ress = [5000, 3000, 0]
        self.structure = 8000
        self.bouclier = 500
        self.attaque = 150

        self.rf = {"Faucheur" : 2}


              
class Lanceur_de_plasma(Defense):

    def __init__(self, **kwargs):
        super(Lanceur_de_plasma, self).__init__(**kwargs)
        self.ress = [50000, 50000, 30000]
        self.structure = 100000
        self.bouclier = 300
        self.attaque = 3000

        self.rf = {}


                
class Petit_bouclier(Defense):

    def __init__(self, **kwargs):
        super(Petit_bouclier, self).__init__(**kwargs)
        self.ress = [10000, 10000, 0]
        self.structure = 20000
        self.bouclier = 2000
        self.attaque = 1

        self.rf = {}



class Grand_bouclier(Defense):

    def __init__(self, **kwargs):
        super(Grand_bouclier, self).__init__(**kwargs)
        self.ress = [50000, 50000, 0]
        self.structure = 100000
        self.bouclier = 10000
        self.attaque = 1

        self.rf = {}



class Satellite_solaire(Defense):

    def __init__(self, **kwargs):
        super(Satellite_solaire, self).__init__(**kwargs)
        self.ress = [0, 2000, 500]
        self.structure = 2000
        self.bouclier = 1
        self.attaque = 1

        self.rf = {}



class Foreuse(Defense):

    def __init__(self, **kwargs):
        super(Foreuse, self).__init__(**kwargs)
        self.ress = [2000, 2000, 1000]
        self.structure = 4000
        self.bouclier = 1
        self.attaque = 1

        self.rf = {}

