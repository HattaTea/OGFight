# coding : utf-8

from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button

from .Coords import Coords
from .Jinput import Jinput
from .Classes import Classes
from .Technos import Technos
from .Aflotte import Aflotte
from .Dflotte import Dflotte
from .Ressources_defenseur import Ressources_defenseur
from .VitesseVol import VitesseVol
from .Fdv_manuel import Fdv_manuel 


class Attaquant(GridLayout):
    def __init__(self, num, defenseur = False, **kwargs):
        super(Attaquant, self).__init__(**kwargs)
        self.cols = 1
        self.fsvatt = ScrollView(bar_width='2dp', smooth_scroll_end=15)
        self.fvatt = GridLayout(cols = 1, size_hint = (1, None), height = 1300 if not defenseur else 1700, spacing = [0, 20])

        self.finput = Jinput(num)

        self.fclasses = Classes()
        self.fclasses.bind(ally = self.maj_tvc)
        self.fclasses.bind(classe = self.maj_tvc)

        self.ftechs = Technos()
        self.ftechs.bind(combu = self.maj_tvc)
        self.ftechs.bind(impu = self.maj_tvc)
        self.ftechs.bind(prop = self.maj_tvc)
        self.ftechs.bind(hyperespace = self.maj_tvc)

        self.fflotte = Aflotte() if not defenseur else Dflotte()
        for wa in self.fflotte.vals:
            self.fflotte.vals[wa].bind(text = self.maj_tvc)

        if defenseur:
            self.ressources = Ressources_defenseur()
        
        self.ftechs.go_nextab = self.fflotte.recieve_focus

        self.fcoord = Coords("Coordonnées de départ :")
        self.fcoord.bind(value = self.maj_tvc)
        
        self.fvit =VitesseVol()
        self.fvit.bind(vitesse = self.maj_tvc)

        self.fvol = GridLayout(rows = 3, spacing = [0, 5])
        self.ftv = GridLayout(cols = 2, size_hint = (1, None), height = 30)
        self.ltv = Label(text = "Temps de vol : ")
        self.etv = Label(text = "")
        self.ftv.add_widget(self.ltv)
        self.ftv.add_widget(self.etv)
        self.fvol.add_widget(self.ftv)

        self.fconso = GridLayout(cols = 2, size_hint = (1, None), height = 30)
        self.lconso = Label(text = "Consommation : ")
        self.econso = Label(text = "0")
        self.fconso.add_widget(self.lconso)
        self.fconso.add_widget(self.econso)
        self.fvol.add_widget(self.fconso)

        self.ffret = GridLayout(cols = 2, size_hint = (1, None), height = 30)
        self.lfret = Label(text = "Fret : ")
        self.efret = Label(text = "0")
        self.ffret.add_widget(self.lfret)
        self.ffret.add_widget(self.efret)
        self.fvol.add_widget(self.ffret)

        self.b_fdv = Button(text = "Formes de vie", size_hint = (1, None), height = 40)
        self.cfdv = Fdv_manuel()
        def setm_fdv(*arg):
            self.fdv_vitesse = self.cfdv.fdv        
        self.cfdv.bind(fdv = setm_fdv)
        self.b_fdv.bind(on_press = self.cfdv.open)


        self.fvatt.add_widget(self.finput)
        self.fvatt.add_widget(self.fclasses)
        self.fvatt.add_widget(self.ftechs)
        self.fvatt.add_widget(self.fflotte)
        if defenseur:
            self.fvatt.add_widget(self.ressources)
        self.fvatt.add_widget(self.fcoord)
        if not defenseur:
            self.fvatt.add_widget(self.fvit)
            self.fvatt.add_widget(self.fvol)
        self.fvatt.add_widget(self.b_fdv)

        self.fsvatt.add_widget(self.fvatt)
        self.add_widget(self.fsvatt)      
         
        
        
        # import re
        def importer_re(res):    
            self.fclasses.boxally.set(res[0]["Classe dalliance"])
            self.fclasses.boxclass.set(res[0]["Classe"]) 

            self.ftechs.earme.text = str(res[5]["Technologie Armes"])
            self.ftechs.ebou.text = str(res[5]["Technologie Bouclier"])
            self.ftechs.ecoque.text = str(res[5]["Technologie Protection des vaisseaux spatiaux"])

            self.ftechs.ecombu.text = str(res[5]["Réacteur à combustion"])
            self.ftechs.eimpu.text = str(res[5]["Réacteur à impulsion"])
            self.ftechs.eprop.text = str(res[5]["Propulsion hyperespace"])
            self.ftechs.ehyper.text = str(res[5]["Technologie hyperespace"])

            try:
                self.fcoord.galaxie.text = res[0]["coord"].split(":")[0]
                self.fcoord.ss.text = res[0]["coord"].split(":")[1]
                self.fcoord.position = res[0]["coord"].split(":")[2]
            except:
                pass

            for v in self.fflotte.avaisseaux:
                for a in res[2]:              
                    vmod = ["Vaisseau de colonisation", "Sonde despionnage", "Étoile de la mort"]        
                    if a in vmod:                  
                        if a == "Vaisseau de colonisation":
                            b = "Vaisseau de Colo"
                        elif a == "Sonde despionnage":
                            b = "Sonde"
                        elif a == "Étoile de la mort" :
                            b = "RIP"              
                    else :
                        b = a      
                    if b.lower().replace("é", "e").replace("è", "e").replace("à", "a") == v.lower():
                        self.fflotte.vals[v].text = str(res[2][a])
                for a in res[3]:
                    vmod = ["Vaisseau de colonisation", "Sonde despionnage", "Étoile de la mort"]        
                    if a in vmod:            
                        if a == "Vaisseau de colonisation":
                            b = "Vaisseau de Colo"
                        if a == "Sonde despionnage":
                            b = "Sonde"
                        if a == "Étoile de la mort" :
                            b = "RIP"              
                    else :
                        b = a      
                    if b.lower().replace("é", "e").replace("è", "e").replace("à", "a") == v.lower():
                        self.fflotte.vals[v].text = str(res[3][a])

            for tf in res[7]:
                if tf in self.cfdv.vals:
                    self.cfdv.vals[tf].text = str(res[7][tf])


            fdv = False
            for t in res[7]:
                if res[7][t] > 0:
                    fdv = True
            self.finput.espio.lab_fdv.text = "FDV chargées"
            if fdv:
                for t in self.fdv_vitesse:
                    self.fdv_vitesse[t] = res[7][t]
            # afficher set
        def reset(*arg):
            self.fdv_vitesse = {"Renforcement du général des Mechas" : 0,
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
                                "Intensification du bouclier à lobsidienne" : 0}        
            self.finput.espio.lab_fdv.text = "Aucune données"

        reset()

        self.finput.importer = importer_re
        self.finput.espio.get = self.finput.importer
        self.finput.espio.reset = reset

    def maj_tvc(self, *arg):
        pass