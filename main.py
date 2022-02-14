import config
from rich.console import Console

import authenticator
import admin
import user
import init

console = Console()

init.init_db(config.DB_NAME)
authenticator.init()
user.init()
admin.init()

console.rule("[bold green]Fatima School Online Exam System[/]")

is_admin, uname = authenticator.show_dialog()

if is_admin:
    admin.show_admin_menu()
else:
    user.show_user_menu(uname)
