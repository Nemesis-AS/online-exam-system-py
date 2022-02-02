import config
import mysql.connector
from rich.console import Console

db = mysql.connector.connect(
    user="root",
    host="localhost",
    passwd=config.MYSQL_PASSWORD,
    database="Online_Exam_System"
)
cursor = db.cursor()
console = Console()

# Utility Functions


def show_options(options: list) -> int:
    output = ""

    for idx in range(len(options)):
        output += f"{idx+1}.{options[idx]}\n"

    console.rule("[bold green]Select Action[/]")
    console.print(output)
    selected_option = int(console.input(
        f"Select Action[{1} - {len(options)}]: "))

    return selected_option - 1


def get_papers():
    cursor.execute(
        "SELECT * FROM Papers WHERE start < CURRENT_TIMESTAMP AND TIMESTAMPADD(MINUTE, duration, start) > CURRENT_TIMESTAMP")
    return cursor.fetchall()


def get_papers_by_class(user_class: int) -> list:
    cursor.execute(
        f"SELECT * FROM Papers WHERE class = '{user_class}' AND  start < CURRENT_TIMESTAMP AND TIMESTAMPADD(MINUTE, duration, start) > CURRENT_TIMESTAMP"
    )
    return cursor.fetchall()

# Actions


def attempt_ques_paper():
    console.print("Attempting Ques Paper...")


def view_result():
    console.print("Viewing Result...")


def see_prev_papers():
    console.print("Viewing Previous Papers...")


def view_answer_key():
    console.print("Viewing Answer Key...")


def show_user_menu() -> None:
    options = ["Attempt Question Paper", "My Result",
               "See Prev Papers", "View Answer Key"]

    user_choice = show_options(options)

    if user_choice == 0:
        attempt_ques_paper()
    elif user_choice == 1:
        view_result()
    elif user_choice == 2:
        see_prev_papers()
    elif user_choice == 3:
        view_answer_key()
    else:
        console.print("invalid Choice")


print(get_papers())
