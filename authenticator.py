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

def show_dialog():
    uname = console.input("Enter Username: ")
    pwd = console.input("Enter Password: ")

    auth_status = authenticate(uname, pwd)
    console.print(auth_status[2])
    if auth_status[0]:
        if auth_status[1]:
            console.print("Welcome Admin", style="bold blue")
        else:
            console.print("Welcome User", style="bold blue")
    else:
        # Try Again
        pass

# Returns [Authentication state, amdin previliges, output string]
def authenticate(username, password):
    if username in users:
        if users[username] == password:
            return [True, False, "[green]Login Successfull![/]"]
        else:
            return [False, False, "[red]Incorrect Password![/]"]
    elif username in admins:
        if admins[username] == password:
            return [True, True, "[green]Login Successfull![/]"]
        else:
            return [False, False, "[red]Incorrect Password![/]"]
    else:
        return [False, False, "[red]Incorrect Username![/]"]