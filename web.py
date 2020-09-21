from flask import Flask, render_template, request, session, logging, url_for, redirect, flash, logging
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from passlib.hash import sha256_crypt
from flask_login import login_user, LoginManager, login_manager, login_required, mixins

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/registration'
db = SQLAlchemy(app)

login_m = LoginManager()
login_m.init_app(app)
login_m.login_view = 'login.html'


class LoginId(db.Model):
    username = db.Column(db.String(50), primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False, primary_key=False, unique=False)
    c_password = db.Column(db.String(50), nullable=False, primary_key=False, unique=False)
    email = db.Column(db.String(50), unique=True, nullable=False, primary_key=False)
    contact = db.Column(db.String(50), unique=True, nullable=False, primary_key=False)
    gender = db.Column(db.String(50), nullable=False, primary_key=False, unique=False)


def __init__(self, username, password, c_password, email, contact, gender):
    self.username = username
    self.password = password
    self.c_password = c_password
    self.email = email
    self.contact = contact
    self.gender = gender


def is_authenticated(self):
    return True


def is_active(self):
    return True


def is_anonymous(self):
    return False


def __repr__(self):
    return '<LoginId %r>' % (self.username)


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/login.html", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form.get('username')
    password = request.form.get('password')
    remember_me = False
    if 'remember_me' in request.form:
        remember_me = True
    registered_user = LoginId.query.filter_by(username=username, password=password).first()
    print(registered_user)
    if registered_user is None:
        flash('Username or Password is invalid', 'danger')
        return render_template("login.html")
    else:
        session['logged_in'] = True
        flash('Logged In successfully', 'success')
        return render_template('sunglasses.html')


@app.route("/register.html", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        '''Add entry to database'''
        username = request.form.get('username')
        password = request.form.get('password')
        c_password = request.form.get('c_password')
        email = request.form.get('email')
        contact = request.form.get('contact')
        gender = request.form.get('gender')
        secure = sha256_crypt.encrypt(str(password))
        if password == c_password and len(contact) == 10:
            entry = LoginId(username=username, password=password, c_password=c_password, email=email, contact=contact,
                             gender=gender)
            db.session.add(entry)
            db.session.commit()
            flash("You are successfully registerd", 'success')
        else:
            flash("Error while registering", 'danger')
            return render_template("register.html")
    return render_template('register.html')


@app.route("/sunglasses.html")
def sunglasses():
    return render_template('sunglasses.html')


@app.route("/eyeglasses.html")
def eyeglasses():
    return render_template('eyeglasses.html')


@app.route("/cls.html")
def lenses():
    return render_template('cls.html')


@app.route("/logout.html")
def logout():
    session['logged_in'] = False
    return render_template('logout.html')


if __name__ == "__main__":
    app.secret_key = '1234567dailycoding'
    app.run(debug=True)
