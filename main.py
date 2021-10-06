from rich.console import Console

import authenticator

console = Console()

console.rule("[bold green]Fatima School Online Exam System[/]")

def authentication_dialog():
    uname = console.input("Enter Username: ")
    pwd = console.input("Enter Password: ")

    auth_status = authenticator.authenticate(uname, pwd)
    console.print(auth_status[2])
    if auth_status[0]:
        if auth_status[1]:
            console.print("Welcome Admin", style="bold blue")
        else:
            console.print("Welcome User", style="bold blue")
    else:
        # Try Again
        pass