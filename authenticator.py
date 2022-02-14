import config
import mysql.connector
from rich.console import Console

db = mysql.connector.connect(
    user="root",
    host="localhost",
    passwd=config.MYSQL_PASSWORD
)
cursor = db.cursor()
console = Console()


def init() -> None:
    cursor.execute(f"USE {config.DB_NAME}")


def show_dialog() -> bool:
    console.print("1. Sign In\n2. Sign Up")
    choice = int(console.input("Enter Choice: "))

    uname = console.input("Enter Username: ")
    pwd = console.input("Enter Password: ")

    if choice == 1:
        auth_status, is_admin, output = authenticate(uname.lower(), pwd)
        console.print(output)
        if auth_status:
            if is_admin:
                console.print("Welcome Admin", style="bold blue")
            else:
                console.print("Welcome User", style="bold blue")

            return is_admin, uname
        else:
            show_dialog()
    else:
        user_class = console.input("Enter Class: ")
        create_new_user(uname, pwd, user_class)
        console.print("Created User Successfully!")
        return False, None


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


def create_new_user(username: str, password: str, user_class: int):
    cursor.execute(
        f"INSERT INTO Users(username, password, class) VALUES('{username}', '{password}', {user_class})")
    db.commit()
