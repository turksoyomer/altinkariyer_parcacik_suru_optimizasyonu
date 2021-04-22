from math import cos, sin, exp
import random

def kayip_fonksiyonu(x, y):
    z = sin(y) * exp((1 - cos(x)) ** 2) + cos(x) * exp((1 - sin(y)) ** 2) + (x - y) ** 2
    # z = x ** 2 + (y + 1) ** 2 - 5 * cos(1.5 * x + 1.5) - 3 * cos(2 * y - 1.5)
    return z


class Parcacik:
    def __init__(self, sinirlar):
        self.sinirlar = sinirlar # [[xmin, xmax],[ymin, ymax]]
        self.pozisyon = [] # [x,y]
        self.pozisyon_ata()
        self.hiz_vektoru = [] # [i,j]
        self.hiz_ata()
        self.en_iyi_pozisyon = self.pozisyon.copy() # [x,y]
        self.en_az_hata = float('inf') # z
        self.eylemsizlik_katsayisi = 0.5
        self.bilissel_katsayi = 2
        self.sosyal_katsayi = 2

    def pozisyon_ata(self):
        self.pozisyon.append(random.uniform(self.sinirlar[0][0], self.sinirlar[0][1]))
        self.pozisyon.append(random.uniform(self.sinirlar[1][0], self.sinirlar[1][1]))

    def hiz_ata(self):
        self.hiz_vektoru.append(random.uniform(-1,1))
        self.hiz_vektoru.append(random.uniform(-1,1))

    def degerlendir(self):
        hata = kayip_fonksiyonu(self.pozisyon[0], self.pozisyon[1])
        return hata

    def hiz_vektoru_guncelle(self, suru_en_iyi_pozisyon):
        """
        suru_en_iyi_pozisyon --> liste [x,y]
        """
        eylemsizlik_x = self.eylemsizlik_katsayisi * self.hiz_vektoru[0]
        bilissel_x = self.bilissel_katsayi * random.random() * (self.en_iyi_pozisyon[0] - self.pozisyon[0])
        sosyal_x = self.sosyal_katsayi * random.random() * (suru_en_iyi_pozisyon[0] - self.pozisyon[0])
        hiz_x = eylemsizlik_x + bilissel_x + sosyal_x

        eylemsizlik_y = self.eylemsizlik_katsayisi * self.hiz_vektoru[1]
        bilissel_y = self.bilissel_katsayi * random.random() * (self.en_iyi_pozisyon[1] - self.pozisyon[1])
        sosyal_y = self.sosyal_katsayi * random.random() * (suru_en_iyi_pozisyon[1] - self.pozisyon[1])
        hiz_y = eylemsizlik_y + bilissel_y + sosyal_y

        self.hiz_vektoru = [hiz_x, hiz_y]

    def pozisyon_guncelle(self):
        self.pozisyon[0] += self.hiz_vektoru[0]
        self.pozisyon[1] += self.hiz_vektoru[1]


class ParcacikSuruOptimizasyonu:
    def __init__(self, sinirlar, parcacik_sayisi, maksimum_iterasyon_sayisi):
        self.sinirlar = sinirlar
        self.parcacik_sayisi = parcacik_sayisi
        self.maksimum_iterasyon_sayisi = maksimum_iterasyon_sayisi
        self.parcaciklar = []
        self.parcacik_ata()
        self.suru_en_az_hata = float('inf')
        self.suru_en_iyi_pozisyon = [0,0]

    def parcacik_ata(self):
        for i in range(self.parcacik_sayisi):
            p = Parcacik(self.sinirlar)
            self.parcaciklar.append(p)

    def optimize_et(self):
        for i in range(self.maksimum_iterasyon_sayisi):
            for parcacik in self.parcaciklar:
                hata = parcacik.degerlendir()
                if hata < parcacik.en_az_hata:
                    parcacik.en_az_hata = hata
                    parcacik.en_iyi_pozisyon = parcacik.pozisyon.copy()
                if hata < self.suru_en_az_hata:
                    self.suru_en_az_hata = hata
                    self.suru_en_iyi_pozisyon = parcacik.pozisyon.copy()
                parcacik.hiz_vektoru_guncelle(self.suru_en_iyi_pozisyon)
                parcacik.pozisyon_guncelle()

sinirlar = [[-10,0],[-6.5,0]]
parcacik_sayisi = 50
maksimum_iterasyon_sayisi = 100

pso = ParcacikSuruOptimizasyonu(sinirlar, parcacik_sayisi, maksimum_iterasyon_sayisi)
pso.optimize_et()
i = 1
for parcacik in pso.parcaciklar:
    print('{}. parçacık son pozisyon: {}'.format(i, parcacik.pozisyon))
    i += 1

print('Sürü en az hata:', pso.suru_en_az_hata)
print('En iyi pozisyon:', pso.suru_en_iyi_pozisyon)
