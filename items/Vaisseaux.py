# coding : utf-8


from math import ceil, floor
import random 

livaisseaux = ["Petit Transporteur", "Grand Transporteur", "Chasseur Leger", "Chasseur Lourd",
               "Croiseur", "Vaisseau de Bataille", "Vaisseau de Colo", "Recycleur", "Sonde",
               "Bombardier", "Destructeur", "RIP", "Traqueur", "Faucheur", "Eclaireur",
               "Lanceur de missiles", "Artillerie laser legere", "Artillerie laser lourde", 
               "Canon de Gauss", "Artillerie a ions", "Lanceur de plasma", "Petit bouclier",
               "Grand bouclier", "Satellite solaire", "Foreuse"]               


class Vaisseau:

    def __init__(self):
        self.ress = [0, 0, 0]
        self.structure = 0
        self.bouclier = 0
        self.attaque = 0

        self.vitesse = 0
        self.fret = 0
        self.conso = 0
        
        self.rf = {}

        self.sfdv = {}
        self.ffdv = {}
        self.bcl = {}

    def with_tech(self, combat = {"arme" : 0, "bouclier" : 0, "protec" : 0}, 
                        vitesse = {"combu" : 0, "impu" : 0, "prop" : 0}, 
                        hyperespace = 0, 
                        classes = {"ally" : "", "joueur" : ""}, 
                        meme_ally = False,
                        conso = 100,
                        fdv = {}):

        ncombat = self.tech_fight(combat, classes, fdv)
        nconso, nfret = self.tech_fretconso(classes, conso, fdv, hyperespace)
        nvitesse = self.tech_vitesse(vitesse, classes, meme_ally, fdv)

        return [ncombat, nvitesse, nfret, nconso]

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


    def tech_fretconso(self, classes, conso, fdv, hyperespace):
        # conso fret
        if classes["joueur"] == "Général":
            if conso == 50:
                reduc_classe = 0.5 * (1 + fdv["Renforcement du général des Mechas"]*0.002)
            if conso == 60:
                reduc_classe = 0.42 * (1 + fdv["Renforcement du général des Mechas"]*0.002)
            if conso == 70:
                reduc_classe = 0.36 * (1 + fdv["Renforcement du général des Mechas"]*0.002)
            if conso == 80:
                reduc_classe = 0.31 * (1 + fdv["Renforcement du général des Mechas"]*0.002)
            else:
                reduc_classe = 0.25 * (1 + fdv["Renforcement du général des Mechas"]*0.002)
            fret_classe = self.bcl["Général"]["fret"] if "Général" in self.bcl and "fret" in self.bcl["Général"] else 0
        else:
            if classes["joueur"] == "Collecteur":
                fret_classe =self.bcl["Collecteur"]["fret"] if "Collecteur" in self.bcl and "fret" in self.bcl["Collecteur"] else 0
                reduc_classe = 0
            else:
                fret_classe = 0
                reduc_classe = 0                
            

        nconso = floor(self.conso * conso/100 * (1 - reduc_classe) * (1 - (fdv["Récupération de chaleur"] + fdv["Module doptimisation"])*0.3))

        nfret = self.fret

        vbf = 0
        for vf in self.ffdv:
            vbf += fdv[vf]*self.ffdv[vf]
        for vvf in self.sfdv:
            vbf += fdv[vvf]*self.sfdv[vvf]

        bth = self.fret*5/100*hyperespace
        bcl = self.fret * fret_classe * (1+fdv["Renfort du collecteur Rocta"]*0.002)
        bfdv = self.fret * vbf
        nfret += bth + bcl + bfdv

        return (nconso, nfret)


    def tech_vitesse(self, vitesse, classes, meme_ally, fdv):
        pass

    def prepare_battle(self, combat = {"arme" : 0, "bouclier" : 0, "protec" : 0}, 
                             vitesse = {"combu" : 0, "impu" : 0, "prop" : 0}, 
                             hyperespace = 0, 
                             classes = {"ally" : "", "joueur" : ""}, 
                             meme_ally = False,
                             conso = 100,
                            fdv = {},
                            pseudo = ""):
        
        techs = self.with_tech(combat, vitesse, hyperespace, classes, meme_ally, conso, fdv)

        self.structure = techs[0]["protec"]
        self.bouclier = techs[0]["bouclier"]
        self.attaque = techs[0]["attaque"]

        self.w_structure = techs[0]["protec"]
        self.w_bouclier = techs[0]["bouclier"]
        self.marked_dead = False

        self.fret = techs[2]

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


        
class Petit_Transporteur(Vaisseau) :

    def __init__(self):
        super(Petit_Transporteur, self).__init__()
        self.ress = [2000, 2000, 0]
        self.structure = 4000
        self.bouclier = 10
        self.attaque = 5

        self.vitesse = 5000
        self.fret = 5000
        self.conso = 20

        self.priority = 1
        
        self.rf = {"Sonde" : 5,
                   "Satellite_solaire" : 5,
                   "Foreuse" : 5}

        
        self.sfdv = {}
        self.ffdv = {"Extension despace fret (vaisseaux civils)" : 0.004,
                     "Compresseur neuromodal" : 0.004}
        self.bcl = {"Collecteur" : {"fret" : 0.25}}


    def tech_vitesse(self, vitesse, classes, meme_ally, fdv):
        if vitesse["impu"] < 5:
            self.vitesse = 5000
            v_tra = self.vitesse * 0.1
            vb_tech = vitesse["combu"]
        else:
            cc_tra = 5000 * 0.1
            ci_tra = 10000 * 0.2 
            
            ccvi = 5000 * (1 + cc_tra*vitesse["combu"])
            civi = 10000 * (1+ci_tra*vitesse["impu"])

            if ccvi > civi:
                self.vitesse = 5000
                v_tra = self.vitesse * 0.1
                vb_tech = vitesse["combu"]  
            else:
                self.vitesse = 10000
                v_tra = self.vitesse * 0.2
                vb_tech = vitesse["impu"]                

        if classes["joueur"] == "Collecteur":
            vb_classe =  self.vitesse * (1 + fdv["Renfort du collecteur Rocta"]*0.002)
        else:
            vb_classe =  0
        vb_ally = self.vitesse * 0.1 if classes["ally"] == "Marchand" or meme_ally else 0

        vb_fdv = 0.002*fdv["Moteur à plasma"] + 0.005*fdv["Moteurs à fusion"]
        
        vsb = v_tra * vb_tech + self.vitesse * vb_fdv
        vb = vsb + vb_classe + vb_ally

        nvitesse = ceil(self.vitesse + vb)

        return nvitesse



