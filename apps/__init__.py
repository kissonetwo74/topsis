from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)



app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "Syer4_1401"
app.config["MYSQL_DB"] = "mydbsql"
# app.config["MYSQL_UNIX_SOCKET"] = "/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock"

app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.config['SECRET_KEY'] = 'syera adell'
app.jinja_env.filters['zip'] = zip
mysql = MySQL(app)

from apps import routes
from apps import topsis
from apps import matriks
# /Applications/XAMPP/xamppfiles/var/mysql/mysql.sock
# /Applications/MAMP/tmp/mysql/mysql.sock