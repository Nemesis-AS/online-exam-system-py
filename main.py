from rich.console import Console

import authenticator
import admin
import user

console = Console()

console.rule("[bold green]Fatima School Online Exam System[/]")

is_admin, uname = authenticator.show_dialog()

if is_admin:
    admin.show_admin_menu()
else:
    user.show_user_menu(uname)
