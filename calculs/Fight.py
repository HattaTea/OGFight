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


from items import *

import threading
from random import random
import numpy as np

import datetime
import time

dic_rf = {}
for item in livaisseaux:
    dic_rf[item] = eval(item.replace(" ", "_"))().rf


class Fight(threading.Thread):

    def __init__(self, attaquants, defenseurs, nb, **kwargs):
        super(Fight, self).__init__(**kwargs)

        self.attaquants = attaquants
        self.defenseurs = defenseurs

        self.fights = [Fighting(self.attaquants, self.defenseurs) for x in range(nb)]

        self.bilans = []

    def run(self, *arg):
        for f in self.fights:
            f.start()
        for ff in self.fights:
            ff.join()
            self.bilans.append(ff.result)
        return self.bilans



class Fighting(threading.Thread):

    def __init__(self, attaquants, defenseurs, **kwargs):
        super(Fighting, self).__init__(**kwargs)

        self.attaquants = np.asarray(attaquants, dtype = "i4")
        self.defenseurs = np.asarray(defenseurs, dtype = "i4")

        self.result = {}
    

    def run(self, *arg):
        # liste de liste de destruction des rounds
        detruit_att = []
        detruit_def = []  
        """
        def shoot(v, liste):
            #cible
            index = int(random()*len(liste))
            target = liste[index]

            #[livaisseaux.index(self.__class__.__name__.replace("_", " ")),
            # self.attaque, self.bouclier, self.w_bouclier, self.structure, 
            # self.w_structure, self.fret, self.pseudo, self.marked_dead]
            # tir
            val = v[1]
            if val > target[3]*0.01:
                brestant = target[3] - val
                crestant = target[5]
                dead = target[8]
                if brestant < 0:
                    crestant = target[5] + brestant
                    brestant = 0
                    if target[5] <= target[4]*0.7:
                        prc = target[5] / target[4]
                        verdict = random()
                        if prc < verdict:
                            dead = True
                target[3] = brestant
                target[5] = crestant
                target[8] = dead
                        
            #rf
            if livaisseaux[target[0]] in dic_rf[livaisseaux[v[0]]]:
                prc = 1 -  (1/dic_rf[livaisseaux[v[0]]][livaisseaux[target[0]]])
                verdict = random()
                if prc > verdict:
                    shoot(v, liste)
            return v
        """

        def snext_turn(v):
            v[3] = v[2]
            return v

        def get_damagesa(v):
            if len(self.defenseurs):
                index = int(random()*len(self.defenseurs))
                target = self.defenseurs[index]
                self.damages_a[index].append(v[1])
                #rf
                if livaisseaux[target[0]].replace(" ", "_") in dic_rf[livaisseaux[v[0]]]:
                    prc = 1 -  (1/dic_rf[livaisseaux[v[0]]][livaisseaux[target[0]].replace(" ", "_")])
                    verdict = random()
                    if prc > verdict:
                        get_damagesa(v)
            return

        def get_damagesd(v):
            if len(self.attaquants):
                index = int(random()*len(self.attaquants))
                target = self.attaquants[index]
                self.damages_d[index].append(v[1])
                #rf
                if livaisseaux[target[0]].replace(" ", "_") in dic_rf[livaisseaux[v[0]]]:
                    prc = 1 -  (1/dic_rf[livaisseaux[v[0]]][livaisseaux[target[0]].replace(" ", "_")])
                    verdict = random()
                    if prc > verdict:
                        time.sleep(0.00001)
                        get_damagesd(v)
            return            

        def apply_damages(d, v):
            #print("tir sur :", v, d)
            for t in range(len(d)):
                brestant = v[3]
                crestant = v[5]
                dead = v[8]
                if d[t] > v[3]*0.01:
                    brestant = brestant - d[t]
                    crestant = v[5]
                    dead = v[8]
                if brestant < 0:
                    crestant = crestant + brestant
                    brestant = 0
                    if crestant <= v[4]*0.7:
                        prc = crestant / v[4]
                        verdict = random()
                        if prc < verdict:
                            dead = 1
                v[3] = brestant
                v[5] = crestant
                v[8] = dead        
            return v        

        for rounds in range(6):
            tr = datetime.datetime.now()
            #print("round ", rounds+1, tr)
            
            self.damages_a = [[] for x in self.defenseurs]
            for a in self.attaquants:
                get_damagesa(a[:2])
                
            #print("get att : ", datetime.datetime.now()-tr)
            self.defenseurs = [apply_damages(xx, yy) for xx, yy in zip(self.damages_a, self.defenseurs)]
            ar = datetime.datetime.now()
            #print("les attaquant ont tirés en :", ar - tr)

            self.damages_d = [[] for y in self.attaquants]
            for d in self.defenseurs:
                get_damagesd(d[:2]) 
            self.attaquants =  [apply_damages(xx, yy) for xx, yy in zip(self.damages_d, self.attaquants)]
            dr = datetime.datetime.now()
            #print("les défenseurs ont tirés en : ", dr - ar)
            
            # listage des cadavres 
            dta = [x for x in self.attaquants if x[8]==1] 
            dtd = [y for y in self.defenseurs if y[8]==1]

            detruit_att.append(dta)
            detruit_def.append(dtd)

            ddr = datetime.datetime.now()
            #print("Les destructions ont pris : ", ddr - dr)
            
            # fin ou next turn
            if not len(self.attaquants) or not len(self.defenseurs):
                break
            else:
                # destructions + régénération des boucliers
                self.attaquants = np.asarray([snext_turn(xx) for xx in self.attaquants if not xx[8]], dtype = "i4")
                self.defenseurs = np.asarray([snext_turn(yy) for yy in self.defenseurs if not yy[8]], dtype = "i4")


        #print("Fin du combat\n", flottes_att, "\n\n", flottes_def, "\n\n")
        res = {"attaquant" : {"alive" : self.attaquants,
                              "dead" : detruit_att},
               "defenseur" : {"alive" : self.defenseurs,
                              "dead" : detruit_def},
               "rounds" : rounds}
        self.result = res
        return res
