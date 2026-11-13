from defDbHandler import *

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
        insert_menu_item(conn, "submenu", 1, "Vis Piechart udfra en kolonne","Piechart over en kolonne af data", 4)
        insert_menu_item(conn, "submenu", 2, "Vis specifik Piechart", "Opretter piechart, der viser fordelingen af hændelser udfra parametre og kolonner.", 4)
        insert_menu_item(conn, "submenu", 3, "Vis Scatterplot diagram med eller uden tendenslinie","Giver mulighed for udvælgelse af akseværdier", 4)
        insert_menu_item(conn, "submenu", 4, "Vis Søjlediagrammer", "Giver mulighed for dannelse af søjediagrammer udfra valgte værdier", 4)
        insert_menu_item(conn, "submenu", 5, "Vis historikdiagram", "Viser historisk sammenhæng udfra valgte parametre", 4)
        insert_menu_item(conn, "submenu", 0, "Tilbage til hovedmenu", "Returnerer til hovedmenuen", 4)

        conn.commit()
        break

if __name__ == "__main__":
    init_db()


