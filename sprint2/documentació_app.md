

## **DOCUMENTACIÓ DE L'APLICACIÓ**

### **DESENVOLUPAMENT DE L'APLICACIÓ**

L'aplicació ha estat desenvolupada utilitzant Flask, un microframework que ofereix una arquitectura flexible i eficient per a aplicacions web. Per a la gestió de dades, s'ha integrat SQLAlchemy, que proporciona una interfície d'ORM (Object-Relational Mapping) per interactuar amb la base de dades de manera senzilla. L'aplicació inclou funcionalitats bàsiques com el registre i autenticació d'usuaris, la gestió de cites mèdiques i la visualització de registres mèdics. Aquestes funcionalitats s'han implementat amb una separació lògica de responsabilitats, apropant-se al patró MVC, on els models encapsulen les dades, les vistes gestionen la interfície d'usuari i els controladors connecten els dos elements.

PER ACABAR---------------------------------
---

### **ESTILS DE L'APLICACIÓ**

Els estils visuals es defineixen a través del fitxer `style.css`. S'han dissenyat elements visuals moderns, mantenint un equilibri entre simplicitat i funcionalitat. Els formularis són clars i fàcils d'utilitzar, els botons tenen un estil coherent per guiar l'usuari i els esquemes de colors s'han triat per assegurar una bona llegibilitat. L'aplicació és responsive, adaptant-se a diferents dispositius per millorar l'experiència d'usuari tant en pantalles petites com grans.

PER ACABAR---------------------------------
---

### **CREACIÓ BASE DE DADES**

La base de dades s'ha creat utilitzant SQLAlchemy, que permet definir l'estructura en Python mitjançant classes. Aquesta base de dades és de tipus relacional, ja que organitza la informació en taules amb relacions definides entre elles. Per exemple, la taula `User` representa els usuaris registrats, la taula `Appointment` gestiona les cites mèdiques i la taula `MedicalRecord` conté els registres mèdics associats. Les relacions entre aquestes taules es defineixen mitjançant claus foranes. Així, `Appointment` i `MedicalRecord` estan vinculades a `User` a través del camp `user_id`, assegurant que cada cita o registre mèdic estigui associat a un usuari existent.

Les dades es garanteixen coherents gràcies a les restriccions com `NOT NULL`, que assegura que els camps necessaris no quedin buits, i `UNIQUE`, que evita duplicats en camps com el correu electrònic. Aquest tipus de base de dades és ideal per assegurar la integritat i consistència de la informació en aplicacions amb relacions complexes entre entitats, com usuaris, cites i registres mèdics.

---

### **DEFINICIÓ DE LES TAULES**

La taula `User` representa els usuaris de l'aplicació i inclou camps com el nom d'usuari, el correu electrònic, la contrasenya i l'edat. La seva estructura garanteix que el correu sigui únic per evitar conflictes, i l'edat només permet valors entre 18 i 120 anys, assegurant registres vàlids. Aquesta taula està relacionada amb altres taules com `Appointment` i `MedicalRecord`, ja que un usuari pot tenir múltiples cites i registres mèdics.

La taula `Appointment` s'encarrega de gestionar les cites mèdiques. Cada cita està vinculada a un usuari mitjançant el camp `user_id`, que és una clau forana que assegura la integritat referencial. Per evitar conflictes, es garanteix que una combinació de `user_id`, data i hora sigui única. Això assegura que un usuari no pugui tenir dues cites a la mateixa hora.

La taula `MedicalRecord` conté els registres mèdics associats als usuaris. Aquesta taula també està vinculada a `User` mitjançant `user_id`. Per garantir la consistència, els camps `user_id`, diagnòstic i tractament són únics en combinació. Això evita que es registrin duplicats per al mateix usuari amb el mateix diagnòstic i tractament.

---

### **COM S'HA CREAT LA BASE DE DADES?**

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

### **AVANTATGE D'UNA BDR PER AQUEST PROJECTE**

1. **Integritat de les dades**: L'ús de claus foranes i restriccions com `NOT NULL` i `UNIQUE` asseguren dades consistents.
2. **Fàcil consulta amb SQL**: És senzill obtenir dades mitjançant consultes SQL, per exemple:
   - Totes les cites d'un usuari: `SELECT * FROM appointment WHERE user_id = ?`
   - Tots els registres mèdics d'un usuari: `SELECT * FROM medical_record WHERE user_id = ?`
3. **Escalabilitat**: Si l'aplicació creix, es poden afegir més taules i relacions fàcilment.
4. **Integració amb SQLAlchemy**: L'ORM facilita la manipulació de dades en Python sense haver d'escriure SQL manualment.

---

### **PATRONS UTILITZATS AL PROJECTE**

En el desenvolupament d'aquest projecte s'han aplicat diversos patrons de disseny. Un d'ells és el patró MVC (Model-View-Controller). Els models estan representats per les classes SQLAlchemy que encapsulen la lògica de dades i les seves validacions. Les vistes són els fitxers HTML que gestionen la interfície d'usuari i presenten les dades de manera amigable. Els controladors són les rutes definides al fitxer principal, que connecten les dades amb les vistes i gestionen la lògica de negoci.

També es pot identificar el patró Singleton a través de la gestió centralitzada de la base de dades. SQLAlchemy assegura que només hi hagi una instància activa de connexió a la base de dades durant tota l'execució de l'aplicació. A més, la configuració inicial de l'aplicació segueix un enfocament proper al patró Factory, que permet crear i configurar l'entorn de l'aplicació de manera modular i escalable.

Aquestes decisions de disseny garanteixen que l'aplicació sigui fàcil de mantenir, escalable i segura, assegurant una separació clara de responsabilitats entre els components.

