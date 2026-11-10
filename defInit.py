from defDbHandler import *
from sqlite3 import Error
from defFileHandler import parse_logline

#DENNE SKAL ÆNDRES VED OVERGANG TIL GUI OG TEST AF DETTE
createlogdata = False


def init_db():
    """
    Initierer databasen med vigtige tabeller og menupunkter - kaldes altid ved programstart
    Udvides med yderligere punkter npr disse er klar
    """
    conn = connect_to_db("bumlebusiness.db")
    while conn is not None:
        create_main_tables(conn, "mainmenu")
        create_main_tables(conn, "submenu")
        create_main_tables(conn, "logdata")

        # Hovedmenu (nr 1-4 samt 0 til afslut)
        insert_menu_item(conn, "mainmenu", 1, "Bearbejdelse af logfil","Giver mulighed for at indlæse logfil, slette eksisterende log indhold og bearbejde logfil")
        insert_menu_item(conn, "mainmenu", 2, "Søgning i log indhold i databasen","Søg efter bruger, ip o.l. i databasen")
        insert_menu_item(conn, "mainmenu", 3, "Udvidet søgning", "Avancerede søgning med flere parametre")
        insert_menu_item(conn, "mainmenu", 4, "Visualisering af log data", "Giver mulighed for at visualisere log data")
        insert_menu_item(conn, "mainmenu", 0, "Afslut program", "Stopper programmet")

        # Undermenuer til Hovedmenu 1 (parentnr = 1)
        insert_menu_item(conn, "submenu", 1, "Vis log fil (cyber_security_log_sample.txt)","Viser den rå logfilen fra disken - gemmer ikke noget", 1)
        insert_menu_item(conn, "submenu", 2, "Indlæser logfil til tabel i databasen", "Undersøger logfil og indsætter data i databasen", 1)
        insert_menu_item(conn, "submenu", 3, "Vis log tabel fra databasen", "Viser alt log data i databasen", 1)
        insert_menu_item(conn, "submenu", 4, "Slet eksisterende log indhold fra databasen","Sletter alt logindhold i databasen", 1)
        insert_menu_item(conn, "submenu", 0, "Tilbage til hovedmenu", "Returnerer til hovedmenuen", 1)

        # Undermenuer til Hovedmenu 2 (parentnr = 2)
        insert_menu_item(conn, "submenu", 1, "Vis historik for en ip-adresse du angiver", "Viser tabel over ip's historik", 2)
        insert_menu_item(conn, "submenu", 2, "Vis historik for et brugernavn du angiver", "Viser tabel over brugers's historik", 2)
        insert_menu_item(conn, "submenu", 3, "Vis historik for en event type", "Viser event historik", 2)
        insert_menu_item(conn, "submenu", 4, "Vis historik for en level type", "Viser level (INFO, WARN, ALERT) historik", 2)
        insert_menu_item(conn, "submenu", 5, "Vis historik for status meddelelse", "Viser status besked historik (OK, FAILED, DENIED etc)", 2)
        insert_menu_item(conn, "submenu", 0, "Tilbage til hovedmenu", "Returnerer til hovedmenuen", 2)
        # Undermenuer til Hovedmenu 3 (parentnr = 3)
        insert_menu_item(conn, "submenu", 1, "Vis historik for en ip-adresse og event", "Viser tabel over historik", 3)
        insert_menu_item(conn, "submenu", 2, "Vis historik for et ip-adresse og level", "Viser tabel over historik", 3)
        insert_menu_item(conn, "submenu", 3, "Vis historik for ALERTS og Login_failed Events", "Viser historik", 3)
        insert_menu_item(conn, "submenu", 4, "Vis historik for alle ALERTS", "Viser ALERTS historik", 3)
        insert_menu_item(conn, "submenu", 5, "Vis historik for flere brugere fra samme IP", "Viser hvis flere brugere logger eller forsøger fra samme IP", 3)
        insert_menu_item(conn, "submenu", 0, "Tilbage til hovedmenu", "Returnerer til hovedmenuen", 3)
        # Undermenuer til Hovedmenu 4 (parentnr = 4)
        insert_menu_item(conn, "submenu", 1, "Vis piecharts","Indsæt data til dannelse af piechart", 4)
        insert_menu_item(conn, "submenu", 2, "Vis scatterplots","Indsæt data til dannelse af scatterplots", 4)
        insert_menu_item(conn, "submenu", 3, "Vis søjlediagrammer", "Indsæt data til dannelse af søjediagrammer", 4)
        insert_menu_item(conn, "submenu", 0, "Tilbage til hovedmenu", "Returnerer til hovedmenuen", 4)

        conn.commit()
        break


def testdata():
    if createlogdata:
        conn = connect_to_db("bumlebusiness.db")
        tabel_cleaner(conn, "logdata")
        conn.commit()
        with open("cyber_security_log_sample.txt", "r", encoding="utf-8") as fil:
            for linie in fil:
                parsedline = parse_logline(linie)
                insert_logdata(conn, "logdata", parsedline)


if __name__ == "__main__":
    init_db()
    testdata()


