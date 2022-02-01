from rich.console import Console

import authenticator, admin, user

console = Console()

console.rule("[bold green]Fatima School Online Exam System[/]")

is_admin = authenticator.show_dialog()

if is_admin:
    admin.show_admin_menu()
else:
    user.show_user_menu()
