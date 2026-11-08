from defDbHandler import *
from sqlite3 import Error
from defFileHandler import parse_logline

#Hvis createlogdata er sat til True, vil logdata blive oprettet

createlogdata = True

def init_db():
    # Opretter forbindelse til databasen - skabes hvis den ikke findes
    conn = connect_to_db("bumlebusiness.db")
    while conn is not None:
        create_main_tables(conn,"mainmenu")
        create_main_tables(conn,"submenu")
        create_main_tables(conn,"logdata")
        #Udarbejdelse af hovedmenu emner
        insert_menu_item(conn, "mainmenu","1", "1 - Bearbejdelse af logfil", "Giver mulighed for at indlæse logfil, slette eksisterende log indhold fra databasen og bearbejde logfil")
        insert_menu_item(conn, "mainmenu", "2", "2 - Bearbejde log indhold i databasen", "Giver mulighed for at bearbejde log indhold i databasen")
        insert_menu_item(conn, "mainmenu", "3", "3 - Søgning i log data", "Giver mulighed for at søge i log data")
        insert_menu_item(conn, "mainmenu", "4", "4 - Visualisering af log data", "Giver mulighed for at visualisere log data")
        insert_menu_item(conn, "mainmenu", "0", "0 - Afslut program", "Stopper programmet")

        #Udarbejdelse af submenu emner

        insert_menu_item(conn, "submenu", "1", "1 - Indlæs log fil (cyber_security_log_sample.txt)", "Indlæser logfilen fra disken", "1")
        insert_menu_item(conn, "submenu", "2", "2 - Slet eksisterende log indhold fra databasen","Sletter alt logindhold i databasen", "1")
        insert_menu_item(conn, "submenu", "3", "3 - Bearbejdelse af logfil", "Render logfil igennem og indsætter data i databasen","1")
        insert_menu_item(conn, "submenu", "4", "0 - Tilbage til hovedmenu", "","0")

        # Udarbejdelse af logdata tabeller (eventtyper, loglevel, users, allowed_ports, allowed_hosts, allowed_ip, status
        break

def testdata():
    if createlogdata:
        conn = connect_to_db("bumlebusiness.db")
        tabel_cleaner(conn, "logdata")
        with open("cyber_security_log_sample.txt", "r", encoding="utf-8") as fil:
            for linie in fil:
                parsedline = parse_logline(linie)
                insert_logdata(conn,"logdata", parsedline)

if __name__ == "__main__":

    init_db()
    testdata()


