import numpy as np
# import pandas as pd
from apps.matriks import matriks
# from apps.models import Alternatif, Data
from apps import mysql, app

kriteria = matriks
w = []

#create sql cursor and query data
with app.app_context():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM kriteria")
    # cur.execute("SELECT DISTINCT")
    dkr = cur.fetchall()

for j,i in enumerate(dkr):
    w.append(i['bobot'])

# bobot preferensi
weight = np.array(w)

# Sigma Normalisasi matriks keputusan
def sigmaxij(cr):
    return list([np.sqrt(sum(np.power(x, 2))) for x in cr.transpose()])

# Normalisasi matriks keputusan
def normalisasi(cr):
    return[(x/sigmaxij(cr)) for x in cr]
normalization = np.array(normalisasi(kriteria))

# Menghitung Bobot normalisasi matriks keputusan
def wnorm(w, cr):
    return np.array([x * w for x in normalisasi(cr)])
wenorm = np.array(wnorm(weight,kriteria))

# Penentuan solusi ideal dan anti ideal
def maxmin(w, cr):
    A = wnorm(w, cr)
    return np.array([[max(A[:, i]), min(A[:, i])] for i in range(len(cr.transpose()))])
mms=maxmin(weight,kriteria).transpose()

# himpunan solusi ideal
def mmx(w, cr):
    B = maxmin(w, cr)
    return B[:, 0]

# Himpunan solusi anti ideal
def mmn(w, cr):
    B = maxmin(w, cr)
    return B[:, 1]

# Jarak tiap alternatif ke solusi ideal
def dmx(w, cr):
    return [np.sqrt(sum(np.power(x-mmx(w, cr), 2))) for x in wnorm(w, cr)]

# Jarak tiap alternatif ke solusi anti ideal
def dmn(w, cr):
    return [np.sqrt(sum(np.power(x-mmn(w, cr), 2))) for x in wnorm(w, cr)]

dmxn=np.array([dmx(weight,kriteria),dmn(weight,kriteria)]).transpose()
# for d in dmxn:
#     print(d[0])
# Perhitungan Kedekatan Relatif dengan Solusi Ideal
def cf(w, cr):
    return (np.array(dmn(w, cr))/(np.array(dmn(w, cr))+np.array(dmx(w, cr))))

cff = (cf(weight, kriteria))
# print(cff)
