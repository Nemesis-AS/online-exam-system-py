import time

# DEBUG
import json
# =======

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


def add_paper_to_db(title, subject, max_marks, noq, start, duration, class_no):
    cursor.execute(
        f"INSERT INTO Papers(title, subject, max_marks, noq, start, duration, class) VALUES('{title}', '{subject}', {max_marks}, {noq}, '{start}', {duration}, {class_no})"
    )
    db.commit()
    console.print("[green]Added Paper Successfully![/]")


def get_papers_from_db():
    cursor.execute("SELECT * FROM Papers")
    return cursor.fetchall()


def get_paper_by_id(paper_id: int):
    cursor.execute(f"SELECT * FROM Papers WHERE id = {paper_id}")
    return cursor.fetchone()


def show_options(options: list) -> int:
    output = ""

    for idx in range(len(options)):
        output += f"{idx+1}.{options[idx]}\n"

    console.rule("[bold green]Select Action[/]")
    console.print(output)
    selected_option = int(console.input(
        f"Select Action[{1} - {len(options)}]: "))

    return selected_option - 1


def save_to_file(data: str) -> None:
    file = open("Output.txt", "a")
    file.write(json.dumps(data))
    file.close()


def read_from_file() -> str:
    file = open("Output.txt", "r")
    data = file.read()
    file.close()
    return data

# Actions


def add_ques_paper():
    # console.print("Adding Ques Paper...")
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

    # paper_data = {
    #     "id": int(time.time()),
    #     "subject": sub_id,
    #     "max_marks": max_marks,
    #     "ques_count": tot_ques,
    #     "data": [],
    #     "shuffle": shuffle.lower() == "y"
    # }

    # for idx in range(tot_ques):
    #     ques = console.input("Enter Question: ")
    #     opt_a = console.input("Enter Option A: ")
    #     opt_b = console.input("Enter Option B: ")
    #     opt_c = console.input("Enter Option C: ")
    #     opt_d = console.input("Enter Option D: ")
    #     answer = console.input("Enter Correct Option: ")

    #     paper_data["data"].append({
    #         "question": ques,
    #         "options": [opt_a, opt_b, opt_c, opt_d],
    #         "answer": answer
    #     })

    # save_to_file(paper_data)

    # https://youtube.com/playlist?list=PLTuJWtGVCB8HzEXPc3AKH37_-PXOkhKDH


def edit_ques_paper():
    papers = get_papers_from_db()
    for paper in papers:
        console.print(paper)

    paper_choice = int(console.input("Enter Paper ID to select: "))
    if paper_choice >= len(papers):
        console.print("[red]Invalid Choice![/]")
        return
    paper_id = papers[paper_choice][0]
    selected_paper = get_paper_by_id(paper_id)
    if not selected_paper:
        console.print("[red]Paper Not Found![/]")
        return

    console.print(selected_paper)

    # console.print("Editing Ques Paper...")


def view_results():
    console.print("Viewing Results...")


def add_answer_key():
    console.print("Adding Answer Key...")

# Start


def show_admin_menu() -> None:
    options = ["Add Question Paper", "Edit Existing Paper",
               "View Results", "Add Answer Key"]

    user_choice = show_options(options)

    if user_choice == 0:
        add_ques_paper()
    elif user_choice == 1:
        edit_ques_paper()
    elif user_choice == 2:
        view_results()
    elif user_choice == 3:
        add_answer_key()
    else:
        console.print("invalid Choice")


# add_ques_paper()
# add_paper_to_db("", "", 0, 0, "", 0, 0)
# print(get_paper_by_id(1))