class Grand_Transporteur(Vaisseau):

    def __init__(self):
        super(Grand_Transporteur, self).__init__()
        self.ress = [6000, 6000, 0]
        self.structure = 12000
        self.bouclier = 25
        self.attaque = 5

        self.vitesse = 7500
        self.fret = 25000
        self.conso = 50

        self.priority = 1

        self.rf = {"Sonde" : 5,
                   "Satellite_solaire" : 5,
                   "Foreuse" : 5}

        self.sfdv = {"Surcadençage (grand transporteur)" : 0.01}
        self.ffdv = {"Extension despace fret (vaisseaux civils)" : 0.004,
                     "Compresseur neuromodal" : 0.004}
        self.bcl = {"Collecteur" : {"fret" : 0.25}}


    def tech_vitesse(self, vitesse, classes, meme_ally, fdv):
        v_tra = self.vitesse * 0.1
        vb_tech = vitesse["combu"]


        if classes["joueur"] == "Collecteur":
            vb_classe =  self.vitesse * (1 + fdv["Renfort du collecteur Rocta"]*0.002)
        else:
            vb_classe =  0        
        vb_ally = self.vitesse * 0.1 if classes["ally"] == "Marchand" or meme_ally else 0

        # bonus fdv
        vb_fdv = 0.002*fdv["Moteur à plasma"] + 0.005*fdv["Moteurs à fusion"] + 0.01*fdv["Surcadençage (grand transporteur)"]

        vsb = v_tra * vb_tech + self.vitesse * vb_fdv
        vb = vsb + vb_classe + vb_ally

        nvitesse = ceil(self.vitesse + vb)        
        
        return nvitesse

     

