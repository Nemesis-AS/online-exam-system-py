from rich.console import Console

console = Console()

admins = {
    "nemesis": "password1",
    "kaif": "password2",
    "krish": "password3"
}

users = {
    "dhruv": "password4",
    "adhish": "password5",
    "achyut": "password6"
}

def show_dialog() -> bool:
    uname = console.input("Enter Username: ")
    pwd = console.input("Enter Password: ")

    auth_status, is_admin, output = authenticate(uname.lower(), pwd)
    console.print(output)
    if auth_status:
        if is_admin:
            console.print("Welcome Admin", style="bold blue")
        else:
            console.print("Welcome User", style="bold blue")
        
        return is_admin
    else:
        show_dialog()

# Returns [Authentication state, amdin previliges, output string]
def authenticate(username: str, password: str) -> list:
    if username in users:
        if users[username] == password:
            return True, False, "[green]Login Successfull![/]"
        else:
            return False, False, "[red]Incorrect Password![/]"
    elif username in admins:
        if admins[username] == password:
            return True, True, "[green]Login Successfull![/]"
        else:
            return False, False, "[red]Incorrect Password![/]"
    else:
        return False, False, "[red]Incorrect Username![/]"