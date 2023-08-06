from pyranda import Jmenos

j = Jmenos()
p = Prijmenis()
for a in range(1, 10):
    jmeno = j.GetRandomJmeno(pohlavi=1)
    prijmeni = p.GetRandomPrijmeni(pohlavi=1)

    print(i.nazev)
    i = j.GetRandomJmeno(pohlavi=2)
    print(i.nazev)