class Chasseur_Leger(Vaisseau) :

    def __init__(self):
        super(Chasseur_Leger, self).__init__()
        self.ress = [3000, 1000, 0]
        self.structure = 4000
        self.bouclier = 10
        self.attaque = 50

        self.vitesse = 12500
        self.fret = 50
        self.conso = 20

        self.priority = 2

        self.rf = {"Sonde" : 5,
                   "Satellite_solaire" : 5,
                   "Foreuse" : 5}

        self.sfdv = {"Révision complète (chasseur léger)" : 0.003,
                     "Chasseur léger Mk II" : 0.003}
        self.ffdv = {}
        self.bcl = {}

        
    def tech_vitesse(self, vitesse, classes, meme_ally, fdv):
        v_tra = self.vitesse * 0.1 
        vb_tech = vitesse["combu"]

        if classes["joueur"] == "Général":
            vb_classe =  self.vitesse * (1 + fdv["Renforcement du général des Mechas"]*0.002)
        else:
            vb_classe =  0        

        vb_ally = self.vitesse * 0.1 if classes["ally"] == "Marchand" or meme_ally else 0

        # bonus fdv
        vb_fdv = 0.002*fdv["Moteur à plasma"] + 0.003*fdv["Révision complète (chasseur léger)"] + 0.003*fdv["Chasseur léger Mk II"]

        vsb = v_tra * vb_tech + self.vitesse * vb_fdv
        vb = vsb + vb_classe + vb_ally

        nvitesse = ceil(self.vitesse + vb)        

        return nvitesse



class Chasseur_Lourd(Vaisseau) :

    def __init__(self):
        super(Chasseur_Lourd, self).__init__()
        self.ress = [6000, 4000, 0]
        self.structure = 10000
        self.bouclier = 25
        self.attaque = 150

        self.vitesse = 10000
        self.fret = 100
        self.conso = 75

        self.priority = 2

        self.rf = {"Sonde" : 5,
                   "Satellite_solaire" : 5,
                   "Foreuse" : 5,
                   "Petit_Transporteur" : 3}

        self.sfdv = {"Renforcement à cristaux ioniques (chasseurs lourds)" : 0.003,
                     "Surcadençage (chasseur lourd)" : 0.003}
        self.ffdv = {}
        self.bcl = {}

    def tech_vitesse(self, vitesse, classes, meme_ally, fdv):   
        v_tra = self.vitesse * 0.2
        vb_tech = vitesse["impu"]

        if classes["joueur"] == "Général":
            vb_classe =  self.vitesse * (1 + fdv["Renforcement du général des Mechas"]*0.002)
        else:
            vb_classe =  0        
        vb_ally = self.vitesse * 0.1 if meme_ally else 0

        # bonus fdv
        vb_fdv = 0.002*fdv["Moteur à plasma"] + 0.003*fdv["Renforcement à cristaux ioniques (chasseurs lourds)"] + 0.003*fdv["Surcadençage (chasseur lourd)"]

        vsb = v_tra * vb_tech + self.vitesse * vb_fdv
        vb = vsb + vb_classe + vb_ally

        nvitesse = ceil(self.vitesse + vb)        

        return nvitesse


                
