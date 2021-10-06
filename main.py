from rich.console import Console

import authenticator

console = Console()

console.rule("[bold green]Fatima School Online Exam System[/]")

auth_status = authenticator.show_dialog()