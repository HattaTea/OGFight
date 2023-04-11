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


# compilation
import os, sys
from kivy.resources import resource_add_path, resource_find

# Kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup

# local
from widgets import Label_Button, Fond
from rubriques import Attaquants, Defenseurs, Param_simu
from rubriques.saisies.Recyclage import Recyclage
from calculs import Bilan_vagues, Resultat, Fight

from items import *

# autre
import numpy as np
import datetime
from math import sqrt
import time

sys.setrecursionlimit(10000)


class Ogfight(App):
    
    def build(self):
        self.root = Fond(cols = 3, spacing = [20, 0], padding = [20, 20])

        # Saisie Attaquants - rubriques.Attaquants
        self.attaquants = Attaquants(size_hint = (1, 1))
        self.root.add_widget(self.attaquants)
        self.attaquants.maj_tvc = self.maj_tvc # actu temps de vol
        self.attaquants.add_attaquant()
        self.attaquants.bind(values = self.actu_pillage)
        #self.attaquants.actu_pillage = self.actu_pillage

        # Saisie Défenseurs - rubriques.Defenseurs
        self.defenseurs = Defenseurs(size_hint = (1, 1))
        self.root.add_widget(self.defenseurs)
        self.defenseurs.maj_tvc = self.maj_tvc
        self.defenseurs.add_first_defenseur()
        self.defenseurs.values[0].ressources.bind(metal = self.maj_pillage) 
        self.defenseurs.values[0].ressources.bind(cristal =self.maj_pillage)
        self.defenseurs.values[0].ressources.bind(deuterium = self.maj_pillage)

        # Saisie Paramètres - rubriques.Param_simu
        self.param = Param_simu()
        self.root.add_widget(self.param)
        self.param.b_simu.bind(on_press = self.simu)
        self.param.b_prec.bind(on_press = self.vague_prec)
        self.param.b_suiv.bind(on_press = self.vague_suiv)

        self.actu_pillage() # initialisation des pillages

        # liste des bilans des vagues
        self.lia_resu = []
        def aff_resu(*arg):
            if len(self.lia_resu):
                self.lia_resu[self.attaquants.nvague].open()
        self.param.b_bilan.bind(on_press = aff_resu)

        # liste des recyclages des vagues
        self.lia_recy = []
        def aff_recy(*arg):
            if len(self.lia_recy):
                self.lia_recy[self.attaquants.nvague].open()
        self.param.b_recyclage.bind(on_press = aff_recy)

        # Bilan
        self.bilan_vagues = Bilan_vagues()
        self.lia_bilan = []
        def aff_bi(*arg):
            try:
                self.bilan_vagues.open()
            except:
                pass
        self.param.b_recap.bind(on_press = aff_bi)


    def simu(self, *args):
        # output chrono
        start = datetime.datetime.now()
        print("starting at", start)
                
        bilan = [] # Liste des simulations de la vague

        # coef si trop de vaisseaux
        vcoef = max([sum(sum([int(eval("a.fflotte.{}".format(a.fflotte.avaisseaux[v]))) for v in a.fflotte.avaisseaux]) for a in self.attaquants.values)],
                    [sum(sum([int(eval("a.fflotte.{}".format(a.fflotte.avaisseaux[v]))) for v in a.fflotte.avaisseaux]) for a in self.defenseurs.values)])[0]
        coef = 1 if vcoef < 100000 else 10 if vcoef < 1000000 else 100 if vcoef < 10000000 else 1000

        # génération des flottes
        def gen_flotte(joueur):
            vdef = [de for de in joueur]
            flottes = []
            
            for a in vdef:
                # techs
                combat = {"arme" : int(a.ftechs.arme), "bouclier" : int(a.ftechs.bouclier), "protec" : int(a.ftechs.coque)}
                vitesse = {"combu" : int(a.ftechs.combu), "impu" : int(a.ftechs.impu), "prop" : int(a.ftechs.prop)}
                hyperespace = int(a.ftechs.hyperespace)
                classes = {"ally" : a.fclasses.ally, "joueur" : a.fclasses.classe}
                meme_ally = False
                conso = float(self.param.conso_uni)
                fdv = a.fdv_vitesse

                # vaisseaux
                for v in a.fflotte.avaisseaux:
                    w = eval("a.fflotte.{}".format(a.fflotte.avaisseaux[v]))
                    nv = eval("{}()".format(v.replace(" ", "_"))).prepare_battle(combat, vitesse, hyperespace, classes, meme_ally, conso, fdv, vdef.index(a))   
                    vflo = sorted([nv for x in range(ceil(int(w)/coef))], key = lambda a : a[9]) # trié par ordre de tir
                    flottes = flottes + vflo

            return flottes

        # simulations 
        nb = 0
        while nb < int(self.param.nb_simu):
            #time.sleep(0.1)
            print("\r{0} / {1}".format(nb+1, self.param.nb_simu))

            vf = Fight(gen_flotte(self.attaquants.values), gen_flotte(self.defenseurs.values), 10)
            vf.start()
            vf.join()
            bilan = bilan + vf.bilans
            nb += 10

        print("Make Bilan : ", datetime.datetime.now()) # chrono

        # Affichage des pertes dans les saisies
        for a in self.attaquants.values:
            for v in a.fflotte.avaisseaux:
                vals = []
                for bi in bilan:
                    nb = 0
                    for vd in bi["attaquant"]["alive"]:
                        if vd[7] == self.attaquants.values.index(a) and livaisseaux[ vd[0]] == v:
                            nb += 1
                    vals.append(nb*coef)
                try:
                    a.fflotte.restants[a.fflotte.avaisseaux[v]].text = "-> {}".format(round(int(eval("a.fflotte.{}".format(a.fflotte.avaisseaux[v]))) * (sum(vals)/len(vals))/int(eval("a.fflotte.{}".format(a.fflotte.avaisseaux[v])))))
                except:          
                    a.fflotte.restants[a.fflotte.avaisseaux[v]].text = "-> 0"  

        for a in self.defenseurs.values:
            for v in a.fflotte.avaisseaux:
                vals = []
                for bi in bilan:
                    nb = 0
                    for vd in bi["defenseur"]["alive"]:
                        if vd[7] == self.defenseurs.values.index(a) and livaisseaux[vd[0]] == v:
                            nb += 1
                    vals.append(nb*coef)
                try:
                    a.fflotte.restants[a.fflotte.avaisseaux[v]].text = "-> {}".format(round(int(eval("a.fflotte.{}".format(a.fflotte.avaisseaux[v]))) * (sum(vals)/len(vals))/int(eval("a.fflotte.{}".format(a.fflotte.avaisseaux[v])))))
                except:          
                    a.fflotte.restants[a.fflotte.avaisseaux[v]].text = "-> 0"  

        self.make_bilan(bilan, coef)

        print("end", datetime.datetime.now(), datetime.datetime.now()-start) # chrono


    def make_bilan(self, bilan, coef):
        # calculs

        # victoires attaquants, défenseurs, match nul
        vica = 0
        vicd = 0
        vicn = 0

        # pertes par ressources - attaquants, défenseurs
        apm = 0
        apc = 0
        apd = 0

        dpm = 0
        dpc = 0
        dpd = 0      

        # cdr flotte par ress
        cdrfm = 0
        cdrfc = 0
        cdrfd = 0

        # cdr def par ress
        cdrdm = 0
        cdrdc = 0
        cdrdd = 0

        # fret faucheur - attaquants, défenseurs
        ffra = 0
        ffrd = 0

        fret_alive = np.int64(0) # fret attaquant pillage

        # rapport de force
        pointa = 1        
        pointd = 1

        for la in bilan:
            # victoires
            if not len(la["attaquant"]["alive"]):
                vicd += 1
            if not len(la["defenseur"]["alive"]):
                vica += 1
            if len(la["attaquant"]["alive"]) and len(la["defenseur"]["alive"]):
                vicn += 1
            
            # pertes attaquants
            for vr in la["attaquant"]["dead"]:
                vr = sorted(vr, key= lambda a : a[0])
                wvr = [wr[0] for wr in vr ]
                x = 0
                while x < len(wvr):
                    w = wvr.count(wvr[x])
                    ress = eval(livaisseaux[vr[x][0]].replace(" ", "_"))().ress
                    apm += ress[0]*w*coef
                    apc += ress[1]*w*coef
                    apd += ress[2]*w*coef
                    cdrfm += ress[0]*w*coef
                    cdrfc += ress[1]*w*coef
                    cdrfd += ress[2]*w*coef
                    pointa += sum(ress)*w*coef
                    x += w             
            
            # pertes défenseurs
            for vrd in la["defenseur"]["dead"]:
                vrd = sorted(vrd, key = lambda a : a[0])
                wvrd = [wv[0] for wv in vrd]
                x = 0
                while x < len(vrd):
                    w = wvrd.count(wvrd[x])
                    vdd = eval(livaisseaux[vrd[x][0]].replace(" ", "_"))()
                    ress = vdd.ress
                    dpm += ress[0]*w*coef
                    dpc += ress[1]*w*coef
                    dpd += ress[2]*w*coef
                    if isinstance(vdd, Vaisseau) or isinstance(vdd, Satellite_solaire) or isinstance(vdd, Foreuse):
                        cdrfm += ress[0]*w*coef
                        cdrfc += ress[1]*w*coef
                        cdrfd += ress[2]*w*coef

                    if isinstance(vdd, Defense) and not isinstance(vdd, Satellite_solaire) and not isinstance(vdd, Foreuse):
                        cdrdm += ress[0]*w*coef
                        cdrdc += ress[1]*w*coef
                        cdrdd += ress[2]*w*coef
                    pointd += sum(ress)*w*coef
                    x += w 

            # survivants attaquants
            for asu in la["attaquant"]["alive"]:
                asux = eval(livaisseaux[asu[0]].replace(" ", "_"))()
                if asux.__class__.__name__ == "Faucheur":
                    ffra += asux.fret*coef
                fret_alive += asu[6]*coef
                pointa += sum(asux.ress)*coef

            # survivants défenseurs
            for dsu in la["defenseur"]["alive"]:
                dsux = eval(livaisseaux[dsu[0]].replace(" ", "_"))()
                if dsux.__class__.__name__ == "Faucheur":
                    ffrd += dsu[6]*coef
                pointd += sum(dsux.ress)*coef   
                
        # Popup résultat
        cbilan = Resultat()

        # rapport de force
        vpointa = (pointa-1)/len(bilan)
        vpointd = (pointd-1)/len(bilan)
        if vpointa > vpointd:
            if vpointd > 0:
                rap = "1 vs {}".format(round(vpointa/vpointd, 2)) 
            else:
                rap = "{} vs 0".format(vpointa)
        else:
            if vpointa > 0:
                rap = "1 vs {}".format(round(vpointd/vpointa, 2))
            else:
                rap = "0 vs {}".format(round(vpointa, 2))
        cbilan.enbr.text = "{0} rounds - Rapport de force : {1}".format(str(sum([x["rounds"] for x in bilan]) // len(bilan)+1), rap)
        

        # victoires
        cbilan.evica.text = "{} %".format(vica // len(bilan)*100)
        cbilan.evicd.text = "{} %".format(vicd // len(bilan)*100)
        cbilan.evicn.text = "{} %".format(vicn // len(bilan)*100)

        # pertes attaquants
        cbilan.eapm.text = format(apm//len(bilan), ",d")
        cbilan.eapc.text = format(apc//len(bilan), ",d")
        cbilan.eapd.text = format(apd//len(bilan), ",d")
        cbilan.eapt.text = format((apm+apc+apd)//len(bilan), ",d")

        # pertes défenseurs
        cbilan.edpm.text = format(dpm//len(bilan), ",d")
        cbilan.edpc.text = format(dpc//len(bilan), ",d")
        cbilan.edpd.text = format(dpd//len(bilan), ",d")
        cbilan.edpt.text = format((dpm+dpc+dpd)//len(bilan), ",d")

        # cdr initial
        met_cdr = int(cdrfm//len(bilan)*int(self.param.prc_cdr)/100 + cdrdm//len(bilan)*int(self.param.prc_defcdr)/100)
        cri_cdr = int(cdrfc//len(bilan)*int(self.param.prc_cdr)/100 + cdrdc//len(bilan)*int(self.param.prc_defcdr)/100)
        deut_cdr = int(cdrfd//len(bilan)*int(self.param.prc_cdr)/100 + cdrdd//len(bilan)*int(self.param.prc_defcdr)/100) if self.param.deut_cdr else 0
        total_cdr = met_cdr + cri_cdr + deut_cdr

        # faucheurs attaquants
        if ffra > 0:
            if ffra > total_cdr*int(self.param.limite_ff)/100:
                rffa = (met_cdr*int(self.param.limite_ff)/100, cri_cdr*int(self.param.limite_ff)/100, deut_cdr*int(self.param.limite_ff)/100)
            else:
                rffa = (met_cdr*ffra/total_cdr*int(self.param.limite_ff)/100, cri_cdr*ffra/total_cdr*int(self.param.limite_ff)/100)
        else:
            rffa = (0, 0, 0)

        # faucheurs défenseurs
        if ffrd > 0:
            if ffrd > total_cdr*int(self.param.limite_ff)/100:
                rffd = (met_cdr*int(self.param.limite_ff)/100, cri_cdr*int(self.param.limite_ff)/100, deut_cdr*int(self.param.limite_ff)/100)
            else:
                rffd = (met_cdr*ffrd/total_cdr*int(self.param.limite_ff)/100, cri_cdr*ffrd/total_cdr*int(self.param.limite_ff)/100, deut_cdr*ffrd/total_cdr*int(self.param.limite_ff)/100)
        else:
            rffd = (0, 0, 0)

        # cdr restant
        cbilan.emcdr.text = format(int(met_cdr - rffa[0] - rffd[0]), ",d")#format(int((dpm+apm)//len(bilan)*float(self.param.prc_cdr)-rffa[0]-rffd[0]), ",d")
        cbilan.eccdr.text = format(int(cri_cdr - rffa[1] - rffd[1]), ",d")#format(int((dpc+apc)//len(bilan)*float(self.param.prc_cdr)-rffa[1]-rffd[1]), ",d")        
        cbilan.edcdr.text = format(int(deut_cdr - rffa[2] - rffd[2]), ",d")
        cbilan.etcdr.text = format(int(total_cdr-sum(rffa)-sum(rffd)), ",d")
        cbilan.elune.text = "{} %".format(total_cdr//100000) if total_cdr//100000 < 21 else "20"

        # recyclage faucheur
        cbilan.lffa.text = "Les Faucheurs attaquants ont collecté :\n{0} unités de métal\n{1} unités de cristal\n{2} unités de deutérium".format(format(int(rffa[0]), ",d"), format(int(rffa[1]), ",d"), format(int(rffa[2]), ",d"))
        cbilan.lffd.text = "Les Faucheurs défenseurs ont collecté :\n{0} unités de métal\n{1} unités de cristal\n{2} unités de deutérium".format(format(int(rffd[0]), ",d"), format(int(rffd[1]), ",d"), format(int(rffd[2]), ",d"))
        
        # pillage
        if self.param.etrpp.text != "0" :
            prc_pi = (fret_alive-sum(rffa)) / int(self.param.etrpp.text.replace(",", ""))/len(bilan) if (fret_alive-sum(rffa)) / int(self.param.etrpp.text.replace(",", ""))/len(bilan) < 1  else 1
        else: 
            prc_pi = 1

        prmet = format(int(int(self.param.emrpp.text.replace(",", "")) * prc_pi), ",d")
        prcri = format(int(int(self.param.ecrpp.text.replace(",", "")) * prc_pi), ",d")
        prdeut = format(int(int(self.param.edrpp.text.replace(",", "")) * prc_pi), ",d")
        
        self.param.emrp.text = prmet
        self.param.ecrp.text = prcri
        self.param.edrp.text = prdeut

        cbilan.pillage.text = "Les attanquants ont pillé :\n{0} unités de métal\n{1} unités de cristal\n{2} unités de deutérium".format(prmet, prcri, prdeut)
        
        # benef
        bamet = - int(cbilan.eapm.text.replace(",", "")) + int(cbilan.emcdr.text.replace(",", "")) + int(prmet.replace(",", "")) + int(rffa[0])
        bacri = - int(cbilan.eapc.text.replace(",", "")) + int(cbilan.eccdr.text.replace(",", "")) + int(prcri.replace(",", "")) + int(rffa[1])
        badeut = - int(cbilan.eapd.text.replace(",", "")) + int(prdeut.replace(",", "")) + int(cbilan.eccdr.text.replace(",", "")) + int(rffa[2])#conso ? : - sum([int(a.econso.text.replace(",", "")) for a in self.attaquants.values])

        bdmet = - int(cbilan.edpm.text.replace(",", "")) + int(cbilan.emcdr.text.replace(",", "")) + int(rffd[0])
        bdcri = - int(cbilan.edpc.text.replace(",", "")) + int(cbilan.eccdr.text.replace(",", "")) + int(rffd[1])
        bddeut = - int(cbilan.edpd.text.replace(",", ""))+ int(cbilan.edcdr.text.replace(",", "")) + int(rffd[2])

        # attaquants
        cbilan.eabm.text = format(int(bamet), ",d")
        cbilan.eabc.text = format(int(bacri), ",d")
        cbilan.eabd.text = format(int(badeut), ",d")
        cbilan.eabt.text = format(int(bamet+bacri+badeut), ",d")

        # défenseurs
        cbilan.edbm.text = format(int(bdmet), ",d")
        cbilan.edbc.text = format(int(bdcri), ",d")
        cbilan.edbd.text = format(int(bddeut), ",d")
        cbilan.edbt.text = format(int(bdmet + bdcri + bddeut), ",d")

        # génération popup résultat
        resultat = Popup(title = "RESULTAT", content = cbilan, 
                         size_hint = (None, None), size = (900, 700))
        
        # génération popup recyclage
        self.make_recyclage(int((dpm+apm)//len(bilan)*float(self.param.prc_cdr))-rffa[0]-rffd[0], int((dpc+apc)//len(bilan)*float(self.param.prc_cdr))-rffa[1]-rffd[1])
        self.lia_resu = self.lia_resu[:self.attaquants.nvague]
        self.lia_resu.append(resultat)
        resultat.open()    

        # bilan
        info_bilan = {}
        info_bilan["cdr"] = [int(cbilan.emcdr.text.replace(",", "")), int(cbilan.eccdr.text.replace(",", ""))]
        info_bilan["pillage"] = [int(prmet.replace(",", "")), int(prcri.replace(",", "")), int(prdeut.replace(",", ""))]
        info_bilan["fret"] = {"attaquant" : {}, "defenseur" : {}}
        info_bilan["conso"] = {"attaquant" : {}, "defenseur" : {}}
        info_bilan["li_res"] = bilan

        for fa in self.attaquants.values:
            if self.attaquants.values.index(fa) not in info_bilan["fret"]["attaquant"]:
                info_bilan["fret"]["attaquant"][self.attaquants.values.index(fa)] = int(fa.efret.text.replace(",", ""))
                info_bilan["conso"]["attaquant"][self.attaquants.values.index(fa)] = int(fa.econso.text.replace(",", ""))
            else:
                info_bilan["fret"]["attaquant"][self.attaquants.values.index(fa)] += int(fa.efret.text.replace(",", ""))
                info_bilan["conso"]["attaquant"][self.attaquants.values.index(fa)] += int(fa.econso.text.replace(",", ""))

        for fd in self.defenseurs.values:
            if self.defenseurs.values.index(fd) not in info_bilan["fret"]["defenseur"]:
                info_bilan["fret"]["defenseur"][self.defenseurs.values.index(fd)] = int(fd.efret.text.replace(",", ""))
                info_bilan["conso"]["defenseur"][self.defenseurs.values.index(fd)] = int(fd.econso.text.replace(",", ""))
            else:
                info_bilan["fret"]["defenseur"][self.defenseurs.values.index(fd)] += int(fd.efret.text.replace(",", ""))
                info_bilan["conso"]["defenseur"][self.defenseurs.values.index(fd)] += int(fd.econso.text.replace(",", ""))                

        self.lia_bilan = self.lia_bilan[:self.attaquants.nvague] # effacement du précédent bilan de la vague si existant
        self.lia_bilan.append(info_bilan)
        self.bilan_vagues.maj_bilan(self.lia_bilan)


    def make_recyclage(self, metal, cristal):
        self.frecy = GridLayout(cols = 1)
        frest = GridLayout(rows = 1, size_hint = (1, None), height = 60)
        lrest = Label(text = "Champs de débris restant :")
        lrm = Label(text = format(int(metal), ",d"))
        lmr = Label(text = "M")
        lrc = Label(text = format(int(cristal), ",d"))
        lcr = Label(text = "C")
        frest.add_widget(lrest)
        frest.add_widget(lrm)
        frest.add_widget(lmr)
        frest.add_widget(lrc)
        frest.add_widget(lcr)
        self.frecy.add_widget(frest)

        self.trecy = GridLayout(cols = 2)
        self.frecy.add_widget(self.trecy)

        self.ratt = Recyclage("ATTAQUANTS", self.attaquants.values, self.defenseurs.values[0].fcoord.value, self.param.nb_gal, self.param.nb_ss, metal, cristal, self.param.conso_uni)
        self.rdef = Recyclage("DEFENSEURS", self.defenseurs.values, self.defenseurs.values[0].fcoord.value, self.param.nb_gal, self.param.nb_ss, metal, cristal, self.param.conso_uni)

        self.trecy.add_widget(self.ratt)
        self.trecy.add_widget(self.rdef)

        precy = Popup(title = "RECYCLAGE",  content = self.frecy, 
                      size_hint = (None, None), size = (900, 700))
        self.lia_recy.append(precy)
                        

    def maj_pillage(self, *arg):
        try:
            wdef = self.defenseurs.values[0].ressources
            self.param.emrpp.text = format(int(float(self.param.prc_pillage)/100*int(wdef.metal)), ",d")
            self.param.ecrpp.text = format(int(float(self.param.prc_pillage)/100*int(wdef.cristal)), ",d")
            self.param.edrpp.text = format(int(float(self.param.prc_pillage)/100*int(wdef.deuterium)), ",d")
            self.param.etrpp.text = format(int(float(self.param.prc_pillage)/100*(int(wdef.metal)+int(wdef.cristal)+int(wdef.deuterium))), ",d")
        except:
            pass

    def actu_pillage(self, *arg):
        try:
            self.param.liatt = [(x.finput.pseudo, x.ftechs.hyperespace, x.fdv_vitesse, self.param.prc_pillage) for x in self.attaquants.values]
            self.param.livai = self.attaquants.values[0].fflotte.vaisseaux

            def maj_tv(*arg):
                try:
                    for a in self.param.liatt:
                        if a[0] == self.param.bpjoueur.text :
                            i = self.param.liatt.index(a)
                    watt = self.attaquants.values[i]

                    wvai = eval("{}()".format(self.param.bpvaiss.text.replace(" ", "_")))
                    
                    wfret = wvai.tech_fretconso({"ally" : watt.fclasses.ally, "joueur" : watt.fclasses.classe}, 
                                                int(self.param.conso_uni), watt.fdv_vitesse, int(watt.ftechs.hyperespace))[1]

                    self.param.lpnb.text = "{}".format(format(int(int(self.param.etrpp.text.replace(",", ""))/wfret+1), ",d"))
                except:
                    pass

            self.param.dpvaiss.clear_widgets()
            for v in self.param.livai:
                btn = Label_Button(text = v, size_hint_y = None, height = 30)
                btn.bind(on_press = lambda btn: self.param.dpvaiss.select(btn.text))
                btn.bind(on_release = maj_tv)
                self.param.dpvaiss.add_widget(btn)

            self.param.dpjoueur.clear_widgets()
            for j in self.param.liatt:
                btn = Label_Button(text = j[0], size_hint_y = None, height = 30)
                btn.bind(on_press = lambda btn: self.param.dpjoueur.select(btn.text))
                self.param.dpjoueur.add_widget(btn)
                btn.bind(on_release = maj_tv)
        except:
            pass

    # temps de vols
    def maj_tvc(self, *arg):
        for j in self.attaquants.values + self.defenseurs.values[1:]:
            try:
                kvitesses = []
                kconso = 0
                kfret = 0
                for v in j.fflotte.vaisseaux:
                    if j.fflotte.vals[v].text != "" and int(j.fflotte.vals[v].text) > 0:
                        wtechs = eval("{}()".format(v.replace(" ", "_"))).with_tech(combat = {"arme" : int(j.ftechs.arme), "bouclier" : int(j.ftechs.bouclier), "protec" : int(j.ftechs.coque)}, 
                                                                                    vitesse = {"combu" : int(j.ftechs.combu), "impu" : int(j.ftechs.impu), "prop" : int(j.ftechs.prop)}, 
                                                                                    hyperespace = int(j.ftechs.hyperespace), 
                                                                                    classes = {"ally" : j.fclasses.ally, "joueur" : j.fclasses.classe}, 
                                                                                    meme_ally = False,
                                                                                    conso = int(self.param.conso_uni),
                                                                                    fdv = j.fdv_vitesse)                        
                        kvitesses.append(wtechs[1])
                        kconso += wtechs[3]*int(j.fflotte.vals[v].text)
                        kfret += wtechs[2]*int(j.fflotte.vals[v].text)

                kvitesse = min(kvitesses) if len(kvitesses) else 1

                kcdep = j.fcoord.value
                kcarr = self.defenseurs.values[0].fcoord.value
                
                if kcdep.split(" - ")[0] == kcarr.split(" - ")[0] :
                    if kcdep.split(" - ")[1] == kcarr.split(" - ")[1]:
                        if kcdep.split(" - ")[2] == kcarr.split(" - ")[2]:
                            # pos
                            j.econso.text = format(1 + round(kconso*(5/35000) * (int(j.fvit.vitesse)/100+1)**2), ",d")
                            j.etv.text = str(datetime.timedelta(seconds = round((10 + (35000/int(j.fvit.vitesse)*sqrt(5000/kvitesse))) / int(self.param.vitesse_uni)))).split(".")[0]
                        else: # ss
                            j.econso.text = format(1 + round(kconso * ((1000+ 5* (abs(int(kcdep.split(" - ")[2]) - int(kcarr.split(" - ")[2])))) / 35000) * (int(j.fvit.vitesse)/100+1)**2), ",d")
                            j.etv.text = str(datetime.timedelta(seconds = round((10 + (35000/int(j.fvit.vitesse)*sqrt((1000000+1000+ (abs(int(kcdep.split(" - ")[2]) - int(kcarr.split(" - ")[2]))) *5*5000)/kvitesse))) / int(self.param.vitesse_uni)))).split(".")[0]
                    else: # gal
                        j.econso.text = format(1 + round(kconso * ((2700 + 95 * (int(self.param.nb_ss) % abs(int(kcdep.split(" - ")[1]) - int(kcarr.split(" - ")[1]))))/35000) * (int(j.fvit.vitesse)/100+1)**2), ",d")
                        j.etv.text = str(datetime.timedelta(seconds = round((10 + (35000/int(j.fvit.vitesse)*sqrt((2700000+(int(self.param.nb_ss) % abs(int(kcdep.split(" - ")[1]) - int(kcarr.split(" - ")[1])))*95000)/kvitesse))) / int(self.param.vitesse_uni)))).split(".")[0]
                else: # uni
                    j.econso.text = format(1 + round(kconso * ((4 * (int(self.param.nb_gal) % abs(int(kcdep.split(" - ")[0]) - int(kcarr.split(" - ")[0]))))/7) * (int(j.fvit.vitesse)/100+1)**2), ",d")
                    j.etv.text = str(datetime.timedelta(seconds = round((10 + (35000/int(j.fvit.vitesse)*sqrt((int(self.param.nb_gal) % abs(int(kcdep.split(" - ")[0]) - int(kcarr.split(" - ")[0])))*20000000/kvitesse))) / int(self.param.vitesse_uni)))).split(".")[0]
            
                j.efret.text = format(int(kfret), ",d")

            except:
                pass


    def vague_suiv(self, *arg):
        self.attaquants.vague_suiv()
        self.defenseurs.vague_suiv()
        self.param.l_vague.text = "VAGUE {}".format(self.attaquants.nvague+1)


    def vague_prec(self, *arg):
        self.attaquants.afficher_vague(self.attaquants.nvague-1)
        self.defenseurs.afficher_vague(self.defenseurs.nvague-1)
        self.param.l_vague.text = "VAGUE {}".format(self.attaquants.nvague+1)



# Lancement
if __name__ == "__main__":
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    Ogfight().run()