class Croiseur(Vaisseau):

    def __init__(self):
        super(Croiseur, self).__init__()
        self.ress = [20000, 7000, 2000]
        self.structure = 27000
        self.bouclier = 50
        self.attaque = 400

        self.vitesse = 15000
        self.fret = 800
        self.conso = 300

        self.priority = 2

        self.rf = {"Sonde" : 5,
                   "Satellite_solaire" : 5,
                   "Foreuse" : 5,
                   "Chasseur_Leger" : 6,
                   "Lanceur_de_missiles" : 10}

        self.sfdv = {"Révision complète (croiseur)" : 0.003,
                     "Croiseur Mk II" : 0.003}
        self.ffdv = {}
        self.bcl = {}

        
    def tech_vitesse(self, vitesse, classes, meme_ally, fdv):                        
        v_tra = self.vitesse * 0.2
        vb_tech = vitesse["impu"]

        if classes["joueur"] == "Général":
            vb_classe =  self.vitesse * (1 + fdv["Renforcement du général des Mechas"]*0.002)
        else:
            vb_classe =  0                    
        vb_ally = self.vitesse * 0.1 if meme_ally else 0

        # bonus fdv
        vb_fdv = 0.002*fdv["Moteur à plasma"] + 0.003*fdv["Révision complète (croiseur)"] + 0.003*fdv["Croiseur Mk II"]

        vsb = v_tra * vb_tech + self.vitesse * vb_fdv
        vb = vsb + vb_classe + vb_ally

        nvitesse = ceil(self.vitesse + vb)        

        return nvitesse



class Vaisseau_de_Bataille(Vaisseau) :

    def __init__(self):
        super(Vaisseau_de_Bataille, self).__init__()
        self.ress = [45000, 15000, 0]
        self.structure = 60000
        self.bouclier = 200
        self.attaque = 1000

        self.vitesse = 10000
        self.fret = 1500
        self.conso = 500
        
        self.priority = 3
        
        self.rf = {"Sonde" : 5,
                   "Satellite_solaire" : 5,
                   "Foreuse" : 5,
                   "Eclaireur" : 5}

        self.sfdv = {"Révision complète (vaisseau de bataille)" : 0.003,
                     "Surcadençage (vaisseau de bataille)" : 0.003}
        self.ffdv = {}
        self.bcl = {}

        
    def tech_vitesse(self, vitesse, classes, meme_ally, fdv):                                
        v_tra = self.vitesse * 0.3
        vb_tech = vitesse["prop"]

        if classes["joueur"] == "Général":
            vb_classe =  self.vitesse * (1 + fdv["Renforcement du général des Mechas"]*0.002)
        else:
            vb_classe =  0                    
        vb_ally = self.vitesse * 0.1 if meme_ally else 0

        # bonus fdv
        vb_fdv = 0.002*fdv["Moteur à plasma"] + 0.003*fdv["Révision complète (vaisseau de bataille)"] + 0.003*fdv["Surcadençage (vaisseau de bataille)"]

        vsb = v_tra * vb_tech + self.vitesse * vb_fdv
        vb = vsb + vb_classe + vb_ally

        nvitesse = ceil(self.vitesse + vb)        

        return nvitesse



class Vaisseau_de_Colo(Vaisseau) :

    def __init__(self):
        super(Vaisseau_de_Colo, self).__init__()
        self.ress = [10000, 20000, 10000]
        self.structure = 30000
        self.bouclier = 100
        self.attaque = 50

        self.vitesse = 2500
        self.fret = 7500
        self.conso = 1000

        self.priority = 1

        self.rf = {"Sonde" : 5,
                   "Satellite_solaire" : 5,
                   "Foreuse" : 5}

        self.sfdv = {}
        self.ffdv = {"Extension despace fret (vaisseaux civils)" : 0.004,
                     "Compresseur neuromodal" : 0.004}
        self.bcl = {}

        
    def tech_vitesse(self, vitesse, classes, meme_ally, fdv):                                
        v_tra = self.vitesse * 0.2
        vb_tech = vitesse["impu"]

        vb_classe =  self.vitesse if classes["joueur"] == "Général" else 0
        vb_ally = self.vitesse * 0.1 if meme_ally else 0

        # bonus fdv
        vb_fdv = 0.002*fdv["Moteur à plasma"] + 0.005*fdv["Moteurs à fusion"]

        vsb = v_tra * vb_tech + self.vitesse * vb_fdv
        vb = vsb + vb_classe + vb_ally

        nvitesse = ceil(self.vitesse + vb)        
        
        return nvitesse



