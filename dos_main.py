#from file_handler import read_raw_logs_to_memory, parse_log_lines
#from db_handler import initialize_database, insert_logs_to_db
from table_view import draw_dos_box, table_submenu, chart_submenu, console
from rich.prompt import Prompt

LOG_FILE = "cyber_security_log_sample.txt"
DB_FILE = "vpn_logs.db"


def main():
    main_menu_items = [
        ("1", "Indlæs rå VPN-logfil til memory & gem i SQLite"),
        ("2", "Tabelvisning & Filtrering (Åbner undermenu »)"),
        ("3", "Analyse & Diagrammer (Åbner undermenu »)"),
        ("0", "Afslut programmet")
    ]

    while True:
        draw_dos_box(
            title="BUMLE BUSINESS - VPN LOG ANALYZER v1.0",
            subtitle="Hovedmenu",
            menu_items=main_menu_items,
            border_color="bright_cyan"
        )

        choice = Prompt.ask(
            "\n[bold yellow]Indtast dit valg[/]",
            choices=["1", "2", "3", "0"],
            default="1"
        )

        if choice == "1":
            raw_logs = read_raw_logs_to_memory(LOG_FILE)
            if raw_logs:
                parsed_logs = parse_log_lines(raw_logs)
                if initialize_database(DB_FILE):
                    insert_logs_to_db(parsed_logs, DB_FILE)
            input("\nTryk Enter for at fortsætte...")

        elif choice == "2":
            table_submenu(DB_FILE)  # Hopper ind i tabel-undermenuen

        elif choice == "3":
            chart_submenu(DB_FILE)  # Hopper ind i graf-undermenuen

        elif choice == "0":
            console.print("\n[bold red]Lukker programmet...[/]")
            break


if __name__ == "__main__":
    main()