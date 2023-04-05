# coding : utf-8

from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox

from kivy.properties import StringProperty



class MyCheckBox(GridLayout):

    value = StringProperty()

    def __init__(self, group, dic, **kwargs):
        super(MyCheckBox, self).__init__(**kwargs)

        self.dic = dic
        self.group = group

        self.spacing = [20, 0]
        self.padding = [10, 0]

        self.cols = 2*len(self.dic) if len(self.dic) < 5 else 10
        self.values = []

        for v in dic:
            lab = Label(text = v, halign = "right", valign = "center", size_hint = (0.9, 1))
            lab.bind(size = lab.setter("text_size"))
            self.add_widget(lab)
            self.active = CheckBox(group = self.group, active = True, allow_no_selection=True, size_hint = (0.1, 1))
            self.active.bind(active = self.get)
            self.add_widget(self.active)
            self.values.append(self.active)

        self.get()

    def set(self, value):
        for v in range(len(self.values)):
            if self.dic[v].lower() == value.lower():
                self.values[v].active = True
            else:
                self.values[v].active = False

    def get(self, *kwarg):
        for v in range(len(self.values)):
            if self.values[v].active:
                self.value = self.dic[v]
                return self.dic[v]
        self.value = "Aucune"
        return "Aucune"
