import sqlite3
from sqlite3 import Error

def connect_to_db(db_name="bumlebusiness.db"):
    """
    Opretter og returnerer en forbindelse til SQLite databasen.
    returnerer en forbindelse til SQLite databasen, eller en fejl, hvis det ikke er muligt.
    :param db_name
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
        conn.commit()

    elif tablename == "submenu":
        #Ændret SQL til at have en sammensat primærnøgle - når GUI menu generator laves, da er dette nemmer
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS submenu (
                nr INTEGER,
                menuitem TEXT,
                description TEXT,
                parentnr INTEGER,
                PRIMARY KEY (parentnr, nr),
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
        conn.commit()
    return cursor

def insert_menu_item(conn, tablename, nr, menuitem, description, parentnr=1):
    """
    Indsætter et nyt menupunkt i tabel. - kan bruges til både hoved og undermenu, da hovedmenu ikke bruger parentnr til noget - så denne ignoreres
    :param conn
    :param tablename
    :param nr
    :param menuitem
    :param description
    :param parentnr
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
        print(f"fejl ved inserting af logdata: {e}")
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
        conn.commit()
        return True
    except Error as e:
        print(f"fejl under rensing af table: {e}")
        return False


def fetch_all_from_table(conn, tablename):
    """
    Henter alt fra en angivet tabel returner indhold
    :param conn
    :param tablename
    """
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {tablename}")
    return cursor.fetchall()
def fetch_distinct_from_table(conn, tablename, parameter):
    """
    Henter specefic data fra et table
    :param conn
    :param tablename
    :param parameter
    """
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT DISTINCT {parameter} FROM {tablename}")
        return cursor.fetchall()
    except Error as e:
        print(f"fejl under udtræk af tabel - forkert angivet navn på tabel: {e}")

def fetch_coloumns_table(conn, tablename):
    """
    Henter kolonnenavne fra en tabel
    :param tablename
    :param conn
    """
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT name FROM PRAGMA_TABLE_INFO('{tablename}')")
        return cursor.fetchall()
    except Error as e:
        print(f"fejl under udtræk af navne - forkert angivet navn på tabel: {e}")


if __name__ == "__main__":
    #Test af funktionalitet
    connection = connect_to_db()
    #create_main_tables(connection, "mainmenu")
    #create_main_tables(connection, "submenu")
    #insert_menu_item(connection, "mainmenu", 1, "1 - INDLÆSNING AF LOGFIL", "Dette område giver dig mulighed for at indlæse en logfil.")
    #insert_menu_item(connection, "submenu", 1, "1 - Indlæs den rå logfil ", "Indlæser den oprindelige logfil fra disken", 1)
    #insert_menu_item(connection, "submenu", 2, "2 - Overfør logdata til database", "Genererer database elementer fra logfil", 1)

   # create_main_tables(connection, "logdata")
    #insert_logdata(connection, "logdata", {'timestamp': '2026-03-02T08:06:21', 'level': 'ALERT', 'event': 'MALWARE_SIGNATURE_MATCH', 'user': 'svc_backup', 'src_ip': '198.51.100.200', 'dest_host': 'mail01', 'dest_port': '445', 'status': 'BLOCKED', 'msg': 'Known malware signature matched'})
    #Vær ops på, at når data udtrækkes, da kommer foreign key lige efter primary key i submenu
    tabel = fetch_coloumns_table(connection, "logdata")
    print(tabel)
