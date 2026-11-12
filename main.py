from defDbHandler import connect_to_db, fetch_all_from_table, tabel_cleaner, insert_logdata,fetch_distinct_from_table
from defFileHandler import openLogfile, parse_logline
from defInit import init_db
from defGUI import console, clear_screen, draw_dos_box, ask_menu_choice, show_log_table, fetch_logdata_single, fetch_logdata_double, magic_print_list, console_print_list
from defDiagramMaker import *


def sorterings_vaerdi(item):
    foerste_element = item[0]

    if foerste_element == "0":
        return 999  # Send "0" om bag i køen
    else:
        return int(foerste_element)  # Lav om til tal for normal sortering

def get_menu_from_db(conn, table_name: str, parent_nr: int | None = None) -> list[tuple[str, str, str]]:
    """
    Henter menupunkter fra tabellen og bruger 'nr' direkte som nøgle.
    :param conn: database connection
    :param table_name: table name
    :param parent_nr: parent nr
    :return: menu items list
    """

    raw_rows = fetch_all_from_table(conn, table_name)
    menu_items = []

    if table_name == "mainmenu":
        for nr, menuitem, desc in raw_rows:
            menu_items.append((str(nr), menuitem, desc or ""))

    elif table_name == "submenu":
        for nr, menuitem, desc, p_nr in raw_rows:
            if int(p_nr) == int(parent_nr):
                menu_items.append((str(nr), menuitem, desc or ""))

    # Sorter så nr=0 (Tilbage/Afslut) altid ligger nederst
    # Nu sorterer vi listen ved at kalde vores nye funktion
    menu_items.sort(key=sorterings_vaerdi)
    return menu_items


def handle_submenu_1_actions(conn, choice: str):
    """
    Styrer hvad der sker når der tastes på skærmen/konsollen
    :param conn: database connection
    :param choice: choice
    """
    if choice == "1":
        console.print("\n[bold cyan]Indlæser og udskriver rå logfil (cyber_security_log_sample.txt)...[/]\n")
        openLogfile("cyber_security_log_sample.txt")
        console.print("\n[bold green]✔ Rå logfil udlæst til skærmen![/]")

    elif choice == "2":
        count = 0
        with open("cyber_security_log_sample.txt", "r", encoding="utf-8") as fil:
            for linie in fil:
                if linie.strip():
                    parsed = parse_logline(linie)
                    insert_logdata(conn, "logdata", parsed)
                    count += 1
        conn.commit()
        console.print(f"\n[bold green]✔ {count} loglinjer er parset og indsat i SQLite-databasen![/]")

    elif choice == "3":
        rows = fetch_all_from_table(conn, "logdata")
        if rows:
            show_log_table(rows[:], title=f"Visningstabel: Logdata ({len(rows)} rækker total)")

    elif choice == "4":
        if tabel_cleaner(conn, "logdata"):
            conn.commit()
            console.print("\n[bold green]✔ Alt eksisterende logindhold i databasen er nu slettet![/]")

def handle_submenu_2_actions(conn, choice: str):
    if choice == "1":
        #Udvalg af data til tabel historik udfra ipadresse
        print(f"Der er følgende ipadresser at vælge imellem i databasen: ")
        result = fetch_distinct_from_table(conn, "logdata", "src_ip")
        magic_print_list(result)
        ipaddr = input(f"Indtast den ip-adresse du ønsker historik for: ")

        rows = fetch_logdata_single(conn,"src_ip", ipaddr)
        if len(rows) > 0:
            show_log_table(rows, f"Oversigt over ip historik for {ipaddr}")
        else:
            print("Intet at vise - Prøv med en anden IP-adresse")
    if choice == "2":
        #Udvalg af data til tabel historik udfra brugernavn
        print(f"Der er følgende bruger i databasen: ")
        #print(fetch_distinct_from_table(conn, "logdata", "user"))

        user = input(f"Indtast den bruger du ønsker historik for: ")

        rows = fetch_logdata_single(conn,"user", user)
        if len(rows) > 0:
            show_log_table(rows, f"Oversigt over bruger historik for {user}")
        else:
            print("Intet at vise - Prøv med et andet brugernavn")

