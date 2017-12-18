import math
import numpy as np
import matplotlib.pyplot as plt

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

# Sczytanie wynikow z pliku
with open("number_of_iterations.txt", "r") as f:
    LK = int(f.read())

wyniki = []
with open("results.txt", "r") as f:
    for i in f:
        line = i.rstrip('\n')
        wyniki.append(line.split('\t'))

wyniki_float = []
for i in wyniki:
    rozpietosc = float(i[0])
    cieciwa = float(i[1])
    list_temp = [rozpietosc, cieciwa]
    wyniki_float.append(list_temp)

# WYKRESY

# Sila oporu
plt.figure(1)
plt.plot([x for x in range(LK+1)], [D(y) for y in wyniki_float])
plt.title('Sila oporu w funkcji liczby iteracji')
plt.xlabel('Liczba iteracji')
plt.ylabel('Sila oporu')
plt.savefig('wykres_sila_oporu.png')

# Powierzchnia nosna
plt.figure(2)
plt.plot([x for x in range(LK+1)], [S(y) for y in wyniki_float])
plt.title('Powierzchnia nosna w funkcji liczby iteracji')
plt.xlabel('Liczba iteracji')
plt.ylabel('Powierzchnia nosna')
plt.savefig('wykres_powierzchnia_nosna.png')

# Rozpietosc plata
plt.figure(3)
plt.plot([x for x in range(LK+1)], [y[0] for y in wyniki_float])
plt.title('Rozpietosc plata w funkcji liczby iteracji')
plt.xlabel('Liczba iteracji')
plt.ylabel('Rozpietosc plata')
plt.savefig('wykres_rozpietosc_plata.png')

# Wydluzenie geometryczne plata
plt.figure(4)
plt.plot([x for x in range(LK+1)], [y[0] for y in wyniki_float])
plt.title('Wydluzenie geometryczne plata w funkcji liczby iteracji')
plt.xlabel('Liczba iteracji')
plt.ylabel('Wydluzenie geometryczne plata')
plt.savefig('wykres_wydluzenie_geometryczne_plata.png')

# Cieciwa
plt.figure(5)
plt.plot([x for x in range(LK+1)], [y[1] for y in wyniki_float])
plt.title('Cieciwa w funkcji liczby iteracji')
plt.xlabel('Liczba iteracji')
plt.ylabel('Cieciwa')
plt.savefig('wykres_cieciwa.png')

# Masa samolotu
plt.figure(6)
plt.plot([x for x in range(LK+1)], [m(y) for y in wyniki_float])
plt.title('Masa samolotu w funkcji liczby iteracji')
plt.xlabel('Liczba iteracji')
plt.ylabel('Masa samolotu')
plt.savefig('wykres_masa_samolotu.png')

# Cz przelotowy
plt.figure(7)
plt.plot([x for x in range(LK+1)], [cz(y) for y in wyniki_float])
plt.title('Cz przelotowy w funkcji liczby iteracji')
plt.xlabel('Liczba iteracji')
plt.ylabel('Cz przelotowy')
plt.savefig('wykres_Cz_przelotowy.png')

# Cz dla Vmin
plt.figure(8)
plt.plot([x for x in range(LK+1)], [cz(y) for y in wyniki_float])
plt.title('Cz dla Vmin w funkcji liczby iteracji')
plt.xlabel('Liczba iteracji')
plt.ylabel('Cz dla Vmin')
plt.savefig('wykres_Cz_dla_Vmin.png')


# MAPY KONTUROWE

# Funkcja celu
x = np.linspace(2, 15, 40)
y = np.linspace(1, 5, 40)

X,Y = np.meshgrid(x, y)

M = F([X, Y]) - Kara([X, Y])

plt.figure(9)
plt.title('Funkcja celu')
plt.xlabel('rozpietosc')
plt.ylabel('cieciwa')
cntf = plt.contourf(X, Y, M, levels = np.linspace(0,16000,25))
cnt = plt.contour(cntf, levels = np.linspace(0,16000,25), colors = 'black')
plt.clabel(cnt, fmt='%.f', colors='black', fontsize=14)
#cbar = plt.colorbar(cntf)
#cbar.ax.set_ylabel("Funkcja celu")
plt.savefig('mapa_funkcja_celu.png')

# Cz dla Vmin
x = np.linspace(2, 15, 40)
y = np.linspace(1, 5, 40)

X,Y = np.meshgrid(x, y)

P = cz_vmin([X, Y])

plt.figure(10)
plt.title('Cz dla Vmin')
plt.xlabel('rozpietosc')
plt.ylabel('cieciwa')
cntf = plt.contourf(X, Y, P, levels = np.linspace(0,24,25))
cnt = plt.contour(cntf, levels = np.linspace(0,24,25), colors = 'black')
plt.clabel(cnt, fmt='%.f', colors='black', fontsize=14)
#cbar = plt.colorbar(cntf)
#cbar.ax.set_ylabel("Cz dla Vmin")
plt.savefig('mapa_Cz_dla_Vmin.png')

#plt.show()