class Recycleur(Vaisseau) :

    def __init__(self):
        super(Recycleur, self).__init__()
        self.ress = [10000, 6000, 2000]
        self.structure = 16000
        self.bouclier = 10
        self.attaque = 1

        self.vitesse = 2000
        self.fret = 20000
        self.conso = 900

        self.priority = 1

        self.rf = {"Sonde" : 5,
                   "Satellite_solaire" : 5,
                   "Foreuse" : 5}

        self.sfdv = {"Technique de recyclage expérimental" : 0.01}
        self.ffdv = {"Extension despace fret (vaisseaux civils)" : 0.004,
                     "Compresseur neuromodal" : 0.004}
        self.bcl = {"Général" : {"fret" : 0.2}}

        
    def tech_vitesse(self, vitesse, classes, meme_ally, fdv):
        if vitesse["impu"] < 17 and vitesse["prop"] < 15:
            self.vitesse = 2000
            v_tra = self.vitesse * 0.1
            vb_tech = vitesse["combu"]
        else:
            if vitesse["impu"] < 17:
                cc_tra = self.vitesse * 0.1
                cp_tra = self.vitesse * 0.3

                ccvi = self.vitesse * (1 + cc_tra*vitesse["combu"])
                cpvi = self.vitesse * (1 + cp_tra*vitesse["prop"])

                if ccvi > cpvi:
                    self.vitesse = 2000
                    v_tra = self.vitesse * 0.1
                    vb_tech = vitesse["combu"]
                else: 
                    self.vitesse = 6000
                    v_tra = self.vitesse * 0.3
                    vb_tech = vitesse["prop"]
            
            if vitesse["prop"] < 15:
                cc_tra = 2000 * 0.1
                ci_tra = 4000 * 0.2

                ccvi = self.vitesse * (1 + cc_tra*vitesse["combu"])
                civi = self.vitesse * (1 + ci_tra*vitesse["impu"])

                if ccvi > civi:
                    self.vitesse = 2000
                    v_tra = self.vitesse * 0.1
                    vb_tech = vitesse["combu"]
                else: 
                    self.vitesse = 4000
                    v_tra = self.vitesse * 0.2
                    vb_tech = vitesse["impu"]

            else:
                cc_tra = 2000 * 0.1
                ci_tra = 4000 * 0.2
                cp_tra = 6000 * 0.3

                ccvi = self.vitesse * (1 + cc_tra*vitesse["combu"])
                civi = self.vitesse * (1 + cc_tra*vitesse["impu"])
                cpvi = self.vitesse * (1 + cp_tra*vitesse["prop"])

                if max([ccvi, civi, cpvi]) == ccvi:
                    self.vitesse = 2000
                    v_tra = self.vitesse * 0.1
                    vb_tech = vitesse["combu"]
                if max([ccvi, civi, cpvi]) == civi:
                    self.vitesse = 4000
                    v_tra = self.vitesse * 0.2
                    vb_tech = vitesse["impu"]
                if max([ccvi, civi, cpvi]) == cpvi:
                    self.vitesse = 6000
                    v_tra = self.vitesse * 0.3
                    vb_tech = vitesse["prop"] 

        if classes["joueur"] == "Général":
            vb_classe =  self.vitesse * (1 + fdv["Renforcement du général des Mechas"]*0.002)
        else:
            vb_classe =  0                    
        vb_ally = self.vitesse * 0.1 if meme_ally else 0

        # bonus fdv
        vb_fdv = 0.002*fdv["Moteur à plasma"] + 0.005*fdv["Moteurs à fusion"] + 0.01*fdv["Technique de recyclage expérimental"]

        vsb = v_tra * vb_tech + self.vitesse * vb_fdv
        vb = vsb + vb_classe + vb_ally

        nvitesse = ceil(self.vitesse + vb)        
        
        return nvitesse



