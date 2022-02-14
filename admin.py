import datetime
import config
import mysql.connector
from rich.console import Console
from rich.table import Table
from rich import box

db = mysql.connector.connect(
    user="root",
    host="localhost",
    passwd=config.MYSQL_PASSWORD
)
cursor = db.cursor(buffered=True)
console = Console()

# Utility Functions


def init() -> None:
    cursor.execute(f"USE {config.DB_NAME}")


def add_paper_to_db(title, subject, max_marks, noq, start, duration, class_no):
    cursor.execute(
        f"INSERT INTO Papers(title, subject, max_marks, noq, start, duration, class) VALUES('{title}', '{subject}', {max_marks}, {noq}, '{start}', {duration}, {class_no})"
    )
    db.commit()


def get_papers_from_db():
    cursor.execute("SELECT * FROM Papers")
    return cursor.fetchall()


def get_paper_by_id(paper_id: int):
    cursor.execute(f"SELECT * FROM Papers WHERE id = {paper_id}")
    return cursor.fetchone()


def get_ques_by_paper(paper_id: int):
    cursor.execute(
        f"SELECT * FROM Questions WHERE ques_paper_id = {paper_id} ORDER BY ques_order")
    return cursor.fetchall()


def get_latest_paper_id():
    cursor.execute("SELECT id FROM Papers ORDER BY id DESC")
    return cursor.fetchone()[0]


def get_results():
    cursor.execute("SELECT * FROM Results")
    return cursor.fetchall()


def show_options(options: list) -> int:
    output = ""

    for idx in range(len(options)):
        output += f"{idx+1}.{options[idx]}\n"

    console.rule("[bold green]Select Action[/]")
    console.print(output)
    selected_option = int(console.input(
        f"Select Action[{1} - {len(options)}]: "))

    return selected_option - 1

# Actions


def add_ques_paper():
    console.rule("[bold green]Create Question Paper[/]")
    title = console.input("Enter Paper Title: ")
    sub_id = console.input("Enter subject: ")
    max_marks = int(console.input("Enter Max. Marks: "))
    tot_ques = int(console.input("Enter No. of questions: "))
    start = console.input("Enter Start Time (YYYY-MM-DD HH:MM:SS): ")
    duration = console.input("Enter Paper Duration (minutes): ")
    class_no = int(console.input("Enter Class: "))

    add_paper_to_db(title, sub_id, max_marks, tot_ques,
                    start, duration, class_no)

    paper_id = get_latest_paper_id()
    questions = []  # (id, question, a, b, c, d, correct, order, paper_id)

    for idx in range(tot_ques):
        ques_text = console.input("Enter Question: ")
        opt_a = console.input("Enter Option A: ")
        opt_b = console.input("Enter Option B: ")
        opt_c = console.input("Enter Option C: ")
        opt_d = console.input("Enter Option D: ")
        answer = console.input("Enter Correct Option: ")
        questions.append((ques_text, opt_a, opt_b, opt_c, opt_d, answer, idx))

    for ques in questions:
        cursor.execute(
            f"INSERT INTO Questions(ques_text, opt_a, opt_b, opt_c, opt_d, answer, ques_order, ques_paper_id) VALUES('{ques[0]}', '{ques[1]}', '{ques[2]}', '{ques[3]}', '{ques[4]}', '{ques[5]}', {ques[6]}, {paper_id})")
        db.commit()

    console.print("[green]Added Paper Successfully![/]")

    # https://youtube.com/playlist?list=PLTuJWtGVCB8HzEXPc3AKH37_-PXOkhKDH


def edit_ques_paper():
    papers = get_papers_from_db()
    table = Table(title="[blue bold]Papers[/]", box=box.HORIZONTALS)

    table.add_column("Sr. No.", justify="right", style="white")
    table.add_column("Title", style="magenta")
    table.add_column("Subject", style="magenta")
    table.add_column("Max Marks", justify="right", style="green")
    table.add_column("No. of Questions", justify="right", style="green")
    table.add_column("Start Time", justify="right", style="green")
    table.add_column("Duration", justify="right", style="green")
    table.add_column("Class", justify="right", style="green")

    for idx in range(len(papers)):
        paper = papers[idx]
        table.add_row(str(idx+1), paper[1], paper[2], str(paper[3]),
                      str(paper[4]), str(paper[5].strftime("%b %d, %Y %I:%M %p")), str(paper[6]), str(paper[7]))
        # console.print(
        #     f"{idx+1}. {paper[1]}, {paper[2]}, {paper[3]},{paper[4]}, {paper[5]}, {paper[6]}, {paper[7]}")
    console.print(table)
    paper_choice = int(console.input("Enter Paper ID to select: "))
    if paper_choice >= len(papers):
        console.print("[red]Invalid Choice![/]")
        return
    paper_id = papers[paper_choice - 1][0]
    selected_paper = get_paper_by_id(paper_id)
    if not selected_paper:
        console.print("[red]Paper Not Found![/]")
        return

    props = ["title", "subject", "max_marks",
             "noq", "start", "duration", "class"]
    console.print("Select Property to Edit: ")
    for idx in range(len(props)):
        console.print(f"{idx+1}. {props[idx]}")
    choice = int(console.input("Enter Choice: "))

    console.print(f"Current Value: {selected_paper[choice]}")
    new_val = console.input("Enter New Value: ")

    if choice in [1, 2, 5]:
        # Text Input
        cursor.execute(
            f"UPDATE Papers SET {props[choice - 1]} = '{new_val}' WHERE id = {selected_paper[0]}")
    else:
        # Number Input
        cursor.execute(
            f"UPDATE Papers SET {props[choice - 1]} = {new_val} WHERE id = {selected_paper[0]}")

    db.commit()
    console.print("[bold green]Edited Paper Successfully![/]")


def view_results():
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


def resolve_complaints():  # Done
    cursor.execute("SELECT * FROM Complaints")
    complaints = cursor.fetchall()

    for idx in range(len(complaints)):
        complaint = complaints[idx]
        console.print(
            f"{idx + 1}. {'Resolved' if complaint[2] else 'Unresolved'} --- {complaint[1]}"
        )
    complaint_idx = int(console.input("Enter Complaint ID to resolve: "))
    curr_complaint = complaints[complaint_idx - 1]

    console.print(
        f"Status: {'Resolved' if complaint[2] else 'Unresolved'}")
    console.print(f"Complaint: {curr_complaint[1]}")
    res = console.input("Enter Reponse: ")
    res = res.replace("'", "\\'")

    cursor.execute(
        f"UPDATE Complaints SET resolved=True, response='{res}' WHERE id = {curr_complaint[0]}")
    db.commit()
    console.print("[green bold]Resolved Complaint Successfully![/]")


def show_admin_menu() -> None:  # Start
    options = ["Add Question Paper", "Edit Existing Paper",
               "View Results", "Resolve Complaints"]

    user_choice = show_options(options)

    if user_choice == 0:
        add_ques_paper()
    elif user_choice == 1:
        edit_ques_paper()
    elif user_choice == 2:
        view_results()
    elif user_choice == 3:
        resolve_complaints()
    else:
        console.print("invalid Choice")
