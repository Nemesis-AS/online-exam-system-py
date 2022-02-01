import config

from rich.console import Console
import mysql.connector

db = mysql.connector.connect(
    user="root",
    host="localhost",
    passwd=config.MYSQL_PASSWORD,
    database="Online_Exam_System"
)
cursor = db.cursor()
console = Console()


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
    user_data = get_user_data(username)

    if user_data:
        if password == user_data[1]:
            return True, bool(user_data[2]), "[green]Login Successfull![/]"
        else:
            return False, False, "[red]Incorrect Password![/]"
    else:
        return False, False, "[red]Incorrect Username![/]"


def get_user_data(username: str):  # item = (username, password, admin)
    cursor.execute(f"SELECT * FROM Users WHERE username='{username}'")
    for item in cursor:
        return item
    return None