class Sonde(Vaisseau) :

    def __init__(self):
        super(Sonde, self).__init__()
        self.ress = [0, 1000, 0]
        self.structure = 1000
        self.bouclier = 0
        self.attaque = 0

        self.vitesse = 100000000
        self.fret = 0
        self.conso = 1

        self.priority = 1

        self.rf = {}

        self.sfdv = {}
        self.ffdv = {"Extension despace fret (vaisseaux civils)" : 0.004,
                     "Compresseur neuromodal" : 0.004}
        self.bcl = {}

        
    def tech_vitesse(self, vitesse, classes, meme_ally, fdv):
        v_tra = self.vitesse * 0.1 
        vb_tech = vitesse["combu"]

        if classes["joueur"] == "Général":
            vb_classe =  self.vitesse * (1 + fdv["Renforcement du général des Mechas"]*0.002)
        else:
            vb_classe =  0            
        vb_ally = self.vitesse * 0.1 if classes["ally"] == "Marchand" or meme_ally else 0

        # bonus fdv
        vb_fdv = 0.002*fdv["Moteur à plasma"] + 0.005*fdv["Moteurs à fusion"]

        vsb = v_tra * vb_tech + self.vitesse * vb_fdv
        vb = vsb + vb_classe + vb_ally

        nvitesse = ceil(self.vitesse + vb)        
        
        return nvitesse



class Bombardier(Vaisseau) :

    def __init__(self):
        super(Bombardier, self).__init__()
        self.ress = [50000, 25000, 15000]
        self.structure = 75000
        self.bouclier = 500
        self.attaque = 1000

        self.vitesse = 4000
        self.fret = 500
        self.conso = 700

        self.priority = 3

        self.rf = {"Sonde" : 5,
                   "Satellite_solaire" : 5,
                   "Foreuse" : 5,
                   "Lanceur_de_missiles" : 20,
                   "Artillerie_laser_legere" : 20,
                   "Artillerie_laser_lourde" : 10,
                   "Artillerie_a_ions" : 10,
                   "Canon_de_Gauss" : 5,
                   "Lanceur_de_plasma" : 5}

        self.sfdv = {"Bombardier Mk II" : 0.003,
                     "Révision complète (bombardier)" : 0.003}
        self.ffdv = {}
        self.bcl = {}

        
    def tech_vitesse(self, vitesse, classes, meme_ally, fdv):
        if vitesse["prop"] < 8:
            self.vitesse = 4000
            v_tra = self.vitesse * 0.2
            vb_tech = vitesse["impu"]
        else:
            ci = 4000*0.2
            cp = 5000*0.3

            civi = 4000 * (1 + ci*vitesse["impu"])
            cpvi = 5000 * (1 + cp*vitesse["prop"])

            if civi > cpvi:
                self.vitesse = 4000
                v_tra = self.vitesse * 0.2
                vb_tech = vitesse["impu"]
            else:
                self.vitesse = 5000
                v_tra = self.vitesse * 0.3
                vb_tech = vitesse["prop"]                

        if classes["joueur"] == "Général":
            vb_classe =  self.vitesse * (1 + fdv["Renforcement du général des Mechas"]*0.002)
        else:
            vb_classe =  0        
        vb_ally = self.vitesse * 0.1 if meme_ally else 0

        # bonus fdv
        vb_fdv = 0.002*fdv["Moteur à plasma"] + 0.003*fdv["Bombardier Mk II"] + 0.003*fdv["Révision complète (bombardier)"]

        vsb = v_tra * vb_tech + self.vitesse * vb_fdv
        vb = vsb + vb_classe + vb_ally

        nvitesse = ceil(self.vitesse + vb)        
  
        return nvitesse



