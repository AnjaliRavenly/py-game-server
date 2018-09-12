from flask import Flask, flash, render_template, session, request, redirect, url_for
from DBcm import UseDatabase, ConnectionError, SQLError

from checker import check_logged_in

app = Flask(__name__)
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
dbconfig = {'host': '127.0.0.1',
             'user': 'admin',
             'password': 'mojehaslo',
             'database': 'mygame', }
app.config['dbconfig'] = dbconfig


class ServerError(Exception):
    pass

@app.route('/login')
def do_login(userEmail, userId, userName)->str:

    session['logged_in'] = True
    session['useremail'] = userEmail
    session['username'] = userName
    session['userId'] = userId
    return 'jesteś teraz zalogowany'


@app.route('/logout')
def do_logout()->str:
    session.pop('logged_in')
    session.pop('username')
    session.pop('useremail')
    session.pop('userId')
    flash('Jesteś teraz wylogowany !')
    return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def login()->'html':
    if 'logged_in' in session:
        return redirect(url_for('view_hero'))

    error = None

    if request.method == 'POST':
        if request.form["action"] == "login":
            try:
                with UseDatabase(app.config['dbconfig']) as cursor:
                    email_form = request.form['email']
                    _SQL = """SELECT COUNT(1) FROM users WHERE email=(%s)"""
                    cursor.execute(_SQL,(email_form,))
                    if not cursor.fetchone()[0]:
                        raise ServerError('Błędny e-mail')

                    password_form = request.form['password']
                    _SQL = """SELECT id, password, username FROM users WHERE email=(%s)"""
                    cursor.execute(_SQL, (email_form,))

                    for row in cursor.fetchall():
                        if password_form == row[1]:
                            do_login(email_form, row[0], row[2])
                            flash('Jesteś teraz zalogowany !')
                            return redirect(url_for('view_hero'))

                    raise ServerError('Złe hasło')

            except ConnectionError as err:

                print('login nie ma połączenia z bazą ', str(err))

            except SQLError as err:

                print('Błędne zapytanie w login', str(err))
            except Exception as err:

                print('Coś poszło źle w login', str(err))
                error = str(err)

    return render_template('index.html', error=error, the_title='Super Gra',)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error_register = None
    success_register = None
    error = None

    if request.method == 'POST':
        if request.form["action"] == "register":

            try:
                with UseDatabase(app.config['dbconfig']) as cursor:
                    username_form = request.form['user']
                    email_form = request.form['email']
                    password_form = request.form['pass']
                    _SQL = """SELECT COUNT(1) FROM users WHERE username=(%s) OR email=(%s)"""
                    cursor.execute(_SQL, (username_form, email_form))

                    if cursor.fetchone()[0]:
                        raise ServerError('Nazwa uzytkownika i/lub adres email są już zajęta.')

                    else:
                        _SQL = """INSERT INTO users (email, username, password) VALUES (%s, %s, %s)"""
                        cursor.execute(_SQL, (email_form, username_form, password_form))

                        _SQL = """SELECT id FROM users WHERE username=(%s)"""
                        cursor.execute(_SQL, (username_form,))

                        row = cursor.fetchone()
                        do_login(email_form, row[0], username_form)
                        flash('Dzięki za rejestrację !')
                        return redirect(url_for('view_hero'))

            except ConnectionError as err:
                print('register nie ma połączenia z bazą ', str(err))

            except SQLError as err:

                print('Błędne zapytanie w register', str(err))

            except ServerError as e:
                error_register = str(e)

            except Exception as err:

                print('Coś poszło źle w register ', str(err))
                error = str(err)

    return render_template('register.html', error_register=error_register,
                           error=error, success_register=success_register, the_title='Rejestracja', )

@app.route('/hero')
@check_logged_in
def view_hero():
    titles = ('Name', 'Typ', 'punkty')
    contents = []
    try:
        with UseDatabase(app.config['dbconfig']) as cursor:
            _SQL = """select h.name, ht.type, ht.points
                from heroes h
                join  hero_types ht on h.hero_type_id=ht.id
                join users u on h.user_id=u.id
                where u.username = %s
                """
            username = str(session['username'])
            cursor.execute(_SQL, (username,))
            contents = cursor.fetchall()
    except ConnectionError as err:
        print('view_hero nie ma połączenia z bazą ', str(err))
    except SQLError as err:
        print('Błędne zapytanie w view_hero', str(err))
    except Exception as err:
        print('Coś poszło źle w view_hero', str(err))
        return 'Błąd'

    return render_template('hero.html', the_title='Lista Twoich Bohaterów', the_row_titles=titles,
                           the_data=contents)

@app.route('/character', methods=['GET', 'POST'])
@check_logged_in
def add_hero():
    error_add = None
    success_add = None
    error = None

    if request.method == 'POST':
        if request.form["action"] == "new_hero":

            id_hero = request.form['heroType']
            heroname_form = request.form['hero_name']
            id_user = str(session['userId'])

            print([id_hero,heroname_form,id_user])

            try:
                with UseDatabase(app.config['dbconfig']) as cur:
                    _SQL2 = """SELECT COUNT(1) FROM heroes WHERE name=(%s)"""
                    cur.execute(_SQL2, (heroname_form,))
                    if cur.fetchone()[0]:
                        raise ServerError('Nazwa bohatera jest już zajęta.')
                    else:
                        _SQL = """INSERT INTO heroes VALUES (%s, %s, %s, %s, %s)"""
                        cur.execute(_SQL, ("", id_user, id_hero, heroname_form, None))
                        flash('Twój nowy bohater został dodany')

                        return redirect(url_for('view_hero'))

            except ConnectionError as err:
                print('Nie ma połączenia z bazą ', str(err))
            except SQLError as err:
                print('Błędne zapytanie ', str(err))
            except ServerError as e:
                error_add = str(e)
            except Exception as err:
                print('Coś poszło źle ', str(err))
                return 'Błąd'

    try:
        with UseDatabase(app.config['dbconfig']) as cursor:
            _SQL = """ select id, type, points from hero_types"""
            cursor.execute(_SQL)
            characterTypes = cursor.fetchall()

    except ConnectionError as err:
        print('add_hero nie ma połączenia z bazą ', str(err))
    except SQLError as err:
        print('Błędne zapytanie w add_hero ', str(err))
    except Exception as err:
        print('Coś poszło źle w add_hero', str(err))
    return render_template("character.html",
                           the_title='Stwórz bohatera',
                           characterTypes=characterTypes,
                           error_add=error_add, error=error, success_add=success_add)

app.secret_key = 'NigdyNieZgadniesz'
app.run()
