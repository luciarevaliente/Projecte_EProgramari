

## **DOCUMENTACIÓ DE L'APLICACIÓ**

### **1. DESENVOLUPAMENT DE L'APLICACIÓ**

L'aplicació ha estat desenvolupada utilitzant Flask, un microframework que ofereix una arquitectura flexible i eficient per a aplicacions web. Per a la gestió de dades, s'ha integrat SQLAlchemy, que proporciona una interfície d'ORM (Object-Relational Mapping) per interactuar amb la base de dades de manera senzilla. L'aplicació inclou funcionalitats bàsiques com el registre i autenticació d'usuaris, la gestió de cites mèdiques i la visualització de registres mèdics. Aquestes funcionalitats s'han implementat amb una separació lògica de responsabilitats, apropant-se al patró MVC, on els models encapsulen les dades, les vistes gestionen la interfície d'usuari i els controladors connecten els dos elements.

PER ACABAR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

---
### **2. ESTILS DE L'APLICACIÓ**

Els estils visuals es defineixen a través del fitxer `style.css`. S'han dissenyat elements visuals moderns, mantenint un equilibri entre simplicitat i funcionalitat. Els formularis són clars i fàcils d'utilitzar, els botons tenen un estil coherent per guiar l'usuari i els esquemes de colors s'han triat per assegurar una bona llegibilitat. L'aplicació és responsive, adaptant-se a diferents dispositius per millorar l'experiència d'usuari tant en pantalles petites com grans.

PER ACABAR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

---

### **3. CREACIÓ BASE DE DADES**

La base de dades s'ha creat amb SQLAlchemy, un ORM que permet definir l'estructura utilitzant classes Python i gestionar les dades sense escriure SQL manual. És una base de dades relacional, on les taules (User, Appointment, MedicalRecord) estan vinculades mitjançant claus foranes per mantenir la integritat referencial. SQLAlchemy aplica restriccions com NOT NULL i UNIQUE per assegurar la coherència i consistència de les dades, oferint una gestió senzilla i escalable per a aplicacions complexes.


   ### **Definició de les taules**

La taula `User` representa els usuaris de l'aplicació i inclou camps com el nom d'usuari, el correu electrònic, la contrasenya i l'edat. La seva estructura garanteix que el correu sigui únic per evitar conflictes, i l'edat només permet valors entre 18 i 120 anys, assegurant registres vàlids. Aquesta taula està relacionada amb altres taules com `Appointment` i `MedicalRecord`, ja que un usuari pot tenir múltiples cites i registres mèdics.

La taula `Appointment` s'encarrega de gestionar les cites mèdiques. Cada cita està vinculada a un usuari mitjançant el camp `user_id`, que és una clau forana que assegura la integritat referencial. Per evitar conflictes, es garanteix que una combinació de `user_id`, data i hora sigui única. Això assegura que un usuari no pugui tenir dues cites a la mateixa hora.

La taula `MedicalRecord` conté els registres mèdics associats als usuaris. Aquesta taula també està vinculada a `User` mitjançant `user_id`. Per garantir la consistència, els camps `user_id`, diagnòstic i tractament són únics en combinació. Això evita que es registrin duplicats per al mateix usuari amb el mateix diagnòstic i tractament.


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


### **Avatatges d'una BDR per al projecte**

1. **Integritat de les dades**: L'ús de claus foranes i restriccions com `NOT NULL` i `UNIQUE` asseguren dades consistents.
2. **Fàcil consulta amb SQL**: És senzill obtenir dades mitjançant consultes SQL, per exemple:
   - Totes les cites d'un usuari: `SELECT * FROM appointment WHERE user_id = ?`
   - Tots els registres mèdics d'un usuari: `SELECT * FROM medical_record WHERE user_id = ?`
3. **Escalabilitat**: Si l'aplicació creix, es poden afegir més taules i relacions fàcilment.
4. **Integració amb SQLAlchemy**: L'ORM facilita la manipulació de dades en Python sense haver d'escriure SQL manualment.


### **Patrons utilitzats**

En el desenvolupament d'aquest projecte s'han aplicat diversos patrons de disseny. Un d'ells és el patró MVC (Model-View-Controller). Els models estan representats per les classes SQLAlchemy que encapsulen la lògica de dades i les seves validacions. Les vistes són els fitxers HTML que gestionen la interfície d'usuari i presenten les dades de manera amigable. Els controladors són les rutes definides al fitxer principal, que connecten les dades amb les vistes i gestionen la lògica de negoci.

També es pot identificar el patró Singleton a través de la gestió centralitzada de la base de dades. SQLAlchemy assegura que només hi hagi una instància activa de connexió a la base de dades durant tota l'execució de l'aplicació. A més, la configuració inicial de l'aplicació segueix un enfocament proper al patró Factory, que permet crear i configurar l'entorn de l'aplicació de manera modular i escalable.

---

### **4. TESTING DE L'APLICACIÓ**

Els tests de l'aplicació es desenvolupen utilitzant el mòdul `unittest` de Python per assegurar la fiabilitat i coherència de les funcionalitats principals. A continuació es descriu com es defineixen i executen les proves, així com els objectius de cada test.

#### **Configuració dels tests**

Els tests es realitzen sobre una base de dades temporal en memòria (`sqlite:///:memory:`) que es crea i es destrueix per a cada sessió de test. Aquesta configuració evita alterar la base de dades real i permet realitzar proves aïllades.

- **Mètode `setUp`**: Configura un entorn de test creant una nova base de dades abans de cada prova.
- **Mètode `tearDown`**: Elimina totes les dades i taules després de cada prova per garantir que no hi hagi contaminació entre tests.

```python
def setUp(self):
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    self.app = app.test_client()
    with app.app_context():
        db.create_all()

def tearDown(self):
    with app.app_context():
        db.session.remove()
        db.drop_all()
```

#### **Proves implementades**

1. **Test de registre d'usuari (`test_register_user`)**  
   Aquesta prova comprova que es pot registrar un usuari correctament. Es fa una petició `POST` amb les dades de registre, i posteriorment es valida que l'usuari s'hagi guardat a la base de dades.

   Objectiu: Assegurar que el procés de registre funciona correctament.

2. **Test d'email únic (`test_unique_email`)**  
   Verifica que no es poden registrar dos usuaris amb el mateix correu electrònic. Si s'intenta, es genera una excepció `IntegrityError`.

   Objectiu: Garantir que la restricció `UNIQUE` sobre el camp `email` funciona.

3. **Test de validació d'edat (`test_age_validation`)**  
   Comprova que només es permeten valors d'edat entre 18 i 120 anys. Si es proporcionen valors fora d'aquest rang, es genera una excepció `ValueError`.

   Objectiu: Assegurar que els registres d'usuaris compleixen la validació d'edat.

Si totes les proves passen correctament, es garanteix que les funcionalitats testejades funcionen com s'espera. Aquesta test és fonamental per assegurar la qualitat del codi i detectar errors abans del desplegament.