class Destructeur(Vaisseau) :

    def __init__(self):
        super(Destructeur, self).__init__()
        self.ress = [60000, 50000, 15000]
        self.structure = 110000
        self.bouclier = 500
        self.attaque = 2000

        self.vitesse = 5000
        self.fret = 2000
        self.conso = 1000

        self.priority = 3

        self.rf = {"Sonde" : 5,
                   "Satellite_solaire" : 5,
                   "Foreuse" : 5,
                   "Artillerie_laser_legere" : 10,
                   "Traqueur" : 2}

        self.sfdv = {"Destructeur Mk II" : 0.003,
                     "Révision complète (destructeur)" : 0.003}
        self.ffdv = {}
        self.bcl = {}

        
    def tech_vitesse(self, vitesse, classes, meme_ally, fdv):
        v_tra = self.vitesse * 0.3
        vb_tech = vitesse["prop"]

        if classes["joueur"] == "Général":
            vb_classe =  self.vitesse * (1 + fdv["Renforcement du général des Mechas"]*0.002)
        else:
            vb_classe =  0                    
        vb_ally = self.vitesse * 0.1 if meme_ally else 0

        # bonus fdv
        vb_fdv = 0.002*fdv["Moteur à plasma"] + 0.003*fdv["Destructeur Mk II"] + 0.003*fdv["Révision complète (destructeur)"]

        vsb = v_tra * vb_tech + self.vitesse * vb_fdv
        vb = vsb + vb_classe + vb_ally

        nvitesse = ceil(self.vitesse + vb)
        
        return nvitesse



class RIP(Vaisseau) :

    def __init__(self):
        super(RIP, self).__init__()
        self.ress = [5000000, 4000000, 1000000]
        self.structure = 9000000
        self.bouclier = 50000
        self.attaque = 200000

        self.vitesse = 100
        self.fret = 1000000
        self.conso = 1

        self.priority = 4
        
        self.rf = {"Sonde" : 1250,
                   "Satellite_solaire" : 1250,
                   "Foreuse" : 1250,
                   "Chasseur_Leger" : 200,
                   "Chasseur_Lourd" : 100,
                   "Croiseur" : 33,
                   "Vaisseau_de_Bataille" : 30,
                   "Bombardier" : 25,
                   "Destructeur" : 5,
                   "Petit_Transporteur" : 250,
                   "Grand_Transporteur" : 250,
                   "Vaisseau_de_Colo" : 250,
                   "Recycleur" : 250,
                   "Traqueur" : 15,
                   "Eclaireur" : 30,
                   "Faucheur" : 10,
                   "Lanceur_de_missiles" : 200,
                   "Artillerie_laser_legere" : 200,
                   "Artillerie_laser_lourde" : 100,
                   "Artillerie_a_ions" : 100,
                   "Canon_de_Gauss" : 50}

        self.sfdv = {}
        self.ffdv = {}
        self.bcl = {}

        
    def tech_vitesse(self, vitesse, classes, meme_ally, fdv):
        v_tra = self.vitesse * 0.3
        vb_tech = vitesse["prop"]

        vb_classe =  self.vitesse if classes["joueur"] == "Général" else 0
        vb_ally = self.vitesse * 0.1 if meme_ally else 0

        vsb = v_tra * vb_tech
        vb = vsb + vb_classe + vb_ally

        nvitesse = ceil(self.vitesse + vb)        

        return nvitesse



