from msilib import datasizemask
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'picaras_tours'

# Intialize MySQL
mysql = MySQL(app)

@app.route('/picaras_tours/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM tb_usuarios WHERE usuario = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            print(account)
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['ID']
            session['username'] = account['usuario']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)

@app.route('/picaras_tours/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/picaras_tours/viajes')
def viajes():
    # Check if user is loggedin
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM tb_viajes")
        dataselect = cursor.fetchall()
        # User is loggedin show them the home page
        return render_template('viajes.html', data=dataselect)
    # User is not loggedin redirect to login page
    return redirect(url_for('home'))

@app.route('/picaras_tours/reportes')
def reportes():
    # Check if user is loggedin
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM tb_viajes WHERE MONTH(fecha_salida)< DATE_ADD(CURRENT_TIMESTAMP(), INTERVAL 6 MONTH);")
        dataselect2 = cursor.fetchall()
        # User is loggedin show them the home page
        return render_template('reportes.html', data=dataselect2)
    # User is not loggedin redirect to login page
    return redirect(url_for('home'))