def handle_submenu_3_actions(conn, choice: str):
    if choice == "1":
        #laver udvalg af ip'er
        parameters = fetch_distinct_from_table(conn, "logdata", "src_ip")
        print("\nher er et udvalg de mulige ip'er")
        items = []
        for item in parameters:
            items.append(item[0])
        console_print_list(items)

        ipaddr = input(f"Indtast den ip-adresse du ønsker historik over eventsne: ").strip()

        #laver udvalg af events
        parameters = fetch_distinct_from_table(conn, "logdata", "event")
        print("\nher er et udvalg af de mulige events")
        items = []
        for item in parameters:
            items.append(item[0])
        console_print_list(items)

        events = input(f"hvilke events vil du gerne have historik over ").strip().upper()
        rows = fetch_logdata_double(conn,"src_ip", ipaddr,"event",events)
        if len(rows) > 0:
            show_log_table(rows, f"Oversigt over ip historik for {ipaddr} og forbundet med event {events}")
        else:
            print("Intet at vise - Prøv med en anden IP-adresse eller event")

    if choice == "2":
        #Udvalg af data til tabel historik udfra brugernavn
        user = input(f"Indtast den bruger du ønsker historik for: ")
        rows = fetch_logdata_single(conn,"user", user)
        if len(rows) > 0:
            show_log_table(rows, f"Oversigt over bruger historik for {user}")
        else:
            print("Intet at vise - Prøv med et andet brugernavn")

def handle_submenu_4_actions(conn, choice: str):
    """
    Styrer hvad der sker når der tastes på skærmen/konsollen
    :param conn: database connection
    :param choice: choice
    """
    if choice == "1":
        console.print("\n[bold cyan]dannelse af piechart[/]\n")
        tablename = input("hvilket table vil du have data fra ")
        data = input("hvilken kolonne skal der laves piechart på ")
        if piechart(conn, tablename, data, data):
            console.print("\n[bold cyan]piechart er lavet i plots[/]\n")



    elif choice == "2":
        console.print("\n[bold cyan]dannelse af specefic piechart[/]\n")
        tablename = input("hvilket table vil du have data fra ")
        data = input("indtast den primære kolonne ")
        data2 = input("indtast kolonne dit søgekriterie kan findes i ")
        parameters = fetch_distinct_from_table(conn, tablename, data2)
        print("\nher er et udvalg af dine parameter")
        items = []
        for item in parameters:
            items.append(item[0])
        console_print_list(items)
        searchKriteria = input("indtast dit søgekriterie ")
        if piechartspecefic(conn, tablename, data,f"{data} in {searchKriteria}" ,data2, searchKriteria):
            print("piechart lavet i plots")


    elif choice == "3":
        console.print("\n[bold cyan]danellse af scatterplot[/]\n")
        tendenslinje = input("vil du gerne have en tendenslinje ja/nej").lower().strip(" ")
        if tendenslinje == "ja" or tendenslinje == "nej":
            tabelname = input("Indtast hvilket table du vil have data fra ")
            xdata = input("Indtast hvilken kolonne du gerne vil have ad x aksen ")
            ydata = input("Indtast hvilken kollone du gerne vil hive en data ud fra ")
            parameters = fetch_distinct_from_table(conn, tabelname,ydata)
            print("\nher er et udvalg af dine parameter")
            items = []
            for item in parameters:
                items.append(item[0])
            console_print_list(items)

            parameter = input("indtast dataen du gerne vil se ")
            if tendenslinje == "ja":
                if scatterplotMedTendensLinje(conn,tabelname,xdata,ydata,parameter):
                    print("scatter plot med tendenslinje i plots")
            elif tendenslinje == "nej":
                if scatterplot(conn,tabelname,xdata,ydata,parameter):
                    print("scatter plot lavet i plots")
        else:
            print("det var ikke ja eller nej til tendenslinjer")

    elif choice == "4":
        tabelname = input("Indtast hvilket table du vil have data fra ")
        xdata = input("Indtast hvilken kolonne du gerne vil have ad x aksen ")
        ydata = input("Indtast hvilken kollone du gerne vil hive en data ud fra ")

        parameters = fetch_distinct_from_table(conn, tabelname, ydata)
        print("\nher er et udvalg af dine parameter")
        items = []
        for item in parameters:
            items.append(item[0])
        console_print_list(items)

        parameter = input("indtast dataen du gerne vil se ")
        if barchart(conn, tabelname, xdata, ydata, parameter):
            print("Barchar lavet i plots")

    elif choice == "5":
        tabelname = input("indtast hvilket table du vil have data fra ")
        coulum = input("indtast kolonnen for dataen du gerne vil lave en historik fra ")

        parameters = fetch_distinct_from_table(conn, tabelname, coulum)
        print("\nher er et udvalg af dine parameter")
        items = []
        for item in parameters:
            items.append(item[0])
        console_print_list(items)

        value = input("indtast hvilken data der skal laves historik fra ")
        parameter = input("indtast hvilken kolonne du gerne vil se i sammenhæng med den valgte data ")
        if historyCreater(conn,tabelname,coulum, value, parameter):
            print("historik er lavet i plots")