class Traqueur(Vaisseau) :

    def __init__(self):
        super(Traqueur, self).__init__()
        self.ress = [30000, 40000, 15000]
        self.structure = 70000
        self.bouclier = 400
        self.attaque = 700

        self.vitesse = 10000
        self.fret = 750
        self.conso = 250

        self.priority = 4

        self.rf = {"Sonde" : 5,
                   "Satellite_solaire" : 5,
                   "Foreuse" : 5,
                   "Chasseur_Lourd" : 4,
                   "Croiseur" : 4,
                   "Vaisseau_de_Bataille" : 7,
                   "Petit_Transporteur" : 3,
                   "Grand_Transporteur" : 3}

        self.sfdv = {"Révision complète (traqueur)" : 0.003,
                     "Traqueur Mk II" : 0.003}
        self.ffdv = {}
        self.bcl = {}

        
    def tech_vitesse(self, vitesse, classes, meme_ally, fdv):
        v_tra = self.vitesse * 0.3
        vb_tech = vitesse["prop"]

        if classes["joueur"] == "Général":
            vb_classe =  self.vitesse * (1 + fdv["Renforcement du général des Mechas"]*0.002)
        else:
            vb_classe =  0                    
        vb_ally = self.vitesse * 0.1 if meme_ally else 0

        # bonus fdv
        vb_fdv = 0.002*fdv["Moteur à plasma"] + 0.003*fdv["Révision complète (traqueur)"] + 0.003*fdv["Traqueur Mk II"]

        vsb = v_tra * vb_tech + self.vitesse * vb_fdv
        vb = vsb + vb_classe + vb_ally

        nvitesse = ceil(self.vitesse + vb)
        
        return nvitesse



class Faucheur(Vaisseau) :

    def __init__(self):
        super(Faucheur, self).__init__()
        self.ress = [85000, 55000, 20000]
        self.structure = 140000
        self.bouclier = 700
        self.attaque = 2800

        self.vitesse = 7000
        self.fret = 10000
        self.conso = 1100

        self.priority = 3
        
        self.rf = {"Sonde" : 5,
                   "Satellite_solaire" : 5,
                   "Foreuse" : 5,
                   "Vaisseau_de_Bataille" : 7,
                   "Bombardier" : 4,
                   "Destructeur" : 3}

        self.sfdv = {}
        self.ffdv = {}
        self.bcl = {}

        
    def tech_vitesse(self, vitesse, classes, meme_ally, fdv):
        v_tra = self.vitesse * 0.3
        vb_tech = vitesse["prop"]

        if classes["joueur"] == "Général":
            vb_classe =  self.vitesse * (1 + fdv["Renforcement du général des Mechas"]*0.002)
        else:
            vb_classe =  0        
            
        vb_ally = self.vitesse * 0.1 if meme_ally else 0

       # bonus fdv
        vb_fdv = 0.002*fdv["Moteur à plasma"]

        vsb = v_tra * vb_tech + self.vitesse * vb_fdv
        vb = vsb + vb_classe + vb_ally

        nvitesse = ceil(self.vitesse + vb)

        return nvitesse



class Eclaireur(Vaisseau) :

    def __init__(self):
        super(Eclaireur, self).__init__()
        self.ress = [8000, 15000, 8000]
        self.structure = 230000
        self.bouclier = 100
        self.attaque = 200

        self.vitesse = 12000
        self.fret = 10000
        self.conso = 300

        self.priority = 2

        self.rf = {"Sonde" : 5,
                   "Satellite_solaire" : 5,
                   "Foreuse" : 5,
                   "Chasseur_Leger" : 3,
                   "Chasseur_Lourd" : 2,
                   "Croiseur" : 3}

        self.sfdv = {}
        self.ffdv = {}
        self.bcl = {"Général" : {"fret" : 0.2}}

        
    def tech_vitesse(self, vitesse, classes, meme_ally, fdv):
        v_tra = self.vitesse * 0.3
        vb_tech = vitesse["prop"]

        if classes["joueur"] == "Général":
            vb_classe =  self.vitesse * (1 + fdv["Renforcement du général des Mechas"]*0.002)
        else:
            vb_classe =  0                    
        vb_ally = self.vitesse * 0.1 if meme_ally else 0

       # bonus fdv
        vb_fdv = 0.002*fdv["Moteur à plasma"]

        vsb = v_tra * vb_tech + self.vitesse * vb_fdv
        vb = vsb + vb_classe + vb_ally

        nvitesse = ceil(self.vitesse + vb)

        return nvitesse

