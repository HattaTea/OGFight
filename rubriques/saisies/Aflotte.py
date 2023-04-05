# coding : utf-8

from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from kivy.properties import StringProperty

from kivy.clock import Clock


class Aflotte(GridLayout):

    pt  = StringProperty("0")
    gt  = StringProperty("0")
    cle  = StringProperty("0")
    clo  = StringProperty("0")
    cro  = StringProperty("0")
    vb  = StringProperty("0")
    vc  = StringProperty("0")
    rec  = StringProperty("0")
    so  = StringProperty("0")
    bb  = StringProperty("0")
    dd  = StringProperty("0")
    rip  = StringProperty("0")
    tr  = StringProperty("0")
    ff  = StringProperty("0")
    ecl  = StringProperty("0")

    def __init__(self, **kwargs):
        super(Aflotte, self).__init__(**kwargs)
        
        self.vaisseaux = ["Petit Transporteur", "Grand Transporteur", "Chasseur Leger", "Chasseur Lourd",
                          "Croiseur", "Vaisseau de Bataille", "Vaisseau de Colo", "Recycleur", "Sonde",
                          "Bombardier", "Destructeur", "RIP", "Traqueur", "Faucheur", "Eclaireur"]

        self.avaisseaux = {"Petit Transporteur" : "pt", 
                           "Grand Transporteur" : "gt", 
                           "Chasseur Leger" : "cle", 
                           "Chasseur Lourd" : "clo",
                           "Croiseur" : "cro", 
                           "Vaisseau de Bataille" : "vb", 
                           "Vaisseau de Colo" : "vc", 
                           "Recycleur" : "rec", 
                           "Sonde" : "so",
                           "Bombardier" : "bb", 
                           "Destructeur" : "dd", 
                           "RIP" : "rip", 
                           "Traqueur" : "tr", 
                           "Faucheur" : "ff", 
                           "Eclaireur" : "ecl"}

        self.restants = {}

        self.cols = 1
        self.size_hint = (1, None)
        self.height = len(self.vaisseaux)*35
        self.padding = [0, 5]
        self.spacing = [0, 5]

        self.vals = {}
        for v in self.vaisseaux:
            frame = GridLayout(cols = 3, size_hint = (1, None), height = 30)
            lab = Label(text = v)
            saisi = TextInput(write_tab = False, size_hint = (None, 1), width = 100, text = "0")
            saisi.bind(text = self.setter(self.avaisseaux[v]))
            saisi.bind(text = lambda i, v : Clock.schedule_once(lambda e, ii = i, vv = v : self.e_number(ii, vv), -1))

            rlab = Label()
            self.restants[self.avaisseaux[v]] = rlab

            frame.add_widget(lab)
            frame.add_widget(saisi)
            frame.add_widget(rlab) 
            self.vals[v] = saisi
            self.add_widget(frame)

    def recieve_focus(self):
        self.vals[self.vaisseaux[0]].focus = True


    def go_nextab(self):
        pass

    def e_number(self, i, v):
        if v != "":
            try:
                int(v)
            except:
                vi = i.cursor_index()
                i.text = i.text[:vi-1]+i.text[vi:]
                if vi == i.cursor_index():
                    i.do_cursor_movement("cursor_left")
                return
  
        