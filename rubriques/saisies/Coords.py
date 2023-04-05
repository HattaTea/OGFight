# coding : utf-8

from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput

from kivy.properties import StringProperty, BooleanProperty

from kivy.clock import Clock

class Coords(GridLayout):

    gal = StringProperty("1")
    syst = StringProperty("1")
    posi = StringProperty("1")
    emp = BooleanProperty(False)

    value = StringProperty("")


    def __init__(self, titre, **kwargs):
        super(Coords, self).__init__(**kwargs)
        self.cols = 9
        self.size_hint = (1, None)
        self.height = 30

        self.add_widget(Label(text = " "))

        self.titre = Label(text = titre, size_hint = (None, 1), width = 180)
        self.add_widget(self.titre)

        self.galaxie = TextInput(write_tab = False, size_hint = (None, 1), width = 20, text = "1")
        self.ss = TextInput(write_tab = False, size_hint = (None, 1), width = 40, text =  "1")
        self.position = TextInput(write_tab = False, size_hint = (None, 1), width = 30, text = "1")
        llune = Label(text = "  Lune : ", size_hint = (None, 1), width = 50)
        self.lune = CheckBox(active = False, size_hint = (None, 1), width = 30)
        self.add_widget(Label(text = " ", size_hint = (0.9, 1)))

        self.add_widget(self.galaxie)
        self.add_widget(self.ss)
        self.add_widget(self.position)
        self.add_widget(llune)
        self.add_widget(self.lune)
        self.add_widget(Label(text = " "))

        self.galaxie.bind(text = self.setter("gal"))
        self.galaxie.bind(text = lambda i, v : Clock.schedule_once(lambda e, ii = i, vv = v : self.e_number(ii, vv), -1))

        self.ss.bind(text = self.setter("syst"))
        self.ss.bind(text = lambda i, v : Clock.schedule_once(lambda e, ii = i, vv = v : self.e_number(ii, vv), -1))

        self.position.bind(text = self.setter("posi"))
        self.position.bind(text = lambda i, v : Clock.schedule_once(lambda e, ii = i, vv = v : self.e_number(ii, vv), -1))

        self.lune.bind(active = self.setter("emp"))

        self.bind(gal = self.set_value)
        self.bind(syst = self.set_value)
        self.bind(posi = self.set_value)
        self.bind(emp = self.set_value)

        self.set_value()


    def set_value(self, *arg):
        self.value = "{0} - {1} - {2} - {3}".format(self.gal, self.syst, self.posi, "L" if self.emp else "P")

    def get(self):
        return [self.galaxie.text, self.ss.text, self.position.text, self.lune.active]


    def e_number(self, i, v):
        if v != "":
            try:
                int(v)
            except:
                print("undo")
                vi = i.cursor_index()
                i.text = i.text[:vi-1]+i.text[vi:]
                if vi == i.cursor_index():
                    i.do_cursor_movement("cursor_left")
                return
  