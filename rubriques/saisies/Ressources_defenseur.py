# coding : utf-8

from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from kivy.properties import StringProperty


class Ressources_defenseur(GridLayout):

    metal = StringProperty("0")
    cristal = StringProperty("0")
    deuterium = StringProperty("0")

    def __init__(self, **kwargs):
        super(Ressources_defenseur, self).__init__(**kwargs)
        self.cols = 3
        self.spacing = [5, 5]
        self.size_hint = (1, None)
        self.height = 65

        ress = ["Métal", "Cristal", "Dutérium"]
        for r in ress:
            lab = Label(text = r, size_hint = (1, None), height = 30)
            self.add_widget(lab)

        self.emetal = TextInput(size_hint = (1, None), height = 30)
        self.emetal.bind(text = self.setter("metal"))
        self.add_widget(self.emetal)

        self.ecristal = TextInput(size_hint = (1, None), height = 30)
        self.ecristal.bind(text = self.setter("cristal"))
        self.add_widget(self.ecristal)

        self.edeuterium = TextInput(size_hint = (1, None), height = 30)
        self.edeuterium.bind(text = self.setter("deuterium"))
        self.add_widget(self.edeuterium)
        
