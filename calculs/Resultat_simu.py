# coding : utf-8 

from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

from widgets import FGridLayout


class Resultat(FGridLayout):

    def __init__(self, **kwargs):
        super(Resultat, self).__init__(**kwargs)
        self.cols = 1
        self.spacing = [10, 10]

        # Nombre de round
        self.fnbr = GridLayout(cols = 1, size_hint = (1, None), height = 40)

        #self.lnbr = Label(text = "Nombre de rounds : ")#, size_hint = (None, 1), width = 140)
        self.enbr = Label()#size_hint = (None, 1), width = 10)
        #self.fnbr.add_widget(Label())
        #self.fnbr.add_widget(self.lnbr)
        self.fnbr.add_widget(self.enbr)
        #self.fnbr.add_widget(Label())
        self.add_widget(self.fnbr)

        # % de victoire
        self.fvic = GridLayout(cols = 3, size_hint = (1, None, ), height = 40)

        self.fvica = GridLayout(cols = 3)
        self.lvica = Label(text = "Les attaquants gagnent : ", size_hint = (None, 1), width = 200)
        self.evica = Label(size_hint = (None, 1), width = 10)
        self.fvica.add_widget(self.lvica)
        self.fvica.add_widget(self.evica)
        self.fvica.add_widget(Label())
        self.fvic.add_widget(self.fvica)

        self.fvicd = GridLayout(cols = 3)
        self.lvicd = Label(text = "Les défenseurs gagnent : ", size_hint = (None, 1), width = 200)
        self.evicd = Label(size_hint = (None, 1), width = 10)
        self.fvicd.add_widget(self.lvicd)
        self.fvicd.add_widget(self.evicd)
        self.fvicd.add_widget(Label())
        self.fvic.add_widget(self.fvicd)

        self.fvicn = GridLayout(cols = 3, size_hint = (0.7, 1))
        self.lvicn = Label(text = "Match nul : ", size_hint = (None, 1), width = 120)
        self.evicn = Label(size_hint = (None, 1), width = 10)
        self.fvicn.add_widget(self.lvicn)
        self.fvicn.add_widget(self.evicn)
        self.fvicn.add_widget(Label())
        self.fvic.add_widget(self.fvicn)

        self.add_widget(self.fvic)

        # BILAN
        self.fb = GridLayout(cols = 2, spacing = [30, 0])
        self.add_widget(self.fb)
        self.fbpb = GridLayout(cols = 1, size_hint = (None, 1), width = 560)
        self.fb.add_widget(self.fbpb)

        # BILAN ATTAQUANT
        self.fbatt = GridLayout(cols = 1, size_hint = (None, 1), width = 560)
        self.fbatt.add_widget(Label(text = "ATTAQUANTS", size_hint = (1, None), height = 60))

        self.fratt = GridLayout(cols = 3, size_hint = (1, None), height = 160)
        self.fbatt.add_widget(self.fratt)

        self.fressa = GridLayout(rows = 5, size_hint = (None, 1), width = 60)
        self.fressa.add_widget(Label())
        self.fressa.add_widget(Label(text = "M"))
        self.fressa.add_widget(Label(text = "C"))        
        self.fressa.add_widget(Label(text = "D"))        
        self.fressa.add_widget(Label(text = "TOTAL", bold = True))

        self.fratt.add_widget(self.fressa)

        self.fpa = GridLayout(rows = 5)
        self.fpa.add_widget(Label(text = "PERTES"))
        self.eapm = Label()
        self.fpa.add_widget(self.eapm)
        self.eapc = Label()
        self.fpa.add_widget(self.eapc)
        self.eapd = Label()
        self.fpa.add_widget(self.eapd)
        self.eapt = Label(bold = True)
        self.fpa.add_widget(self.eapt)                

        self.fratt.add_widget(self.fpa)

        self.fba = GridLayout(rows = 5)
        self.fba.add_widget(Label(text = "BENEFICE POSSIBLE"))
        self.eabm = Label()
        self.fba.add_widget(self.eabm)
        self.eabc = Label()
        self.fba.add_widget(self.eabc)
        self.eabd = Label()
        self.fba.add_widget(self.eabd)
        self.eabt = Label(bold = True)
        self.fba.add_widget(self.eabt)

        self.fratt.add_widget(self.fba)

        self.fbpb.add_widget(self.fbatt)


        # BILAN DEFENSEUR
        self.fbdef = GridLayout(cols = 1, size_hint = (None, 1), width = 560)
        self.fbdef.add_widget(Label(text = "DEFENSEURS", size_hint = (1, None), height = 60))

        self.frdef = GridLayout(cols = 3, size_hint = (1, None), height = 160)
        self.fbdef.add_widget(self.frdef)

        self.fressd = GridLayout(rows = 5, size_hint = (None, 1), width = 60)
        self.fressd.add_widget(Label())
        self.fressd.add_widget(Label(text = "M"))
        self.fressd.add_widget(Label(text = "C"))        
        self.fressd.add_widget(Label(text = "D"))        
        self.fressd.add_widget(Label(text = "TOTAL", bold = True))

        self.frdef.add_widget(self.fressd)

        self.fpd = GridLayout(rows = 5)
        self.fpd.add_widget(Label(text = "PERTES"))
        self.edpm = Label()
        self.fpd.add_widget(self.edpm)
        self.edpc = Label()
        self.fpd.add_widget(self.edpc)
        self.edpd = Label()
        self.fpd.add_widget(self.edpd)
        self.edpt = Label(bold = True)
        self.fpd.add_widget(self.edpt)                

        self.frdef.add_widget(self.fpd)

        self.fbd = GridLayout(rows = 5)
        self.fbd.add_widget(Label(text = "BENEFICE POSSIBLE"))
        self.edbm = Label()
        self.fbd.add_widget(self.edbm)
        self.edbc = Label()
        self.fbd.add_widget(self.edbc)
        self.edbd = Label()
        self.fbd.add_widget(self.edbd)
        self.edbt = Label(bold = True)
        self.fbd.add_widget(self.edbt)

        self.frdef.add_widget(self.fbd)

        self.fbpb.add_widget(self.fbdef)


        # CDR
        self.fvcdr = GridLayout(cols = 1)
        self.fcdr = GridLayout(cols = 1, size_hint = (None, None), size = (190, 200))
        self.fcdr.add_widget(Label(text = "CDR", size_hint = (1, None), height = 60))

        """self.rl = GridLayout(cols = 2)
        self.fcdr.add_widget(self.rl)"""

        self.bcdr = GridLayout(cols = 2)
        self.fcdr.add_widget(self.bcdr)
        self.lmcdr = Label(text = "M", size_hint = (None, 1), width = 3)
        self.emcdr = Label()
        self.lccdr = Label(text = "C", size_hint = (None, 1), width = 3)
        self.eccdr = Label()
        self.ldcdr = Label(text = "D", size_hint = (None, 1), width = 3)
        self.edcdr = Label()        
        self.ltcdr = Label(text = "TOTAL", bold = True, size_hint = (None, 1), width = 10)
        self.etcdr = Label()
        self.llune = Label(text = "Probabilité de luner : ", size_hint = (None, 1), width = 180)
        self.elune = Label()#size_hint = (None, 1), width = 10)
        self.bcdr.add_widget(self.lmcdr)
        self.bcdr.add_widget(self.emcdr)
        self.bcdr.add_widget(self.lccdr)               
        self.bcdr.add_widget(self.eccdr)
        self.bcdr.add_widget(self.ltcdr)  
        self.bcdr.add_widget(self.etcdr)
        self.bcdr.add_widget(self.llune)

        self.bcdr.add_widget(self.elune)

        self.fvcdr.add_widget(self.fcdr)
        self.lffa = Label(halign = "center")
        self.fvcdr.add_widget(self.lffa)
        self.lffd = Label(halign = "center")
        self.fvcdr.add_widget(self.lffd)
        self.pillage = Label(halign = "center")
        self.fvcdr.add_widget(self.pillage)
        self.fb.add_widget(self.fvcdr)
