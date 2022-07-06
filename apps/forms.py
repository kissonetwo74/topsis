from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired
from apps import mysql



class AlternatifForm(FlaskForm):
    nama = StringField('Nama', validators=[DataRequired()])
    alamat = StringField('Alamat', validators=[DataRequired()])
    nohp = StringField('No HP/ Telp')

class KriteriaForm(FlaskForm):
    nama = StringField("Nama", validators=[DataRequired()])
    bobot = StringField("Bobot", validators=[DataRequired()])


class SubkriteriaForm(FlaskForm):
    nama = StringField('Nama', validators=[DataRequired()])
    bobot = StringField('Bobot', validators=[DataRequired()])