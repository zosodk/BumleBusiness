import os
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich import box

console = Console()

# ==========================================
# DUMMY DATA (Kun til mock-up fremvisning)
# ==========================================
MOCK_LOGS = [
    {"id": 1, "time": "08:01:17", "level": "INFO", "event": "LOGIN_SUCCESS", "user": "eve", "ip": "10.0.0.5", "dest": "db01:53", "status": "OK"},
    {"id": 2, "time": "08:15:31", "level": "ALERT", "event": "PORT_SCAN_DETECTED", "user": "admin", "ip": "203.0.113.7", "dest": "mail01:3389", "status": "BLOCKED"},
    {"id": 3, "time": "08:01:12", "level": "WARN", "event": "LOGIN_FAILED", "user": "alice", "ip": "203.0.113.250", "dest": "vpn01:443", "status": "FAILED"},
    {"id": 4, "time": "08:05:11", "level": "ALERT", "event": "MALWARE_MATCH", "user": "svc_backup", "ip": "198.51.100.200", "dest": "web01:445", "status": "BLOCKED"},
]


def clear_screen():
    """Rydder terminalen."""
    os.system("cls" if os.name == "nt" else "clear")


def draw_dos_box(title: str, subtitle: str, menu_items: list[tuple[str, str]], border_color: str = "bright_cyan"):
    """Genbrugelig funktion der tegner selve DOS-rammen til både hoved- og undermenuer."""
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


def show_mock_table(filter_level: str | None = None):
    """Viser en mock-up tabel med farvekodede rækker."""
    table = Table(title="MOCK-UP: VPN Server Logs", box=box.DOUBLE_EDGE, header_style="bold cyan")
    table.add_column("ID", style="dim", justify="right")
    table.add_column("Tid")
    table.add_column("Level")
    table.add_column("Event", style="bold")
    table.add_column("Bruger", style="green")
    table.add_column("Kilde-IP", style="yellow")
    table.add_column("Dest")
    table.add_column("Status")

    for row in MOCK_LOGS:
        if filter_level and row["level"] != filter_level:
            continue

        lvl_color = {"INFO": "green", "WARN": "yellow", "ALERT": "bold red"}.get(row["level"], "white")
        stat_color = "bold red" if row["status"] in ("FAILED", "BLOCKED") else "green"

        table.add_row(
            str(row["id"]),
            row["time"],
            f"[{lvl_color}]{row['level']}[/]",
            row["event"],
            row["user"],
            row["ip"],
            row["dest"],
            f"[{stat_color}]{row['status']}[/]"
        )

    console.print()
    console.print(table)


# ==========================================
# UNDERMENU 1: TABELVISNING
# ==========================================
def table_submenu():
    submenu_items = [
        ("1", "Vis ALLE logdata (Mock-up tabel)"),
        ("2", "Vis kun kritiske alarmer (level = ALERT)"),
        ("3", "Søg på specifik Kilde-IP (Mock-up)"),
        ("0", "« Tilbage til Hovedmenuen")
    ]

    while True:
        draw_dos_box(
            title="UNDERMENU: TABELVISNING",
            subtitle="Hovedmenu > Tabelvisning",
            menu_items=submenu_items,
            border_color="bright_green"  # Grøn ramme i tabel-undermenuen
        )

        choice = Prompt.ask("\n[bold yellow]Vælg visning[/]", choices=["1", "2", "3", "0"], default="1")

        if choice == "0":
            break  # Hopper ud af undermenuens while-loop og tilbage til hovedmenuen
        elif choice == "1":
            show_mock_table()
        elif choice == "2":
            show_mock_table(filter_level="ALERT")
        elif choice == "3":
            ip = Prompt.ask("[bold cyan]Indtast IP at søge efter[/]", default="203.0.113.250")
            console.print(f"\n[bold green]✔ (Mock-up) Viser resultater for IP: {ip}[/]")

        input("\nTryk Enter for at vende tilbage til undermenuen...")


# ==========================================
# UNDERMENU 2: DIAGRAMMER & ANALYSE
# ==========================================
def chart_submenu():
    submenu_items = [
        ("1", "Scatter-plot: Tidspunkt vs. Kilde-IP"),
        ("2", "Scatter-plot: Event vs. Port"),
        ("3", "Overbliksdiagram: Hændelsestyper (Søjlediagram)"),
        ("0", "« Tilbage til Hovedmenuen")
    ]

    while True:
        draw_dos_box(
            title="UNDERMENU: ANALYSE & DIAGRAMMER",
            subtitle="Hovedmenu > Diagrammer",
            menu_items=submenu_items,
            border_color="bright_magenta"  # Lilla ramme i graf-undermenuen
        )

        choice = Prompt.ask("\n[bold yellow]Vælg diagram[/]", choices=["1", "2", "3", "0"], default="1")

        if choice == "0":
            break

        console.print(f"\n[bold magenta]📈 (Mock-up) Her åbner Matplotlib-vinduet for graf #{choice}...[/]")
        input("\nTryk Enter for at vende tilbage til undermenuen...")


# ==========================================
# HOVEDMENU
# ==========================================
def main_menu():
    main_items = [
        ("1", "Indlæs logfil til memory & SQLite (Mock-up)"),
        ("2", "Tabelvisning & Filtrering (Åbner undermenu »)"),
        ("3", "Analyse & Diagrammer (Åbner undermenu »)"),
        ("0", "Afslut programmet")
    ]

    while True:
        draw_dos_box(
            title="BUMLE BUSINESS - VPN LOG ANALYZER v1.0",
            subtitle="Hovedmenu",
            menu_items=main_items,
            border_color="bright_cyan"  # Cyan ramme i hovedmenuen
        )

        choice = Prompt.ask("\n[bold yellow]Indtast dit valg[/]", choices=["1", "2", "3", "0"], default="1")

        if choice == "1":
            console.print("\n[bold green]✔ (Mock-up) 296 loglinjer indlæst i memory og gemt i SQLite![/]")
            input("\nTryk Enter for at fortsætte...")
        elif choice == "2":
            table_submenu()  # Kalder undermenu 1
        elif choice == "3":
            chart_submenu()  # Kalder undermenu 2
        elif choice == "0":
            clear_screen()
            console.print("[bold red]Programmet er afsluttet.[/]")
            break


if __name__ == "__main__":
    main_menu()