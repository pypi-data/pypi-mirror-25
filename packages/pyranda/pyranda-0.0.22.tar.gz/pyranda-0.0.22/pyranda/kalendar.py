class KalendarItem:
    """ Objekt pro položku kalendáře.."""
    def __init__(self):
        self.rok = 0
        self.mesic = 0
        self.den = 0
        self.pden = 0
        self.popis = ""
        self.nden = 0
        self.svatek = False
        self.dentydne = 0

    def SetDate(self, rok, mesic, den):
        """ Nastavení datumu do položky kalendáře.. """
        self.rok = rok
        self.mesic = mesic
        self.den = den

    def SetPDen(self, pden):
        """ Nastavení informace o pracovním dnu do položky kalendáře.. """
        self.pden = pden

    def SetPopis(self, popis):
        """ Popis dne v položce kalendáře.. """
        self.popis = popis

    def SetNDen(self, nden):
        """ Nastavení pořadového čísla dne.. """
        self.nden = nden

    def SetSvatek(self, svatek):
        """ Nastavení boolean informace o tom, že daný den je svátek.. """
        self.svatek = svatek

    def SetDenTydne(self, dentydne):
        """ Nastavení pořadového dne v týdnu.. """
        self.dentydne = dentydne

class Kalendar:
    """ Objekt kalendáře.. """
    def __init__(self):
        self.items = []

    def AddItem(self, item):
        """ Přidání položky do kalendáře.. """
        self.items.append(item)

    def ReadDate(self):
        item.SetItem(2017, 1, 2); item.SetPDen(False)
        item.SetPopis("")
        item.SetNDen(2)
        item.SetSvatek(False)
        item.SetDenTydne(2)
