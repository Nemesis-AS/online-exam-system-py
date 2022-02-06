import config
import mysql.connector
from rich.console import Console
from rich.table import Table
from rich import box

db = mysql.connector.connect(
    user="root",
    host="localhost",
    passwd=config.MYSQL_PASSWORD,
    database="Online_Exam_System"
)
cursor = db.cursor()
console = Console()

user_info = ()  # ('dhruv', 'password4', 0, 12)

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


def get_papers() -> list:
    cursor.execute(
        "SELECT * FROM Papers WHERE start < CURRENT_TIMESTAMP AND TIMESTAMPADD(MINUTE, duration, start) > CURRENT_TIMESTAMP")
    return cursor.fetchall()


def get_papers_by_class(user_class: int) -> list:
    cursor.execute(
        f"SELECT * FROM Papers WHERE class = '{user_class}'"
    )  # AND start < CURRENT_TIMESTAMP AND TIMESTAMPADD(MINUTE, duration, start) > CURRENT_TIMESTAMP
    return cursor.fetchall()


def get_prev_papers() -> list:
    cursor.execute(
        f"SELECT * FROM Papers WHERE TIMESTAMPADD(MINUTE, duration, start) < CURRENT_TIMESTAMP AND class = {user_info[3]}")
    return cursor.fetchall()


def get_user_info(uname: str):
    cursor.execute(f"SELECT * FROM Users WHERE username = '{uname}'")
    return cursor.fetchone()


def get_ques_by_paper(paper_id: int):
    cursor.execute(
        f"SELECT * FROM Questions WHERE ques_paper_id = {paper_id} ORDER BY ques_order")
    return cursor.fetchall()


def submit_answers(paper_id, ans: list, marks: int) -> None:
    cursor.execute(
        f"INSERT INTO Results(paper_id, user_id, marks, answers) VALUES({paper_id}, '{user_info[0]}', {marks}, '{''.join(ans)}')")
    db.commit()


def get_results() -> list:
    cursor.execute(f"SELECT * FROM Results WHERE user_id = '{user_info[0]}'")
    return cursor.fetchall()

# Actions


def attempt_ques_paper():  # Done
    papers = get_papers_by_class(user_info[3])

    table = Table(title="[blue bold]Papers[/]", box=box.HORIZONTALS)

    table.add_column("Paper ID", justify="right", style="white")
    table.add_column("Title", style="magenta")
    table.add_column("Subject", style="magenta")
    table.add_column("Max Marks", justify="right", style="green")
    table.add_column("No. of Questions", justify="right", style="green")
    table.add_column("Start Time", justify="right", style="green")
    table.add_column("Duration", justify="right", style="green")
    table.add_column("Class", justify="right", style="green")
    for paper in papers:
        table.add_row(str(paper[0]), paper[1], paper[2], str(paper[3]),
                      str(paper[4]), str(paper[5].strftime("%b %d, %Y %I:%M %p")), str(paper[6]), str(paper[7]))
    console.print(table)

    paper_id = int(console.input("Enter Choice: "))

    questions = get_ques_by_paper(paper_id)
    answers = []
    marks = 0
    for ques in questions:
        console.print(f"Q: [bold]{ques[1]}[/]")
        console.print(f"[yellow]A: {ques[2]}[/]")
        console.print(f"[yellow]B: {ques[3]}[/]")
        console.print(f"[yellow]C: {ques[4]}[/]")
        console.print(f"[yellow]D: {ques[5]}[/]")
        ans = console.input("Enter Answer[A, B, C, D]: ")
        answers.append(ans)

        if ans.lower() == ques[6].lower():
            marks += 1

    submit_answers(paper_id, answers, marks)
    console.print("[green]Question Paper Submitted Successfully![/]")


def view_result():  # Done
    res = get_results()

    table = Table(title="[bold blue]Results[/]", box=box.HORIZONTALS)
    table.add_column("Sr. No.", justify="right", style="white")
    table.add_column("Paper ID", justify="right", style="cyan")
    table.add_column("Username", style="magenta")
    table.add_column("Marks", justify="right", style="green")

    for idx in range(len(res)):
        table.add_row(str(idx+1) + ".", str(res[idx][1]),
                      res[idx][2], str(res[idx][3]))
    console.print(table)


# view_result()


def see_prev_papers():  # Partially Done
    papers = get_prev_papers()
    table = Table(title="[blue bold]Previous Papers[/]", box=box.HORIZONTALS)

    table.add_column("Paper ID", justify="right", style="white")
    table.add_column("Title", style="magenta")
    table.add_column("Subject", style="magenta")
    table.add_column("Max Marks", justify="right", style="green")
    table.add_column("No. of Questions", justify="right", style="green")
    table.add_column("Start Time", justify="right", style="green")
    table.add_column("Duration", justify="right", style="green")
    table.add_column("Class", justify="right", style="green")
    for paper in papers:
        table.add_row(str(paper[0]), paper[1], paper[2], str(paper[3]),
                      str(paper[4]), str(paper[5].strftime("%b %d, %Y %I:%M %p")), str(paper[6]), str(paper[7]))
    console.print(table)


# see_prev_papers()


def submit_complaint():  # Partially Done
    body = console.input("Enter Complaint: ")
    body = body.replace("'", "\\'")
    cursor.execute(f"INSERT INTO Complaints(body) VALUES('{body}')")
    db.commit()
    console.print("[green]Submitted Complaint Successfully![/]")


# submit_complaint()


def show_user_menu(uname: str) -> None:
    global user_info
    user_info = get_user_info(uname)
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
        submit_complaint()
    else:
        console.print("invalid Choice")


# print(get_papers())
