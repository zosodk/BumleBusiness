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
        #print(f"Fejl ved forbindelse til databasen: {e}")
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
                menuitem TEXT,
                description TEXT,
                parentnr INTEGER,
                FOREIGN KEY (parentnr) REFERENCES mainmenu(nr)
            )
        """)
        conn.commit()

    elif tablename == "logdata":
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logdata (
                nr INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                level TEXT,
                event TEXT,
                user TEXT,
                src_ip TEXT,
                dest_host TEXT,
                dest_port INTEGER,
                status TEXT,
                msg LONGTEXT
            )
        """)
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
        query = "INSERT OR REPLACE INTO submenu (nr, menuitem, description, parentnr) VALUES (?, ?, ?, ?)"
        cursor.execute(query, (nr, menuitem, description, parentnr))
    #
    conn.commit()
    #print(f"Succes! {name} er tilføjet.")
    return cursor.lastrowid

def insert_logdata(conn,tablename,  logdata):
    """
    denne funtkion modtager en dictionary(logdata) fra log_parser
    som den tilføjer til databasen table logdata
    :param conn:
    :param tablename:
    :param logdata:
    :return: bool angående om der opstår en fejl eller ej
    """
    try:
        cursor = conn.cursor()
        if tablename == "logdata":
            #tabel_cleaner(conn, tablename) //Fjernet denne, da den konsekvent sletter alt data i tabellen hver gang den indsætter en linie....
            query = "INSERT OR REPLACE INTO logdata (timestamp, level, event, user, src_ip, dest_host, dest_port, status, msg) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
            cursor.execute(query,(logdata["timestamp"],logdata["level"],logdata["event"],logdata["user"],logdata["src_ip"],logdata["dest_host"],logdata["dest_port"],logdata["status"],logdata["msg"]))
        conn.commit()
        return True
    except Error as e:
        print(f"fejl ved inerting af logdata: {e}")
        return False

def tabel_cleaner(conn, tablename):
    """
    Sletter alt data et tabel indeholder
    :param conn:
    :param tablename:
    :return: bool angående om der sker en fejl eller ej
    """
    try:
        cursor = conn.cursor()
        cursor.execute(f"Delete FROM {tablename}")
        # 2. Nulstil tælleren (starter fra 1 ved næste INSERT)
        cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{tablename}';")
        return True
    except Error as e:
        print(f"fejl under rensing af table: {e}")
        return False


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

    tabel = fetch_all_from_table(connection, "logdata")
    print(tabel)
