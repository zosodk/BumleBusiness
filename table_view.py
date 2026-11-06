import os
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich import box

# Importer jeres database-funktioner
from db_handler import get_all_logs, get_logs_by_column

console = Console()


def clear_screen():
    """Rydder terminalen på tværs af styresystemer."""
    os.system("cls" if os.name == "nt" else "clear")


def draw_dos_box(title: str, subtitle: str, menu_items: list[tuple[str, str]], border_color: str = "bright_cyan"):
    """
    Genbrugelig funktion: Tegner en DOS-menu ud fra en titel og en liste af (tast, beskrivelse).
    Bruges til både hovedmenuen og alle undermenuer!
    """
    clear_screen()

    menu_table = Table(show_header=False, box=None, padding=(0, 2))
    menu_table.add_column("Tast", style="bold yellow", justify="right")
    menu_table.add_column("Handling", style="bold white")

    for key, description in menu_items:
        menu_table.add_row(f"[{key}]", description)

    panel = Panel(
        menu_table,
        title=f"[bold white on blue] {title} [/]",
        subtitle=f"[dim]{subtitle}[/]",
        box=box.DOUBLE,
        border_style=border_color,
        padding=(1, 4),
        expand=False
    )
    console.print(panel)


def print_logs_as_rich_table(rows: list, table_title: str = "VPN Server Logs"):
    """Udskriver rækker fra SQLite i en formateret og farvekodet tabel."""
    if not rows:
        console.print("\n[bold red]⚠ Ingen logdata fundet (har du husket at indlæse logfilen først?).[/]")
        return

    table = Table(title=f"{table_title} ({len(rows)} rækker)", box=box.DOUBLE_EDGE, header_style="bold cyan")
    table.add_column("ID", style="dim", justify="right")
    table.add_column("Tidspunkt", style="dim")
    table.add_column("Level")
    table.add_column("Event", style="bold")
    table.add_column("Bruger", style="green")
    table.add_column("Kilde-IP", style="yellow")
    table.add_column("Dest. Host:Port")
    table.add_column("Status")

    for row in rows:
        level_color = {"INFO": "green", "WARN": "yellow", "ALERT": "bold red"}.get(row["level"], "white")
        status_color = "bold red" if row["status"] in ("FAILED", "BLOCKED") else "green"

        table.add_row(
            str(row["id"]),
            row["timestamp"],
            f"[{level_color}]{row['level']}[/]",
            row["event"],
            row["user"],
            row["src_ip"],
            f"{row['deimport os
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich import box

# Importer jeres database-funktioner
from db_handler import get_all_logs, get_logs_by_column

console = Console()


def clear_screen():
    """Rydder terminalen på tværs af styresystemer."""
    os.system("cls" if os.name == "nt" else "clear")


def draw_dos_box(title: str, subtitle: str, menu_items: list[tuple[str, str]], border_color: str = "bright_cyan"):
    """
    Genbrugelig funktion: Tegner en DOS-menu ud fra en titel og en liste af (tast, beskrivelse).
    Bruges til både hovedmenuen og alle undermenuer!
    """
    clear_screen()

    menu_table = Table(show_header=False, box=None, padding=(0, 2))
    menu_table.add_column("Tast", style="bold yellow", justify="right")
    menu_table.add_column("Handling", style="bold white")

    for key, description in menu_items:
        menu_table.add_row(f"[{key}]", description)

    panel = Panel(
        menu_table,
        title=f"[bold white on blue] {title} [/]",
        subtitle=f"[dim]{subtitle}[/]",
        box=box.DOUBLE,
        border_style=border_color,
        padding=(1, 4),
        expand=False
    )
    console.print(panel)


def print_logs_as_rich_table(rows: list, table_title: str = "VPN Server Logs"):
    """Udskriver rækker fra SQLite i en formateret og farvekodet tabel."""
    if not rows:
        console.print("\n[bold red]⚠ Ingen logdata fundet (har du husket at indlæse logfilen først?).[/]")
        return

    table = Table(title=f"{table_title} ({len(rows)} rækker)", box=box.DOUBLE_EDGE, header_style="bold cyan")
    table.add_column("ID", style="dim", justify="right")
    table.add_column("Tidspunkt", style="dim")
    table.add_column("Level")
    table.add_column("Event", style="bold")
    table.add_column("Bruger", style="green")
    table.add_column("Kilde-IP", style="yellow")
    table.add_column("Dest. Host:Port")
    table.add_column("Status")

    for row in rows:
        level_color = {"INFO": "green", "WARN": "yellow", "ALERT": "bold red"}.get(row["level"], "white")
        status_color = "bold red" if row["status"] in ("FAILED", "BLOCKED") else "green"

        table.add_row(
            str(row["id"]),
            row["timestamp"],
            f"[{level_color}]{row['level']}[/]",
            row["event"],
            row["user"],
            row["src_ip"],
            f"{row['dest_host']}:{row['dest_port']}",
            f"[{status_color}]{row['status']}[/]"
        )

    console.print()
    console.print(table)


# ==========================================
# UNDERMENU 1: TABELVISNING & FILTRERING
# ==========================================
def table_submenu(db_path: str = "vpn_logs.db"):
    """Undermenu til at vælge, hvordan logtabellen skal filtreres."""
    submenu_items = [
        ("1", "Vis ALLE logdata (296 rækker)"),
        ("2", "Vis kun kritiske alarmer (level = ALERT)"),
        ("3", "Vis kun advarsler (level = WARN)"),
        ("4", "Filtrér på en specifik Kilde-IP (f.eks. 203.0.113.250)"),
        ("5", "Filtrér på et specifikt Brugernavn (f.eks. svc_backup)"),
        ("0", "« Tilbage til Hovedmenuen")
    ]

    while True:
        draw_dos_box(
            title="UNDERMENU: TABELVISNING & FILTRERING",
            subtitle="Hovedmenu > Tabelvisning",
            menu_items=submenu_items,
            border_color="bright_green"  # Skifter rammen til grøn, så man tydeligt kan se, man er i en undermenu
        )

        choice = Prompt.ask(
            "\n[bold yellow]Vælg visning[/]",
            choices=["1", "2", "3", "4", "5", "0"],
            default="1"
        )

        if choice == "0":
            break  # Bryder ud af undermenuens while-loop og hopper tilbage til hovedmenuen!

        elif choice == "1":
            rows = get_all_logs(db_path=db_path)
            print_logs_as_rich_table(rows, "Alle VPN-logdata")

        elif choice == "2":
            rows = get_logs_by_column("level", "ALERT", db_path=db_path)
            print_logs_as_rich_table(rows, "Kritiske hændelser (level=ALERT)")

        elif choice == "3":
            rows = get_logs_by_column("level", "WARN", db_path=db_path)
            print_logs_as_rich_table(rows, "Advarsler (level=WARN)")

        elif choice == "4":
            ip_input = Prompt.ask("[bold cyan]Indtast Kilde-IP[/]", default="203.0.113.250")
            rows = get_logs_by_column("src_ip", ip_input.strip(), db_path=db_path)
            print_logs_as_rich_table(rows, f"Logs for Kilde-IP: {ip_input}")

        elif choice == "5":
            user_input = Prompt.ask("[bold cyan]Indtast Brugernavn[/]", default="svc_backup")
            rows = get_logs_by_column("user", user_input.strip(), db_path=db_path)
            print_logs_as_rich_table(rows, f"Logs for bruger: {user_input}")

        input("\nTryk Enter for at vende tilbage til undermenuen...")


# ==========================================
# UNDERMENU 2: DIAGRAMMER & VISUALISERING
# ==========================================
def chart_submenu(db_path: str = "vpn_logs.db"):
    """Undermenu til valg af scatter-plots og overbliksdiagrammer."""
    submenu_items = [
        ("1", "Scatter-plot: Tidspunkt vs. Kilde-IP (Find angrebsmønstre)"),
        ("2", "Scatter-plot: Event-type vs. Destinationsport"),
        ("3", "Præsentationsdiagram: Brute-Force & Malware angrebet d. 2. marts"),
        ("4", "Overbliksdiagram: Fordeling af hændelsestyper (Søjlediagram)"),
        ("5", "Overbliksdiagram: Fordeling af Status OK / FAILED / BLOCKED"),
        ("0", "« Tilbage til Hovedmenuen")
    ]

    while True:
        draw_dos_box(
            title="UNDERMENU: ANALYSE & VISUALISERING",
            subtitle="Hovedmenu > Visualisering",
            menu_items=submenu_items,
            border_color="bright_magenta"  # Lilla ramme for visualiseringsmenuen
        )

        choice = Prompt.ask(
            "\n[bold yellow]Vælg diagram[/]",
            choices=["1", "2", "3", "4", "5", "0"],
            default="1"
        )

        if choice == "0":
            break

        # Her kalder I jeres plot-funktioner fra visualizer.py
        console.print(f"\n[bold magenta]Genererer diagram #{choice}... (Luk graf-vinduet for at fortsætte)[/]")
        input("\nTryk Enter for at vende tilbage til undermenuen...")st_host']}:{row['dest_port']}",
            f"[{status_color}]{row['status']}[/]"
        )

    console.print()
    console.print(table)


# ==========================================
# UNDERMENU 1: TABELVISNING & FILTRERING
# ==========================================
def table_submenu(db_path: str = "vpn_logs.db