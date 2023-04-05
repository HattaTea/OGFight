# coding : utf-8

from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label


class Espio_Input(GridLayout):

    def __init__(self, **kwargs):
        super(Espio_Input, self).__init__(**kwargs)

        self.cols = 2
        self.size_hint = (1, None)
        self.height = 90
        self.input = TextInput(text = "Copier/Coller l'intégralité du RE ici")
        
        self.fbut = GridLayout(rows = 3, size_hint = (0.4, 1))
        self.lab_fdv = Label(text = "Aucune données")
        self.b_reset = Button(text = "Effacer")
        self.b_reset.bind(on_release = self.reset)
        self.valid = Button(text = "Importer")#, size_hint = (0.2, None), height = 30)
        self.valid.bind(on_press = self.get_text)

        self.fbut.add_widget(self.lab_fdv)
        self.fbut.add_widget(self.b_reset)
        self.fbut.add_widget(self.valid)
        
        self.add_widget(self.input)        
        self.add_widget(self.fbut)

        self.default = []
        
    def get(self, res):
        pass

    def reset(self, *arg):
        pass


    def get_text(self, *arg):
        self.input.text += " ("
        joueur = {"Joueur" : "",
                  "Classe" : "",
                  "Classe dalliance" : "",
                  "Probabilité de contre-espionnage" : 0,
                  "date" : "",
                  "coord" : ""}

        planete = {"met" : 0,
                   "cri" : 0,
                   "deut" : 0,
                   "energie" : 0,
                   "nourriture" : 0,
                   "cdr" : 0,
                   "acti" : 0}

        dock = {"Chasseur léger" : 0,
                "Chasseur lourd" : 0,
                "Croiseur" : 0,
                "Vaisseau de bataille" : 0,
                "Traqueur" : 0,
                "Bombardier" : 0,
                "Destructeur" : 0,
                "Étoile de la mort" : 0,
                "Faucheur" : 0,
                "Éclaireur" : 0,
                "Petit transporteur" : 0,
                "Grand transporteur" : 0,
                "Recycleur" : 0,
                "Vaisseau de colonisation" : 0}

        flotte = {"Chasseur léger" : 0,
                  "Chasseur lourd" : 0,
                  "Croiseur" : 0,
                  "Vaisseau de bataille" : 0,
                  "Traqueur" : 0,
                  "Bombardier" : 0,
                  "Destructeur" : 0,
                  "Étoile de la mort" : 0,
                  "Faucheur" : 0,
                  "Éclaireur" : 0,
                  "Petit transporteur" : 0,
                  "Grand transporteur" : 0,
                  "Recycleur" : 0,
                  "Sonde despionnage" : 0,
                  "Satellite solaire" : 0,
                  "Foreuse" : 0,
                  "Vaisseau de colonisation" : 0}

        defense = {"Lanceur de missiles" : 0,
                   "Artillerie laser légère" : 0,
                   "Artillerie laser lourde" : 0,
                   "Canon de Gauss" : 0,
                   "Artillerie à ions" : 0,
                   "Lanceur de plasma" : 0,
                   "Petit bouclier" : 0,
                   "Grand bouclier" : 0,
                   "Missile d`interception" : 0,
                   "Missile interplanétaire" : 0}

        batiment = {"Mine de métal" : 0,
                    "Hangar de métal" : 0,
                    "Mine de cristal" : 0,
                    "Hangar de cristal" : 0,
                    "Synthétiseur de deutérium" : 0,
                    "Réservoir de deutérium" : 0,
                    "Centrale électrique de fusion" : 0,
                    "Usine de robots" : 0,
                    "Usine de nanites" : 0,
                    "Chantier spatial" : 0,
                    "Dock spatial" : 0,
                    "Silo de missiles" : 0,
                    "Laboratoire de recherche" : 0,
                    "Dépôt de ravitaillement" : 0,
                    "Terraformeur" : 0}

        recherche = {"Technologie énergétique" : 0,
                     "Technologie Laser" : 0,
                     "Technologie à ions" : 0,
                     "Technologie hyperespace" : 0,
                     "Technologie Plasma" : 0,
                     "Technologie Espionnage" : 0,
                     "Technologie Ordinateur" : 0,
                     "Astrophysique" : 0,
                     "Réseau de recherche" : 0,
                     "Technologie Graviton" : 0,
                     "Réacteur à combustion" : 0,
                     "Réacteur à impulsion" : 0,
                     "Propulsion hyperespace" : 0,
                     "Technologie Armes" : 0,
                     "Technologie Bouclier" : 0,
                     "Technologie Protection des vaisseaux spatiaux" : 0}

        batiment_fdv = {"Secteur résidentiel" : 0,
                        "Ferme biosphérique": 0,
                        "Centre de recherche" : 0,
                        "Académie des sciences" : 0,
                        "Centre de neurocalibrage" : 0,
                        "Extraction par fusion" : 0,
                        "Réserve alimentaire" : 0,
                        "Fusion à haute énergie" : 0,
                        "Tour d’habitation" : 0,
                        "Laboratoire de biotechnologie" : 0,
                        "Metropolis" : 0,
                        "Bouclier planétaire" : 0,
                        "Enclave stoïque" : 0,
                        "Culture du cristal" : 0,
                        "Forge runique" : 0,
                        "Centre technologique runique" : 0,
                        "Orictorium" : 0,
                        "Fusion magmatique" : 0,
                        "Chambre de disruption" : 0,
                        "Monument rocheux" : 0,
                        "Raffinerie de cristaux" : 0,
                        "Syntoniseur de deutérium" : 0,
                        "Centre de recherche sur les minéraux" : 0,
                        "Usine de traitement à haut rendement" : 0,
                        "Refugium" : 0,
                        "Condensateur d’antimatière" : 0,
                        "Salle à vortex" : 0,
                        "Maison du savoir" : 0,
                        "Forum de la transcendance" : 0,
                        "Convecteur d’antimatière" : 0,
                        "Laboratoire de clonage" : 0,
                        "Accélérateur par chrysalide" : 0,
                        "Biomodificateur" : 0,
                        "Modulateur psionique" : 0,
                        "Hangar de construction de vaisseau" : 0,
                        "Supraréfracteur" : 0,
                        "Chaîne de production" : 0,
                        "Usine de fusion de cellules" : 0,
                        "Centre de recherche en robotique" : 0,
                        "Réseau d’actualisation" : 0,
                        "Centre d’assemblage automatisé" : 0,
                        "Centre d’assemblage automatisé" : 0,
                        "Transformateur hyperpuissant" : 0,
                        "Chaîne de production de micropuces" : 0,
                        "Atelier de montage" : 0,
                        "Production de masse de puces" : 0,
                        "Synthétiseur à haut rendement" : 0,
                        "Nanorobots réparateurs" : 0}

        recherche_fdv = {"Renforcement du général des Mechas" : 0,
                         "Renforcement d'explorateur Kaelesh" : 0,
                         "Renfort du collecteur Rocta" : 0,
                         "IA du dépôt" : 0,
                         "Terraformeur à haute performance" : 0,
                         "Terraformeur à plasma" : 0,
                         "Construction optimisée de silos" : 0,
                         "Réseau d'analyse superglobal" : 0,
                         "Planque orbitale" : 0,
                         "Réseau psionique" : 0,
                         "Faisceau de traction télékinésique" : 0,
                         "Technologie de détection améliorée" : 0,
                         "Sixième sens" : 0,
                         "Système de propulsion télékinétique" : 0,
                         "Capteurs gravitationnels" : 0,
                         "Récupération de chaleur" : 0,
                         "Module doptimisation" : 0,
                         "Pilote automatique Slingshot" : 0,
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
                         "Module à cristaux ioniques" : 0,
                         "Intensification du bouclier à lobsidienne" : 0,
                         "Sondage en profondeur" : 0,
                         "Tête de forage en dimant" : 0,
                         "Sondage acoustique" : 0,
                         "Technologie d'extraction sismique" : 0,
                         "Technique de catalyse" : 0,
                         "Traitement au sulfure" : 0,
                         "Système de pompage à haute énergie" : 0,
                         "Pompes au magma" : 0,
                         "Extracteurs à haute performance	" : 0,
                         "Extraction" : 0,
                         "Chaîne de production automatisée" : 0,
                         "Technologies d'extraction améliorés" : 0,
                         "Harmonisateur psychique" : 0,
                         "Intelligence artificielle collective" : 0,
                         "Batteries volcaniques" : 0,
                         "Centrales géothermiques" : 0,
                         "IA de recherche" : 0,
                         "Neuro-interface" : 0,
                         "Technologie de laboratoire améliorée" : 0,
                         "Intelligence collective optimisée" : 0,
                         "Assistants robotiques" : 0,
                         "Superordinateur" : 0,
                         "Supraconducteur à haute température" : 0,
                         "Émetteur d'énergie à diamants" : 0,
                         "Stellarator amélioré" : 0,
                         "Générateur de champ de camouflage" : 0,
                         "IA de drone améliorée" : 0,
                         "Propulseurs à faible température" : 0,
                         "Technique d'armement expérimental" : 0,
                         "Matrice de protection psionique" : 0,
                         "Boucliers runiques" : 0}

        for dic in [defense, batiment, recherche, batiment_fdv, recherche_fdv]:
            for item in dic:
                if item in self.input.text:
                    index = self.input.text.index(item) + len(item)
                    val = ""
                    for x in range(len(self.input.text[index:])):
                        try:
                            int(self.input.text[index:][x])
                            val+= self.input.text[index:][x]
                        except:
                            if self.input.text[index:][x] == " ":
                                pass
                            else:
                                if self.input.text[index:][x] != ".":                                
                                    try:
                                        dic[item] = int(val)
                                    except:
                                        pass
                                    break

        for s in self.input.text.split("\n"):
            if "[" in s and "]" in s:
                joueur["coord"] = s[s.index("[")+1:s.index("]")]
                joueur["date"] = s[s.index("]")+1:]

            if "Joueur " in s:
                joueur["Joueur"] = s.split("Joueur ")[-1]

            if "Classe" in s and "alliance" not in s:
                joueur["Classe"] = s.split(": ")[1].split("`")[-1]

            if "Classe" in s and 'alliance' in s:
                joueur["Classe dalliance"] = s.split(": ")[1]

            if "Probabilité" in s:
                joueur["Probabilité de contre-espionnage"] = s.split(": ")[1]

            if "Réparations en cours" in self.input.text:
                for v in dock:
                    if v in self.input.text[self.input.text.index("Réparations en cours")+19:]:
                        index = self.input.text[self.input.text.index("Réparations en cours")+19:].index(v) + len(v)
                        val = ""
                        for x in range(len(self.input.text[self.input.text.index("Réparations en cours")+19:][index:])):
                            try:
                                int(self.input.text[self.input.text.index("Réparations en cours")+19:][index:][x])
                                val+= self.input.text[self.input.text.index("Réparations en cours")+19:][index:][x]
                            except:
                                if self.input.text[self.input.text.index("Réparations en cours")+19:][index:][x] != ".":                                
                                    try:
                                        dock[v] = int(val)
                                    except:
                                        pass
                                    break
                
                for vv in flotte:
                    if vv in self.input.text[:self.input.text.index("Réparations en cours")]:
                        index = self.input.text[:self.input.text.index("Réparations en cours")].index(vv) + len(vv)
                        val = ""
                        for x in range(len(self.input.text[:self.input.text.index("Réparations en cours")][index:])):
                            try:
                                int(self.input.text[:self.input.text.index("Réparations en cours")][index:][x])
                                val+= self.input.text[:self.input.text.index("Réparations en cours")][index:][x]
                            except:
                                if self.input.text[:self.input.text.index("Réparations en cours")][index:][x] != ".":                                
                                    try:
                                        flotte[vv] = int(val)
                                    except:
                                        pass
                                    break

            else:
                for v in flotte:
                    if v in self.input.text:
                        index = self.input.text.index(v) + len(v)
                        val = ""
                        for x in range(len(self.input.text[index:])):
                            try:
                                int(self.input.text[index:][x])
                                val+= self.input.text[index:][x]
                            except:
                                if self.input.text[index:][x] != ".":                                
                                    try:
                                        flotte[v] = int(val)
                                    except:
                                        pass
                                    break

        res = [joueur, dock, flotte, defense, batiment, recherche, batiment_fdv, recherche_fdv]

        self.get(res)
        #print(res)