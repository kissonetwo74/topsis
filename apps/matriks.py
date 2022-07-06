from apps import app,mysql
import numpy as np
    
M = []

with app.app_context():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM kriteria")
    kr = cur.fetchall()
    cur.execute("SELECT DISTINCT alternatif.nama FROM alternatif INNER JOIN penilaian ON alternatif.id=penilaian.alternatif_id")
    al = cur.fetchall()
    cur.execute("SELECT * FROM penilaian")
    pl = cur.fetchall()

print(al)
print(kr)
x = len(al)
y = len(kr)

for d in pl:
    M.append(d['subkriteria_id'])
mat = np.array(M)
# print(mat)
matriks = mat.reshape(x,y)
# print(matriks)
# print(type(matriks))

