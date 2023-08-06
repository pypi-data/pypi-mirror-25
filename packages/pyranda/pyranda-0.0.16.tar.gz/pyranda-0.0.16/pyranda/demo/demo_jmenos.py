from ..jmenos import Jmenos
from ..jmeno import Jmeno

j = Jmenos()
for a in range(1, 10):
    i = j.GetRandomJmeno(pohlavi=1)
    print(i.nazev)
    i = j.GetRandomJmeno(pohlavi=2)
    print(i.nazev)
