# coding : utf-8

from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

from widgets import MyDropDown, Label_Button 
from items import Recycleur

import datetime
from math import sqrt

class Recyclage(GridLayout):
    def __init__(self, camp, vals, dest, nb_gal, nb_ss, metal, cristal, conso_uni, **kwargs):
        super(Recyclage, self).__init__(**kwargs)
        self.cols = 1
        self.add_widget(Label(text = camp, size_hint = (1, None), height = 60))
        self.add_widget(Label(text = "Sélectionner un joueur :", size_hint = (1, None), height = 30))

        self.boxa = MyDropDown()
        for a in vals:
            btn = Label_Button(text = "{0} / hyperespace {1} / {2}".format(a.finput.pseudo, a.ftechs.hyperespace, a.fcoord.value), size_hint_y = None, height = 30)
            btn.bind(on_release = lambda btn: self.boxa.select(btn.text))
            self.boxa.add_widget(btn)
        
        self.b_boxa = Button(text = "", size_hint = (1, None), height = 30)
        self.b_boxa.bind(on_release = self.boxa.open)        
        self.boxa.bind(on_select = lambda instance, x: setattr(self.b_boxa, 'text', x))

        self.rwconso = 0
        self.rwfret = 0
        self.rwvit = 0
        self.cdep = ""
        self.carr = dest
        #
        def make_recycleur(*arg):
            texte = self.b_boxa.text
            for at in vals:   
                if at.finput.pseudo == texte.split(" / ")[0]:
                    if at.ftechs.hyperespace == texte.split(" / ")[1].split("hyperespace ")[1]:
                        if at.fcoord.value == texte.split(" / ")[2]:
                            self.cdep = at.fcoord.value
                            recycleur = Recycleur()
                            self.rwconso, self.rwfret = recycleur.tech_fretconso({"ally" : at.fclasses.ally, "joueur" : at.fclasses.classe}, int(conso_uni), at.fdv_vitesse, int(at.ftechs.hyperespace))
                            self.rwvit = recycleur.tech_vitesse({"combu" : int(at.ftechs.combu), "impu" : int(at.ftechs.impu), "prop" : int(at.ftechs.prop)}, {"ally" : at.fclasses.ally, "joueur" : at.fclasses.classe}, False, at.fdv_vitesse)
                            # vitesses
                            self.boxvit.clear_widgets()
                            self.bvit.text = ""
                            if at.fclasses.classe == "Général":
                                for x in range(20):
                                    btn = Label_Button(text = str(100-(x*5)), size_hint_y = None, height = 30)
                                    btn.bind(on_release = lambda btn: self.boxvit.select(btn.text))
                                    self.boxvit.add_widget(btn)
                            else:
                                for x in range(10):
                                    btn = Label_Button(text = str(100-(x*10)), size_hint_y = None, height = 30)
                                    btn.bind(on_release = lambda btn: self.boxvit.select(btn.text))
                                    self.boxvit.add_widget(btn)

                            self.rmax.text = format(int((metal+cristal)//self.rwfret+1), ",d")
        
        self.add_widget(self.b_boxa)

        self.fvc = GridLayout(cols = 2, size_hint = (1, None), height = 300, spacing=  [0, 10], padding = [0, 20])
        lvit = Label(text = "Vitesse de vol : ", size_hint = (1, None), height = 30)
        
        self.boxvit = MyDropDown()
        self.bvit = Button(text = "", size_hint = (None, None), size = (40, 30))

        lnb = Label(text = "Nombre : ", size_hint = (1, None), height = 30)
        self.enbr = TextInput(size_hint = (1, None), height = 30)

        lrmax = Label(text = "Nombre max. : ", size_hint = (1, None), height = 30)
        self.rmax = Label(text = "0", size_hint = (1, None), height = 30)

        lrcdr = Label(text = "CDR théorique : ")
        self.rcdr = Label(text = "")

        lcon = Label(text = "Consommation :")
        self.econ = Label(text = "")

        ltv = Label(text = "Temps de vol : ")
        self.etv = Label(text = "")

        def maj_cyclo(*arg):
            try:
                ft = self.rwfret * int(self.enbr.text)
            except:
                ft = 0

            tcdr = metal + cristal
            if ft >= tcdr:
                wrm = metal
                wrc = cristal
            else:
                wrm = int(metal / (metal + cristal) * ft)+1
                wrc = int(cristal / (metal + cristal) * ft)
            self.rcdr.text = "{0} métal et {1} cristal".format(format(wrm, ",d"), format(wrc, ",d"))

            try:
                if self.cdep.split(" - ")[0] == self.carr.split(" - ")[0] :
                    if self.cdep.split(" - ")[1] == self.carr.split(" - ")[1]:
                        if self.cdep.split(" - ")[2] == self.carr.split(" - ")[2]:
                            # pos
                            self.econ.text = format(1 + round(self.rwconso*int(self.enbr.text)*(5/35000) * (int(self.bvit.text)/100+1)**2), ",d")
                            self.etv.text = str(datetime.timedelta(seconds = round((10 + (35000/int(self.bvit.text)*sqrt(5000/self.rwvit))) / int(self.param.vitesse_uni)))).split(".")[0]
                        else: # ss
                            self.econ.text = format(1 + round(self.rwconso*int(self.enbr.text) * ((1000+ 5* (abs(int(self.cdep.split(" - ")[2]) - int(self.carr.split(" - ")[2])))) / 35000) * (int(self.bvit.text)/100+1)**2), ",d")
                            self.etv.text = str(datetime.timedelta(seconds = round((10 + (35000/int(self.bvit.text)*sqrt((1000000+1000+ (abs(int(self.cdep.split(" - ")[2]) - int(self.carr.split(" - ")[2]))) *5*5000)/self.rwvit))) / int(self.param.vitesse_uni)))).split(".")[0]
                    else: # gal
                        self.econ.text = format(1 + round(self.rwconso*int(self.enbr.text) * ((2700 + 95 * (int(nb_ss) % abs(int(self.cdep.split(" - ")[1]) - int(self.carr.split(" - ")[1]))))/35000) * (int(self.bvit.text)/100+1)**2), ",d")
                        self.etv.text = str(datetime.timedelta(seconds = round((10 + (35000/int(self.bvit.text)*sqrt((2700000+(int(nb_ss) % abs(int(self.cdep.split(" - ")[1]) - int(self.carr.split(" - ")[1])))*95000)/self.rwvit))) / int(self.param.vitesse_uni)))).split(".")[0]
                else: # uni
                    self.econ.text = format(1 + round(self.rwconso*int(self.enbr.text) * ((4 * (int(nb_gal) % abs(int(self.cdep.split(" - ")[0]) - int(self.carr.split(" - ")[0]))))/7) * (int(self.bvit.text)/100+1)**2), ",d")
                    self.etv.text = str(datetime.timedelta(seconds = round((10 + (35000/int(self.bvit.text)*sqrt((int(nb_gal) % abs(int(self.cdep.split(" - ")[0]) - int(self.carr.split(" - ")[0])))*20000000/self.rwvit))) / int(self.param.vitesse_uni)))).split(".")[0]
            except:
                pass


        self.fvc.add_widget(lvit)
        self.fvc.add_widget(self.bvit)
        self.fvc.add_widget(lnb)
        self.fvc.add_widget(self.enbr)
        self.fvc.add_widget(lrmax)
        self.fvc.add_widget(self.rmax)
        self.fvc.add_widget(lrcdr)
        self.fvc.add_widget(self.rcdr)
        self.fvc.add_widget(lcon)
        self.fvc.add_widget(self.econ)
        self.fvc.add_widget(ltv)
        self.fvc.add_widget(self.etv)

        self.enbr.bind(text = maj_cyclo)
        self.bvit.bind(text = maj_cyclo)

        self.add_widget(self.fvc)
        
        self.b_boxa.bind(text =  make_recycleur)
        self.bvit.bind(on_release = self.boxvit.open)        
        self.boxvit.bind(on_select=lambda instance, x: setattr(self.bvit, 'text', x))