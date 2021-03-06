import time

# DEBUG
import json
# =======

from rich.console import Console
console = Console()

# Utility Functions
def show_options(options: list) -> int:
    output = ""

    for idx in range(len(options)):
        output += f"{idx+1}.{options[idx]}\n"
    
    console.rule("[bold green]Select Action[/]")
    console.print(output)
    selected_option = int(console.input(f"Select Action[{1} - {len(options)}]: "))

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
    sub_id = console.input("Enter subject: ")
    max_marks = int(console.input("Enter Max. Marks: "))
    tot_ques = int(console.input("Enter No. of questions: "))
    shuffle = console.input("Shuffle Questions[Y/N]: ")

    paper_data = {
        "id": int(time.time()),
        "subject": sub_id,
        "max_marks": max_marks,
        "ques_count": tot_ques,
        "data": [],
        "shuffle": shuffle.lower() == "y"
    }

    for idx in range(tot_ques):
        ques = console.input("Enter Question: ")
        opt_a = console.input("Enter Option A: ")
        opt_b = console.input("Enter Option B: ")
        opt_c = console.input("Enter Option C: ")
        opt_d = console.input("Enter Option D: ")
        answer = console.input("Enter Correct Option: ")

        paper_data["data"].append({
            "question": ques,
            "options": [opt_a, opt_b, opt_c, opt_d],
            "answer": answer
        })
    
    save_to_file(paper_data)
    

def edit_ques_paper():
    papers = json.loads(read_from_file())
    console.print(papers)
    console.print("Editing Ques Paper...")

def view_results():
    console.print("Viewing Results...")

def add_answer_key():
    console.print("Adding Answer Key...")

# Start
def show_admin_menu() -> None:
    options = ["Add Question Paper", "Edit Existing Paper", "View Results", "Add Answer Key"]
    
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