import math

# Funkcje pomocniczne
def b(v): # rozpietosc plata
    return v[0]

def S(v): # powierzchnia nosna
    return v[0] * v[1]

def lambbda(v): # wydluzenie geometryczne
    return pow(b(v),2)/S(v)

def m(v): # masa samolotu
    return mbp + 4.936 * S(v) * pow(lambbda(v), 0.3)

def cz(v): # Cz przelotowy
    return (2 * m(v) * g)/(rho * pow(Vc, 2) * S(v))

def cz_vmin(v): # Cz dla Vmin
    return (2 * m(v) * g) / (rho * pow(Vmin, 2) * S(v))

def e0(v): # wspolczynnik Oswalda
    return 4.61 * (1 - 0.045 * pow(lambbda(v), 0.68)) * math.cos(pow(fi_LE * math.pi / 180, 0.15)) - 3.1

def Kara(v): # funkcja kary
    return pow(((1 / (Cz_max - cz(v))) - (1 / (Cz_max - cz_vmin(v)))), 2)

def D(v): # opor calkowity
    return (rho * pow(Vc, 2) / 2) * S(v) * (cxt + (pow(cz(v), 2) / (math.pi * lambbda(v) * e0(v))))

def F(v): # funkcja celu
    return D(v) + Kara(v)

# Dane
nwym = 2 # liczba wymiarow przestrzeni decyzyjnych
rho = 1.225 #gestosc powietrza [kg/m3]
cxt = 0.02 #opor minimalny (tarcia)
g = 9.807 #przyspieszenie ziemskie [m/s2]
mbp = 2393 #masa konstrukcji bez masy plata [kg]
Vc = 125 #predkosc przelotowa [m/s]
Vmin = 30 #predkosc minimalna [m/s]
fi_LE = 0 #skos plata (krawedzi natarcia) [deg]
Cz_max = 2.5 #max. wartosc wsp. sily nosnej

# Pierwsze przyblizenie
x0 = [[14.0, 1.8]] # wartosci poczatkowe wektora zmiennych decyzyjnych
dlk = 0.0005 # krok iteracji
LK = 5000 # liczba krokow iteracyjnych

xb = x0 # wartosci poczatkowe wektora zmiennych decyzyjnych

v1 = []
v2 = []

G = [[1 for i in range(nwym)]]

for k in range(1, LK+1):
    print "\nITERACJA %s" % k
    G.append([1 for l in range(nwym)])

    for n in range(nwym):
        Ster = 1
        xb_temp1 = xb[k-1]
        xb_temp2 = xb[k-1]
        v1 = []
        v2 = []
        for j in range(nwym):
            xb_plus_dlk = xb_temp1[j] + dlk
            xb_minus_dlk = xb_temp2[j] - dlk
            v1.append(xb_plus_dlk)
            v2.append(xb_minus_dlk)

        G[k][n] = (F(v1) - F(v2)) / (2 * dlk)

    xb.append([0 for i in range(nwym)])
    for n in range(nwym):
        xb[k][n] = xb[k - 1][n] - G[k - 1][n] * (dlk / math.sqrt(sum(i ** 2 for i in G[k - 1])))

    print "Rozpietosc plata: %f" % xb[k][0]
    print "Cieciwa: %f" % xb[k][1]

# Zapis wynikow do pliku
with open("number_of_iterations.txt", "w+") as f:
    f.write(str(LK))

with open("results.txt", "w+") as f:
    for i in range(len(xb)):
        f.write(str(xb[i][0]) + "\t" + str(xb[i][1]) + "\n")

with open("results_of_the_last_iteration.txt", "w+") as f:
    f.write("Rozpietosc plata: %.2f\n" % xb[LK][0])
    f.write("Cieciwa: %.2f\n" % xb[LK][1])
    f.write("Powierzchnia nosna: %.2f\n" % S(xb[LK]))
    f.write("Wydluzenie geometryczne: %.2f\n" % lambbda(xb[LK]))
    f.write("Masa samolotu: %.2f\n" % m(xb[LK]))
    f.write("Cz przelotowy: %.2f\n" % cz(xb[LK]))
    f.write("Cz dla Vmin: %.2f\n" % cz_vmin(xb[LK]))
    f.write("Wspolczynnik Oswalda: %.2f\n" % e0(xb[LK]))
    f.write("Funkcja kary: %.2f\n" % Kara(xb[LK]))
    f.write("Opor calkowity: %.2f\n" % D(xb[LK]))
    f.write("Funkcja celu: %.2f\n" % F(xb[LK]))
