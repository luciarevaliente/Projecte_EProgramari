from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#Per totes les classes d'abaix, s'ha de comprovar que tots els atributs que ho requereixin siguin unics, no nul·ls...
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    surname = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    #S'ha de validar que la edat estigui entre 18 i 120

    @staticmethod
    def validate_age(age):
        if int(age) < 18 or int(age) > 120:
            raise ValueError("L'edat ha d'estar entre 18 i 120 anys.")
    


#Es modificarà

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

#És modificarà

class MedicalRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    diagnosis = db.Column(db.Text, nullable=False)
    treatment = db.Column(db.Text, nullable=False)
    doctor_notes = db.Column(db.Text, nullable=True)

    @staticmethod
    def validate_unique_record(user_id, diagnosis, treatment):
        existing_record = MedicalRecord.query.filter_by(user_id=user_id, diagnosis=diagnosis, treatment=treatment).first()
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


@app.route('/welcome/<username>')
def welcome(username):
    return render_template('welcome.html', username=username)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        surname = request.form['surname']
        password = request.form['password']
        email = request.form['email']
        email2 = request.form['email2']
        age = request.form['age']

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
            flash(str(e), 'error')
            return redirect(url_for('register'))

        new_user = User(username=username, surname=surname, password=password, email=email, age=age)
        db.session.add(new_user)
        db.session.commit()

        flash('Registre complet! Ara pots iniciar sessió.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
    if request.method == 'POST':
        user_id = request.form['user_id']
        date = request.form['date']
        time = request.form['time']
        description = request.form['description']

        # Validació de 'appointment' únic. 
        try:
            Appointment.validate_unique_appointment(user_id, date, time)
        except ValueError as e:
            flash(str(e), 'error')
            return redirect(url_for('appointments'))
        
        new_appointment = Appointment(user_id=user_id, date=date, time=time, description=description)
        db.session.add(new_appointment)
        db.session.commit()

        flash('Cita mèdica registrada correctament!', 'success')
        return redirect(url_for('appointments'))

    all_appointments = Appointment.query.all()
    return render_template('appointments.html', appointments=all_appointments)


@app.route('/medical_records', methods=['GET', 'POST'])
def medical_records():
    if request.method == 'POST':
        user_id = request.form['user_id']
        diagnosis = request.form['diagnosis']
        treatment = request.form['treatment']
        doctor_notes = request.form['doctor_notes']

        # Validació de 'medical_record' únic. 
        try:
            MedicalRecord.validate_unique_record(user_id, diagnosis, treatment)
        except ValueError as e:
            flash(str(e), 'error')
            return redirect(url_for('medical_records'))

        new_record = MedicalRecord(user_id=user_id, diagnosis=diagnosis, treatment=treatment, doctor_notes=doctor_notes)
        db.session.add(new_record)
        db.session.commit()

        flash('Registre mèdic creat correctament!', 'success')
        return redirect(url_for('medical_records'))

    all_records = MedicalRecord.query.all()
    return render_template('medical_records.html', records=all_records)

if __name__ == '__main__':
    app.run(debug=True)
