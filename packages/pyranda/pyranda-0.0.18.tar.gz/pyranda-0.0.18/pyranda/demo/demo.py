from pyranda import Jmenos, Prijmenis

j = Jmenos()
p = Prijmenis()
for a in range(1, 10):
    jmeno = j.GetRandomJmeno(pohlavi=1)
    prijmeni = p.GetRandomPrijmeni(pohlavi=1)

    print(jmeno.nazev + " " + prijmeni.nazev)
