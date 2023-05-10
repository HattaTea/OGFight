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
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView

from items import *

class Bilan_vagues(Popup):

    def __init__(self, **kwargs):
        super(Bilan_vagues, self).__init__(**kwargs)

        self.title = "Bilan"
        self.content = GridLayout(cols = 1)
        self.size = (900, 700)
        self.size_hint = (None, None)

        self.ftabs = GridLayout(cols = 2, size_hint = (1, None), height = 60)
        self.b_att = Button(text = "ATTAQUANTS")
        self.b_att.bind(on_press = self.switch)
        self.b_def = Button(text = "DEFENSEURS")
        self.b_def.bind(on_press = self.switch)
        self.faff = GridLayout(cols = 1)

        self.ftabs.add_widget(self.b_att)
        self.ftabs.add_widget(self.b_def)
        self.content.add_widget(self.ftabs)
        self.content.add_widget(self.faff)

        self.f_att = GridLayout(cols = 1)
        self.f_def = GridLayout(cols = 1)

        self.values = []

    def open(self, *arg):
        self.maj_bilan()
        super().open(*arg)

    def switch(self, ins):
        if ins == self.b_att and self.faff.children[0] != self.f_att:
            self.faff.clear_widgets()
            self.faff.add_widget(self.f_att)
        if ins == self.b_def and self.faff.children[0] != self.f_def:
            self.faff.clear_widgets()
            self.faff.add_widget(self.f_def)
            

    def maj_bilan(self, *arg):
        #print("\nli_res :\n", li_res, "\n/\n")
        self.f_att.clear_widgets()
        self.f_def.clear_widgets()
        self.faff.clear_widgets()
        
        # PERTES
        dic_att = {}
        dic_def = {}
        dica_att = {}
        dica_def = {}
        pillage = [0, 0, 0]
        dic_conso = {}
        for r in self.values:
            vatt = {}
            vdef = {}
            vatta = {}
            vdefa = {}
            for p in range(len(r["pillage"])):
                pillage[p] += r["pillage"][p]            

            for s in r["li_res"]:
                for ata in s["attaquant"]["alive"]:
                    kata = eval(livaisseaux[ata[0]].replace(" ", "_"))().ress
                    if r["names"]["attaquant"][ata[7]] not in vatta:
                        vatta[r["names"]["attaquant"][ata[7]]] = sum(kata)*r["coef"]
                    else:
                        vatta[r["names"]["attaquant"][ata[7]]] += sum(kata)*r["coef"]

                for raa in s["attaquant"]["dead"]:
                    for ra in raa:
                        kra = eval(livaisseaux[ra[0]].replace(" ", "_"))().ress
                        if r["names"]["attaquant"][ra[7]] not in vatt:
                            vatt[r["names"]["attaquant"][ra[7]]] = {"metal" : 0, "cristal" : 0, "deut" : 0}
                        vatt[r["names"]["attaquant"][ra[7]]]["metal"] += kra[0]*r["coef"]
                        vatt[r["names"]["attaquant"][ra[7]]]["cristal"] += kra[1]*r["coef"]
                        vatt[r["names"]["attaquant"][ra[7]]]["deut"] += kra[2]*r["coef"]

                for dea in s["defenseur"]["alive"]:
                    kdea = eval(livaisseaux[dea[0]].replace(" ", "_"))().ress
                    if r["names"]["defenseur"][dea[7]] not in vdefa:
                        vdefa[r["names"]["defenseur"][dea[7]]] = sum(kdea)*r["coef"]
                    else:
                        vdefa[r["names"]["defenseur"][dea[7]]] += sum(kdea)*r["coef"]

                for rdd in s["defenseur"]["dead"]:
                    for rd in rdd:
                        krd = eval(livaisseaux[rd[0]].replace(" ", "_"))().ress
                        if r["names"]["defenseur"][rd[7]] not in vdef:
                            vdef[r["names"]["defenseur"][rd[7]]] = {"metal" : 0, "cristal" : 0, "deut" : 0}
                        vdef[r["names"]["defenseur"][rd[7]]]["metal"] += krd[0]*r["coef"]
                        vdef[r["names"]["defenseur"][rd[7]]]["cristal"] += krd[1]*r["coef"]
                        vdef[r["names"]["defenseur"][rd[7]]]["deut"] += krd[2]*r["coef"]

            for ats in vatta:
                vatta[ats] = round(vatta[ats] / len(r["li_res"]))
            for des in vdefa:
                vdefa[des] = round(vdefa[des] / len(r["li_res"]))

            for a in vatt:
                for rc in vatt[a]:
                    vatt[a][rc] = round(vatt[a][rc] / len(r["li_res"])) - r["conso"]["attaquant"][r["names"]["attaquant"].index(a)]*r["coef"] if rc == "deut" else  round(vatt[a][rc] / len(r["li_res"]))
            for d in vdef:
                for rcs in vdef[d]:
                    vdef[d][rcs] = round(vdef[d][rcs] / len(r["li_res"])) - r["conso"]["defenseur"][r["names"]["defenseur"].index(d)]*r["coef"] if rcs == "deut" else round(vdef[d][rcs] / len(r["li_res"]))

            for tc in r["conso"]:
                for c in r["conso"][tc]:
                    if c not in dic_conso:
                        dic_conso[c] = r["conso"][tc][c]*r["coef"]
                    else:
                        dic_conso[c] += r["conso"][tc][c]*r["coef"]

            for attas in vatta:
                if attas not in dica_att:
                    dica_att[attas] = vatta[attas]
                else:
                    dica_att[attas] += vatta[attas]

            for defes in vdefa:
                if defes not in dica_def:
                    dica_def[defes] = vdefa[defes]
                else:
                    dica_def[defes] += vdefa[defes]

            for aa in vatt:
                if aa not in dic_att:
                    dic_att[aa] = vatt[aa]
                else:
                    #dic_att[aa] += vatt[aa]
                    for r in dic_att[aa]:
                        dic_att[aa][r] += vatt[aa][r]

            for dd in vdef:
                if dd not in dic_def:
                    dic_def[dd] = vdef[dd]
                else:
                    #dic_def[dd] += vdef[dd]
                    for rr in dic_def[dd]:
                        dic_def[dd][rr] += vdef[dd][rr]

        # PILLAGES
        pondpi = {}

        for ha in dic_att:
            if ha not in pondpi:
                pondpi[ha] = sum([dic_att[ha][t] for t in dic_att[ha]])
            else:
                pondpi[ha] += sum([dic_att[ha][t] for t in dic_att[ha]])
        for haa in dica_att:
            if haa in pondpi:
                pondpi[haa] += dica_att[haa]
            else:
                pondpi[haa] = dica_att[haa]
        
        maxpond = sum([pondpi[k] for k in pondpi])

        pondpij = {}
        for j in pondpi:
            pondpij[j] = [round(pondpi[j] / maxpond * pillage[pp]) for pp in range(len(pillage))]

        # TABLEAUX
        ent = ["JOUEUR", "CONSO", "PERTES", "PILLAGE", "BENEF PAR JOUEUR"]
        fenta = GridLayout(cols = len(ent), size_hint = (1, None), height = 60)
        fentd = GridLayout(cols = len(ent), size_hint = (1, None), height = 60)
        for e in range(len(ent)):
            fenta.add_widget(Label(text = ent[e]))
            fentd.add_widget(Label(text = ent[e]))
        self.f_att.add_widget(fenta)
        self.f_def.add_widget(fentd)

        scrolla = ScrollView()
        scrolld = ScrollView()

        faffa = GridLayout(cols = len(ent))
        faffd = GridLayout(cols = len(ent))
        
        scrolla.add_widget(faffa)
        self.f_att.add_widget(scrolla)
        scrolld.add_widget(faffd)
        self.f_def.add_widget(scrolld)

        # att
        liatt = []
        for oa in dic_att:
            if oa not in liatt:
                liatt.append(oa)
        for oaa in dica_att:
            if oaa not in liatt:
                liatt.append(oaa)

        fnoms_att = GridLayout(rows = len(liatt))
        fcon = GridLayout(rows = len(liatt))
        fperj = GridLayout(rows = len(liatt))
        fpil = GridLayout(rows = len(liatt))
        fben = GridLayout(rows = 1)

        for ia in liatt:
            fnoms_att.add_widget(Label(text = str(ia), size_hint = (1, None), height = 100))

            fcon.add_widget(Label(text = format(dic_conso[r["names"]["attaquant"].index(ia)], ",d"), size_hint = (1, None), height = 100))

            fper = GridLayout(rows = 3, size_hint = (1, None), height = 100)
            txper = [0, 0, 0]
            itxp = 0
            if ia in dic_att:
                for tpr in dic_att[ia]:
                    fper.add_widget(Label(text = format(dic_att[ia][tpr], ",d")))
                    txper[itxp] += dic_att[ia][tpr]
                    itxp += 1
            else:
                for tpr in range(3):
                    fper.add_widget(Label(text = "0"))
            fperj.add_widget(fper)

            fpilj = GridLayout(rows = 3, size_hint = (1, None), height = 100)
            txpill = [0, 0, 0]
            itxl = 0
            for tpi in pondpij[ia]:
                fpilj.add_widget(Label(text = format(tpi, ",d")))
                txpill[itxl] += tpi
                itxl += 1

            fpil.add_widget(fpilj)

        # benef
        # cdr 
        txcdr = [0, 0, 0]
        vtxcdr = [cr["cdr"] for cr in self.values]
        for v in vtxcdr:
            txcdr[0] += v[0]
            txcdr[1] += v[1]
            txcdr[2] += v[2]

        
        fbenj = GridLayout(rows = 3, size_hint = (1, None), height = 100)
        for b in range(3):
            fbenj.add_widget(Label(text = format(round(int(txcdr[b] + txpill[b] - txper[b])/len(liatt)), ",d")))
        fben.add_widget(fbenj)
        
        faffa.add_widget(fnoms_att)
        faffa.add_widget(fcon)
        faffa.add_widget(fperj)
        faffa.add_widget(fpil)
        faffa.add_widget(fben)
        faffa.size_hint = (1, None)
        faffa.height = len(liatt) * 105

        self.faff.add_widget(self.f_att)

        # def
        lidef = []
        for od in dic_def:
            if od not in lidef:
                lidef.append(od)
        for odd in dica_def:
            if odd not in lidef:
                lidef.append(odd)

        fnoms_def = GridLayout(rows = len(lidef))
        fcond = GridLayout(rows = len(lidef))
        fperjd = GridLayout(rows = len(lidef))
        fpild = GridLayout(rows = len(lidef))
        fbend = GridLayout(rows = 1)

        for ide in lidef:
            fnoms_def.add_widget(Label(text = str(ide), size_hint = (1, None), height = 100))

            fcond.add_widget(Label(text = format(dic_conso[r["names"]["defenseur"].index(ide)], ",d"), size_hint = (1, None), height = 100))
            
            fperd = GridLayout(rows = 3, size_hint = (1, None), height = 100)
            txperd = [0, 0, 0]
            itxpd = 0
            if ide in dic_def:
                for tpr in dic_def[ide]:
                    fperd.add_widget(Label(text = format(dic_def[ide][tpr], ",d")))
                    txperd[itxpd] += dic_def[ide][tpr]
                    itxpd += 1
            else:
                for tpr in range(3):
                    fperd.add_widget(Label(text = "0"))
            fperjd.add_widget(fperd)


        fbenjd = GridLayout(rows = 3, size_hint = (1, None), height = 100)
        for b in range(3):
            fbenjd.add_widget(Label(text = format(round(int(txcdr[b] - txperd[b])/len(lidef)), ",d")))
        fbend.add_widget(fbenjd)
        
        faffd.add_widget(fnoms_def)
        faffd.add_widget(fcond)
        faffd.add_widget(fperjd)
        faffd.add_widget(fpild)
        faffd.add_widget(fbend)
        faffd.size_hint = (1, None)
        faffd.height = len(lidef) * 105
