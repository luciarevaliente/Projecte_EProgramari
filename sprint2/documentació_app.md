



### **DESENVOLUPAMENT DE L'APLICACIÓ**
---
### **ESTILS DE L'APLICACIÓ**
---
### **CREACIÓ BASE DE DADES**

La base de dades s'ha creat utilitzant **SQLAlchemy**, un ORM (Object-Relational Mapping) que permet definir l'estructura de la base de dades utilitzant classes Python. Aquesta base de dades és **relacional**, ja que organitza la informació en taules amb relacions definides entre elles. A continuació s'explica per què és relacional, així com les taules creades i les seves característiques.

1. **Estructura basada en taules**: La informació es guarda en taules (`User`, `Appointment`, `MedicalRecord`) on cada fila representa un registre únic.
2. **Relacions entre taules**: Hi ha **claus foranes** que estableixen vincles entre taules, com per exemple:
   - La taula `Appointment` té una columna `user_id` que fa referència a l'usuari propietari de la cita.
   - La taula `MedicalRecord` també utilitza `user_id` per relacionar-se amb la taula `User`.
3. **Integritat referencial**: Les relacions garanteixen que cada cita o registre mèdic estigui associat a un usuari existent. Això evita registres "orfes" a la base de dades.

Aquest tipus de base de dades és adequat perquè l'aplicació tracta dades estructurades amb relacions clares entre entitats (usuaris, cites i registres mèdics). Els sistemes de bases de dades relacionals són ideals per a aplicacions on es necessita assegurar la coherència i integritat de les dades.

### **Definició de les taules**
La taula **User** representa els usuaris registrats a l'aplicació. Està relacionada amb altres taules mitjançant una relació un-a-molts amb la taula **Appointment**, ja que un usuari pot tenir moltes cites, i amb la taula **MedicalRecord**, ja que un usuari pot tenir molts registres mèdics. Aquesta taula inclou diverses restriccions, com que el camp *email* ha de ser únic per evitar duplicats i que el camp *age* només admet valors entre 18 i 120 anys per assegurar que els registres siguin vàlids.

La taula **Appointment** s'utilitza per gestionar les cites mèdiques. Està vinculada a la taula **User** mitjançant el camp *user_id*, que identifica l'usuari que té la cita. Aquesta taula aplica restriccions perquè *user_id*, *date* i *time* siguin únics, evitant així duplicats. A més, la clau forana *user_id* garanteix que només es poden registrar cites per a usuaris que existeixen a la taula **User**.

La taula **MedicalRecord** s'encarrega de gestionar els registres mèdics associats als usuaris. Està relacionada amb la taula **User** mitjançant el camp *user_id*, que identifica l'usuari associat al registre mèdic. Les restriccions inclouen que els camps *user_id*, *diagnosis* i *treatment* han de ser únics per evitar duplicats i assegurar la consistència dels registres.


### **Com s'ha creat la base de dades?**
1. **Configuració inicial amb SQLAlchemy**:
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
   db = SQLAlchemy(app)
   ```
   - Es defineix SQLite com a sistema de gestió de bases de dades.
   - `database.db` és el fitxer que emmagatzema les dades.

2. **Execució de `db.create_all()`**:
   ```python
   with app.app_context():
       db.create_all()
   ```
   - SQLAlchemy llegeix les definicions de les classes i crea automàticament les taules corresponents amb les restriccions definides.

---

### **Avantatges d'una base de dades relacional per aquest projecte**
1. **Integritat de les dades**: L'ús de claus foranes i restriccions com `NOT NULL` i `UNIQUE` asseguren dades consistents.
2. **Fàcil consulta amb SQL**: És senzill obtenir dades mitjançant consultes SQL, per exemple:
   - Totes les cites d'un usuari: `SELECT * FROM appointment WHERE user_id = ?`
   - Tots els registres mèdics d'un usuari: `SELECT * FROM medical_record WHERE user_id = ?`
3. **Escalabilitat**: Si l'aplicació creix, es poden afegir més taules i relacions fàcilment.
4. **Integració amb SQLAlchemy**: L'ORM facilita la manipulació de dades en Python sense haver d'escriure SQL manualment.

---
### **Patrons utilitzats al projecte**

En el projecte, s'han aplicat alguns patrons de disseny implícits o estructures que segueixen principis relacionats amb patrons populars. A continuació, analitzem si s'han utilitzat patrons com **Singleton**, **MVC**, entre altres:

---

### **1. Patró MVC (Model-View-Controller)**

**Sí, s'ha utilitzat el patró MVC en certa manera, però de forma parcial.**

- **Model (M)**: 
  - Representat per les classes de models (`User`, `Appointment`, `MedicalRecord`) definides amb SQLAlchemy. Aquestes classes encapsulen la lògica de dades i les seves relacions, així com algunes validacions.
  - Exemples:
    ```python
    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(150), nullable=False)
        email = db.Column(db.String(150), nullable=False, unique=True)
    ```
  
- **View (V)**: 
  - Representat pels fitxers HTML que es troben al directori `templates`. Aquests fitxers mostren les dades i s'encarreguen de la interacció amb l'usuari.
  - Exemples:
    - `login.html`: Formulari per iniciar sessió.
    - `medical_records.html`: Taula que mostra registres mèdics.

- **Controller (C)**: 
  - Representat per les rutes definides al fitxer `app.py`. Aquestes rutes gestionen les sol·licituds de l'usuari, interactuen amb els models i renderitzen les vistes.
  - Exemples:
    ```python
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username, password=password).first()
            if user:
                return redirect(url_for('welcome', username=username))
        return render_template('login.html')
    ```

S'ha implementat un patró MVC bàsic. Encara es pot millorar separant millor la lògica del controlador i implementant fitxers específics per a cada component (Models, Views, Controllers).

