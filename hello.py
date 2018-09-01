from flask import Flask, render_template, session, request, redirect, url_for
from DBcm import UseDatabase, ConnectionError, CredentialsErorr, SQLError
from hashlib import md5
import mysql.connector
from checker import check_logged_in

app = Flask(__name__)
dbconfig = {'host': '127.0.0.1',
             'user': 'admin',
             'password': 'mojehaslo',
             'database': 'myGame', }
app.config['dbconfig'] = dbconfig


# conn = mysql.connector.connect(**dbconfig)
@app.route('/login')
def do_login()->str:
    session['logged_in'] = True
    return 'Jesteś teraz zalogowany.'


@app.route('/logout')
def do_logout()->str:
    session.pop('logged_in')
    return 'Jesteś teraz wylogowany'

@app.route('/status')
def status()-> str:
    if 'logged_in' in session:
        return 'jestes zalogowany'
    return 'nie jestes zalogowany'


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return render_template('bohaterowie.html')

    error = None

    class ServerError(Exception):
        pass

    if request.method == 'POST':
        if request.form["action"] == "login":
            try:
                conn = mysql.connect()
                cur = conn.cursor()
                username_form = request.form['username']
                cur.execute("SELECT COUNT(1) FROM users WHERE login = '" + username_form + "'")

                if not cur.fetchone()[0]:
                    raise ServerError('Błędna nazwa użytkownika')

                password_form = request.form['password']
                cur.execute("SELECT password FROM users WHERE login = '" + username_form + "'")

                for row in cur.fetchall():
                    if md5(password_form.encode('utf-8')).hexdigest() == row[0]:
                        session['username'] = request.form['username']
                        return render_template('bohaterowie.html')

                raise ServerError('Błędne hasło')

            except ServerError as e:
                error = str(e)

    return render_template('index.html', error=error)

@app.route('/bohaterowie')
@check_logged_in
def view_hero():
    try:
        with UseDatabase(app.config['dbconfig']) as cursor:
            _SQL = """select * from heros"""
            cursor.execute(_SQL)
            contents = cursor.fetchall()
        titles = ('ID', 'Typ', 'Strefa', 'punkty')
        return render_template('bohaterowie.html', the_title='Lista Bohaterów', the_row_titles=titles, the_data=contents)
    except ConnectionError as err:
        print('Nie ma połączenia z bazą ', str(err))
    except SQLError as err:
        print('Błędne zapytanie ', str(err))
    except Exception as err:
        print('Coś poszło źle ', str(err))
        return 'Błąd'
    return render_template('bohaterowie.html')

app.secret_key = 'NigdyNieZgadniesz'
app.run()