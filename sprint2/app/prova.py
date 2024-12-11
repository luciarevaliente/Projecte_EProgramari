import sqlite3

# Ruta a la base de dades
db_path = 'instance/database.db'  # Canvia aquest camí si la teva base de dades està en un altre lloc

try:
    # Conecta a la base de dades
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("Taules a la base de dades:")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for table in tables:
        print(f"\nTaula: {table[0]}")
        print("Estructura de la taula:")
        
        # Obtenir l'estructura de cada taula
        cursor.execute(f"PRAGMA table_info({table[0]});")
        columns = cursor.fetchall()
        for column in columns:
            print(f"  - {column[1]} ({column[2]}) {'NOT NULL' if column[3] else ''} {'PRIMARY KEY' if column[5] else ''}")

except sqlite3.DatabaseError as e:
    print(f"Error amb la base de dades: {e}")
finally:
    # Tanca la connexió
    if 'conn' in locals():
        conn.close()
