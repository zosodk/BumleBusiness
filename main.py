from defDbHandler import connect_to_db, fetch_all_from_table, tabel_cleaner, insert_logdata
from defFileHandler import openLogfile, parse_logline
from defInit import init_db
from defGUI import console, clear_screen, draw_dos_box, ask_menu_choice, show_log_table
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
        if tabel_cleaner(conn, "logdata"):
            conn.commit()
            console.print("\n[bold green]✔ Alt eksisterende logindhold i databasen er nu slettet![/]")

    elif choice == "3":
        count = 0
        with open("cyber_security_log_sample.txt", "r", encoding="utf-8") as fil:
            for linie in fil:
                if linie.strip():
                    parsed = parse_logline(linie)
                    insert_logdata(conn, "logdata", parsed)
                    count += 1
        conn.commit()
        console.print(f"\n[bold green]✔ {count} loglinjer er parset og indsat i SQLite-databasen![/]")

def handle_submenu_4_actions(conn, choice: str):
    """
    Styrer hvad der sker når der tastes på skærmen/konsollen
    :param conn: database connection
    :param choice: choice
    """
    if choice == "1":
        console.print("\n[bold cyan]Der skal vælges data til indsættelse i piechartet[/]\n")
        data = input("hvilken data skal der laves piechart på")


    elif choice == "2":
        if tabel_cleaner(conn, "logdata"):
            conn.commit()
            console.print("\n[bold green]✔ Alt eksisterende logindhold i databasen er nu slettet![/]")

    elif choice == "3":
        count = 0
        with open("cyber_security_log_sample.txt", "r", encoding="utf-8") as fil:
            for linie in fil:
                if linie.strip():
                    parsed = parse_logline(linie)
                    insert_logdata(conn, "logdata", parsed)
                    count += 1
        conn.commit()
        console.print(f"\n[bold green]✔ {count} loglinjer er parset og indsat i SQLite-databasen![/]")

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
        #default choice i submenu sættes til at gå til bage til hovedmenu
        choice = ask_menu_choice("Vælg funktion", valid_keys, default_choice="0")

        if choice == "0":
            break

        if parent_nr == 1:
            handle_submenu_1_actions(conn, choice)
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