import sqlite3
from sqlite3 import Error

def connect_to_db(db_name="bumlebusiness.db"):
    """
    Opretser og returnerer en forbindelse til SQLite databasen.
    returnerer en forbindelse til SQLite databasen, eller en fejl, hvis det ikke er muligt.
    """
    try:
        # opretter forbindelsen
        conn = sqlite3.connect(db_name)
        return conn
    except Error as e:
        print(f"Fejl ved forbindelse til databasen: {e}")
        return None

def create_table(conn, tablename):
    """
    Opret en tabel hvis den ikke allerede findes.
    """
    cursor = conn.cursor()
    # Eksempel på en tabel til studerende
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {tablename} ( id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT, gender TEXT, birth_year INTEGER, has_former_degree INTEGER)")
    conn.commit()
    return cursor

def insert_items(conn, tablename, **items):
    """
    Indsætter en ny elementer i tabel.
    """
    cursor = conn.cursor()
    query = "INSERT INTO test (name, gender, **birth_year, has_former_degree) VALUES (?, ?, ?, ?)"
    cursor.execute(query, (name, gender, birth_year, has_former_degree))
    conn.commit()
    print(f"Succes! {name} er tilføjet.")
    return cursor.lastrowid

def fetch_all_from_table(conn, tablename):
    """
    Henter alt fra en angivet tabel returner indhold
    """
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {tablename}")
    return cursor.fetchall()


connection = connect_to_db()
create_table(connection, "test")
insert_student(connection, "Maria", "M", 2021, True)
tabel = fetch_all_from_table(connection, "test")
print(tabel)
