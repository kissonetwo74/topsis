from apps import app,mysql
from apps.matriks import kr,al,matriks
from flask_wtf import FlaskForm
from flask import render_template, request, redirect, url_for,flash
from apps.forms import AlternatifForm, KriteriaForm, SubkriteriaForm
from apps.topsis import cff, normalization, wenorm, mms, dmxn

import numpy as np


def getcur():
    return mysql.connection.cursor()


@app.route('/')
def index():

    return render_template("index.html")

@app.route('/alternatif', methods=['GET','POST'])
def alternatif():
    form = AlternatifForm()
    cur = getcur()
    # cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM alternatif")
    data = cur.fetchall()
   
    if form.validate_on_submit():
        nama = form.nama.data
        alamat = form.alamat.data
        nohp = form.nohp.data
        cur.execute("INSERT INTO alternatif(nama, alamat, nohp ) values(%s,%s,%s)",(nama,alamat, nohp))
        mysql.connection.commit()
        return redirect(url_for('alternatif'))
    return render_template('alternatif.html', form = form, data = data)


@app.route('/del_alternatif/<string:id>')
def del_alternatif(id):
    # cur = mysql.connection.cursor()
    cur = getcur()
    cur.execute("DELETE FROM alternatif WHERE id = %s", (id))
    mysql.connection.commit()
    return redirect(url_for('alternatif'))

@app.route('/kriteria', methods=['GET','POST'])
def kriteria():
    form = KriteriaForm()
    # cur = mysql.connection.cursor()
    cur = getcur()
    cur.execute("SELECT * FROM kriteria")
    data = cur.fetchall()
    if form.validate_on_submit():
        nama = form.nama.data
        bobot = form.bobot.data
        cur.execute("INSERT INTO kriteria(nama, bobot) VALUES(%s, %s)",(nama, bobot))
        mysql.connection.commit()
        return redirect(url_for('kriteria'))
    return render_template('kriteria.html', form = form, data = data)

@app.route('/del_kriteria/<string:id>', methods=['GET','POST'])
def del_kriteria(id):
    # cur = mysql.connection.cursor()
    cur = getcur()
    cur.execute("DELETE FROM kriteria WHERE id = %s",(id))
    mysql.connection.commit()
    return redirect(url_for('kriteria'))


@app.route('/subkriteria', methods=['GET','POST'])
def subkriteria():
    form = SubkriteriaForm()
    cur = getcur()
    cur.execute("SELECT * FROM kriteria")
    data = cur.fetchall()
    cur.execute("SELECT * FROM subkriteria")
    data2 = cur.fetchall()
    if form.validate_on_submit():
        nama = form.nama.data
        bobot = form.bobot.data
        idkriteria = request.form.get("kri")
        cur.execute("INSERT INTO subkriteria(nama,nilai,kriteria_id) VALUES(%s,%s,%s)", (nama,bobot,idkriteria))
        mysql.connection.commit()
        return redirect(url_for('subkriteria'))
    return render_template("subkriteria.html", data = data, data2 = data2, form = form)


@app.route('/penilaian')
def datapenilaian():
    iad = ["A+","A-"]
    return render_template("datapenilaian.html", data = kr, mt=matriks, data1 = al, cf=cff, normal=normalization, wnorm = wenorm, mms=mms, iad=iad, dmxn=dmxn)


@app.route('/penilaian/<int:id>', methods=['GET','POST'])
def penilaian(id):
    cur = getcur()
    cur.execute(f"SELECT * FROM alternatif WHERE id={id}")
    data = cur.fetchone()
    cur.execute("SELECT * FROM kriteria")
    data1 = cur.fetchall()
    cur.execute("SELECT * FROM subkriteria")
    data2 = cur.fetchall()

    return render_template("penilaian.html", data = data, data1 = data1, data2 = data2)



@app.route('/input_penilaian', methods=['GET','POST'])
def inputpenilaian():
    cur = getcur()
    cur.execute("SELECT * FROM kriteria")
    data = cur.fetchall()
    
    if request.method == 'POST':
        id = request.form.get("ida")
        cur.execute(f"SELECT * FROM penilaian where alternatif_id = {id}")
        data1 = cur.fetchall()
        if data1:
            flash("Nilai Alternatif sudah ada")
        else:
            print("tidak ada")
            i = 1
            for j in data:
                a = request.form.get("ida")
                k = request.form.get(f"k{i}")
                sk = request.form.get(f"sk{i}")
                cur.execute("INSERT INTO penilaian(alternatif_id, kriteria_id, subkriteria_id) VALUES(%s,%s,%s)", (a,k,sk))
                mysql.connection.commit()
                i = i + 1
    return redirect(url_for('alternatif'))

@app.route('/clear_tbsubkriteria')
def clear_tbsubkriteria():
    if request.method=='GET':
        cur = getcur()
        cur.execute("TRUNCATE TABLE subkriteria")
        return redirect(url_for('subkriteria'))

@app.route('/clear_tbkriteria')
def clear_tbkriteria():
    if request.method=='GET':
        cur = getcur()
        cur.execute("TRUNCATE TABLE kriteria")
        return redirect(url_for('kriteria'))    