def run_dynamic_submenu(conn, parent_nr: int, parent_title: str):
    """
    gennerer undermenuen udfra databasen og submenu tabellen - fetch_all_from_db blev skrottet og to dedikerede til menusystenet blev lavet
    :param conn: database connection
    :param parent_nr: parent nr
    :param parent_title: parent title
    """
    border_colors = {1: "bright_green", 2: "bright_yellow", 3: "bright_blue", 4: "bright_magenta"}
    color = border_colors.get(parent_nr, "bright_green")

    while True:
        submenu_items = get_menu_from_db(conn, "submenu", parent_nr=parent_nr)

        if not submenu_items:
            console.print(f"\n[bold yellow]⚠ Ingen undermenupunkter fundet for '{parent_title}' i databasen.[/]")
            if parent_nr in (2, 3):
                rows = fetch_all_from_table(conn, "logdata")
                if rows:
                    show_log_table(rows[:], title=f"Visningstabel: Logdata ({len(rows)} rækker total)")
            input("\nTryk Enter for at vende tilbage...")
            break
        #Titler og undermenuer indsættes i dos box'ens så det står pænt
        draw_dos_box(
            title=f"UNDERMENU: {parent_title.upper()}",
            subtitle=f"Hovedmenu > {parent_title}",
            menu_items=submenu_items,
            border_color=color
        )

        valid_keys = [item[0] for item in submenu_items]
        #default choice i submenu sættes til at gå tilbage til hovedmenu
        choice = ask_menu_choice("Vælg funktion", valid_keys, default_choice="0")

        if choice == "0":
            break

        if parent_nr == 1:
            handle_submenu_1_actions(conn, choice)
        elif parent_nr == 2:
            handle_submenu_2_actions(conn, choice)
        elif parent_nr == 3:
            handle_submenu_3_actions(conn, choice)
        elif parent_nr == 4:
            handle_submenu_4_actions(conn, choice)
        else:
            console.print(f"\n[bold magenta]✔ Valgte punkt [{choice}] under {parent_title}[/]")

        input("\nTryk Enter for at fortsætte...")


def main_menu():
    init_db()
    conn = connect_to_db("bumlebusiness.db")

    if conn is None:
        console.print("[bold red]Kritisk fejl: Kan ikke oprette forbindelse til databasen.[/]")
        return

    while True:
        main_items = get_menu_from_db(conn, "mainmenu")
        valid_keys = [item[0] for item in main_items]

        draw_dos_box(
            title="BUMLE BUSINESS - LOG ANALYSE v1.0",
            subtitle="Hovedmenu",
            menu_items=main_items,
            border_color="bright_cyan"
        )

        choice = ask_menu_choice("Indtast dit valg", valid_keys, default_choice="1")

        if choice == "0":
            clear_screen()
            console.print("[bold red]Programmet er afsluttet.[/]")
            conn.close()
            break

        selected_title = f"Menu {choice}"

        # Vi løber igennem hvert punkt i listen
        for item in main_items:
            key = item[0]  # Første element (f.eks. "1")
            title = item[1]  # Andet element (f.eks. "Logoperationer")
            # Hvis nøglen matcher brugerens valg, gemmer vi titlen og stopper
            if key == choice:
                selected_title = title
                break  # 'break' stopper løkken med det samme, da vi har fundet det, vi søgte
        run_dynamic_submenu(conn, int(choice), selected_title)


if __name__ == "__main__":
    main_menu()
