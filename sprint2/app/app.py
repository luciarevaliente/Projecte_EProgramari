from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
UPLOAD_FOLDER = 'instance'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    surname = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    @staticmethod
    def validate_age(age):
        if int(age) < 18 or int(age) > 120:
            raise ValueError("L'edat ha d'estar entre 18 i 120 anys.")
    


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)

    @staticmethod
    def validate_unique_appointment(user_id, date, time):
        existing_appointment = Appointment.query.filter_by(user_id=user_id, date=date, time=time).first()
        if existing_appointment:
            raise ValueError("Aquesta cita ja està registrada per aquest usuari a aquesta data i hora.")


class MedicalRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    grup_sanguini = db.Column(db.Text, nullable=False)
    condicions_especials = db.Column(db.Text, nullable=True)
    medicacio_actual = db.Column(db.Text, nullable=True)
    llista_alergies = db.Column(db.Text, nullable=True)

    @staticmethod
    def validate_unique_record(user_id, grup_sanguini, condicions_especials, medicacio_actual, llista_alergies):
        existing_record = MedicalRecord.query.filter_by(user_id=user_id, grup_sanguini=grup_sanguini, medicacio_actual=medicacio_actual, condicions_especials=condicions_especials, llista_alergies=llista_alergies).first()
        if existing_record:
            raise ValueError("Aquest registre mèdic ja existeix per a aquest usuari.")

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            return redirect(url_for('welcome', username=username))
        else:
            flash('Usuari o contrasenya incorrectes!', 'error')
    return render_template('login.html')

@app.route('/upload/<username>', methods=['GET','POST'])
def upload(username):
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Cap fitxer seleccionat')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('Cap fitxer seleccionat')
            return redirect(request.url)

        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            flash(f"Fitxer {file.filename} pujat correctament!")
            return redirect(url_for('appointments',username=username))

    return render_template('upload.html',username=username)

@app.route('/welcome/<username>')
def welcome(username):
    # Busca l'usuari a la base de dades
    user = User.query.filter_by(username=username).first()
    if not user:
        print("Usuari no trobat!", "error")
        return redirect(url_for('login'))
    
    # Obté les cites associades a l'usuari
    appointments = Appointment.query.filter_by(user_id=user.username).all()
    print(user.username,appointments)
    # Passa les cites al template
    return render_template('welcome.html', username=username, appointments=appointments)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name=request.form['name']
        username = request.form['username']
        surname = request.form['surname']
        password = request.form['password']
        email = request.form['email']
        email2 = request.form['email2']
        age = request.form['age']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Aquest user-name ja està registrat.', 'error')
            return redirect(url_for('register'))

        # Comprova correu duplicat
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Aquest correu electrònic ja està registrat.', 'error')
            return redirect(url_for('register'))

        # Comprova correus coincidents
        if email != email2:
            flash('Els correus electrònics no coincideixen.', 'error')
            return redirect(url_for('register'))

        # Valida edat
        try:
            User.validate_age(age)
        except ValueError as e:
            flash("Rang d'edat permès 18-120.", 'error')
            return redirect(url_for('register'))

        new_user = User(name=name, surname=surname, username=username,password=password, email=email, age=age)
        db.session.add(new_user)
        db.session.commit()

        flash('Registre complet! Ara pots iniciar sessió.', 'success')
        return redirect(url_for('choose', username=username))

    return render_template('register.html')

@app.route('/choose/<username>', methods=['GET','POST'])
def choose(username):
    if request.method == 'POST':

        accio = request.form['action']
        if accio == 'primer':
            return redirect(url_for('medical_records',username=username))
        if accio == 'segon':
            return redirect(url_for('welcome', username=username))

    return render_template('choose.html', username=username)

@app.route('/appointments/<username>', methods=['GET', 'POST'])
def appointments(username):
    if request.method == 'POST':
        user_id = username
        date = request.form['date']
        time = request.form['time']
        description = request.form['description']

        # Validació de 'appointment' únic. 
        try:
            Appointment.validate_unique_appointment(user_id, date, time)
        except ValueError as e:
            flash(str(e), 'error')  # Afegeix un missatge flash amb el detall de l'error
            return redirect(url_for('appointments', username=user_id))
        
        new_appointment = Appointment(user_id=user_id, date=date, time=time, description=description)
        db.session.add(new_appointment)
        db.session.commit()

        flash('Cita mèdica registrada correctament!', 'success')  # Missatge d'èxit
        return redirect(url_for('welcome', username=user_id))

    all_appointments = Appointment.query.all()
    return render_template('appointments.html', appointments=all_appointments)


@app.route('/medical_records/<username>', methods=['GET', 'POST'])
def medical_records(username):
    if request.method == 'POST':
        username = username
        alergies = request.form['llista_alergies']
        grup_sanguini = request.form['grup_sanguini']
        condicions_especials = request.form['condicions_especials']
        medicacio_actual = request.form['medicacio_actual']
        llista_alergies = ','.join([a.strip() for a in alergies.split(',')])

        # Validació de 'medical_record' únic. 
        try:
            MedicalRecord.validate_unique_record(username, grup_sanguini, medicacio_actual, condicions_especials, llista_alergies)
        except ValueError as e:
            flash(str(e), 'error')
            return redirect(url_for('medical_records',username=username))

        new_record = MedicalRecord(user_id=username, grup_sanguini=grup_sanguini, medicacio_actual=medicacio_actual, condicions_especials=condicions_especials, llista_alergies=llista_alergies)
        db.session.add(new_record)
        db.session.commit()

        flash('Registre mèdic creat correctament!', 'success')
        return redirect(url_for('upload',username=username))

    all_records = MedicalRecord.query.all()
    return render_template('medical_records.html', records=all_records, username=username)

if __name__ == '__main__':
    app.run(debug=True)
