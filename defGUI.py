import os
os.environ.setdefault("TERM", "xterm-256color")
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich import box

console = Console(force_terminal=True, color_system="truecolor", width=180)


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def draw_dos_box(title: str, subtitle: str, menu_items: list[tuple[str, str, str]], border_color: str = "bright_cyan"):
    """Tegner DOS-rammen ud fra (nr_str, menuitem, description)."""
    clear_screen()

    menu_table = Table(show_header=False, box=None, padding=(0, 2))
    menu_table.add_column("Tast", style="bold yellow", justify="right")
    menu_table.add_column("Handling", style="bold white")
    menu_table.add_column("Beskrivelse", style="dim white")

    for nr_str, menuitem, description in menu_items:
        menu_table.add_row(f"[{nr_str}]", menuitem, description)

    panel = Panel(
        menu_table,
        title=f"[bold black on white] {title} [/]",
        subtitle=f"[dim]{subtitle}[/]",
        box=box.DOUBLE,
        border_style=border_color,
        padding=(1, 4),
        expand=True
    )
    console.print(panel)


def ask_menu_choice(prompt_text: str, valid_choices: list[str], default_choice: str = "0") -> str:
    default_val = default_choice if default_choice in valid_choices else valid_choices[0]
    return Prompt.ask(
        f"\n[bold yellow]{prompt_text}[/]",
        console=console,
        choices=valid_choices,
        default=default_val
    )


def show_log_table(db_rows: list[tuple], title: str = "Cyber security Logs (SQLite)"):
    table = Table(title=title, box=box.DOUBLE_EDGE, header_style="bold cyan", width=180)
    table.add_column("ID", style="dim", justify="right")
    table.add_column("Timestamp")
    table.add_column("Level")
    table.add_column("Event", style="bold")
    table.add_column("Bruger", style="green")
    table.add_column("Kilde-IP", style="yellow")
    table.add_column("Destination")
    table.add_column("Status")
    table.add_column("Besked", style="dim")

    for row in db_rows:
        nr, ts, level, event, user, src_ip, dest_host, dest_port, status, msg = row

        lvl_color = {"INFO": "green", "WARN": "yellow", "ALERT": "bold red"}.get(level, "white")
        stat_color = "bold red" if status in ("FAILED", "BLOCKED") else "green"

        table.add_row(
            str(nr),
            ts,
            f"[{lvl_color}]{level}[/]",
            event,
            user,
            src_ip,
            f"{dest_host}:{dest_port}",
            f"[{stat_color}]{status}[/]",
            msg
        )

    console.print()
    console.print(table)