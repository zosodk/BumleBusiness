import sqlite3
from sqlite3 import Error

def connect_to_db(db_name="bumlebusiness.db"):
    """
    Opretter og returnerer en forbindelse til SQLite databasen.
    returnerer en forbindelse til SQLite databasen, eller en fejl, hvis det ikke er muligt.
    """
    try:
        # opretter forbindelsen
        conn = sqlite3.connect(db_name)
        return conn
    except Error as e:
        print(f"Fejl ved forbindelse til databasen: {e}")
        return None

def create_main_tables(conn, tablename):
    """
    Opret tabeller, hvis de ikke allerede findes.
    :param conn: forbindelse til databasen
    :param tablename: navnet på tabellen der skal oprettes
    """
    cursor = conn.cursor()
    # tablename == mainmenu
    if tablename == "mainmenu":
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mainmenu (
                nr INTEGER PRIMARY KEY,
                menuitem TEXT,
                description TEXT
            )
        """)

    elif tablename == "submenu":
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS submenu (
                nr INTEGER PRIMARY KEY,
                parentnr INTEGER,
                menuitem TEXT,
                description TEXT,
                FOREIGN KEY (parentnr) REFERENCES mainmenu(nr)
            )
        """)
        cursor.execute("")
        conn.commit()
    return cursor

def insert_menu_item(conn, tablename, nr, menuitem, description, parentnr=1):
    """
    Indsætter en ny elementer i tabel.
    """
    cursor = conn.cursor()
    if tablename == "mainmenu":
        query = "INSERT OR REPLACE INTO mainmenu (nr, menuitem, description) VALUES (?, ?, ?)"
        cursor.execute(query, (nr, menuitem, description))
    elif tablename == "submenu":
        query = "INSERT OR REPLACE INTO submenu (nr, parentnr, menuitem, description) VALUES (?, ?, ?, ?)"
        cursor.execute(query, (nr, parentnr, menuitem, description))
    #
    conn.commit()
    #print(f"Succes! {name} er tilføjet.")
    return cursor.lastrowid

def fetch_all_from_table(conn, tablename):
    """
    Henter alt fra en angivet tabel returner indhold
    """
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {tablename}")
    return cursor.fetchall()

def generate_mainmenu_elements(connection):
    """
    Genererer database indgange for at vi kan skabe en grafiskbrugerflade senere hen
    :param connection: Connection til databasen
    """
    #Mainmenu skal altid laves først, da submenu er afhængig af mainmenu
    create_main_tables(connection, "mainmenu")
    create_main_tables(connection, "submenu")

    #Mainmenu items - nr bliver ikke talt op automatisk - skal angives. Hvis ikke dette bliver gjort, da vil den blive overskrevet:
    insert_menu_item(connection, "mainmenu", 1, "1 - INDLÆSNING AF LOGFIL", "Dette område giver dig mulighed for at indlæse en logfil.")

    #Submenu items:
    #Husk at tælle nr op - samt at referere til den korrekte hovedmenu - parentnr
    #Hvis den eksisterer i forvejen, da overskrives den blot (INSERT INTO OR REPLACE)
    insert_menu_item(connection, "submenu", 1, "1 - Indlæs den rå logfil ", "Indlæser den oprindelige logfil fra disken", 1)
    insert_menu_item(connection, "submenu", 2, "2 - Overfør logdata til database", "Genererer database elementer fra logfil", 1)


if __name__ == "__main__":
    #Test af funktionalitet
    connection = connect_to_db()
    create_main_tables(connection, "mainmenu")
    create_main_tables(connection, "submenu")
    insert_menu_item(connection, "mainmenu", 1, "1 - INDLÆSNING AF LOGFIL", "Dette område giver dig mulighed for at indlæse en logfil.")
    insert_menu_item(connection, "submenu", 1, "1 - Indlæs den rå logfil ", "Indlæser den oprindelige logfil fra disken", 1)
    insert_menu_item(connection, "submenu", 2, "2 - Overfør logdata til database", "Genererer database elementer fra logfil", 1)
    #Vær ops på, at når data udtrækkes, da kommer foreign key lige efter primary key i submenu
    tabel = fetch_all_from_table(connection, "submenu")
    print(tabel)
