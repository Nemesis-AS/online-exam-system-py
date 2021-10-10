from rich.console import Console
console = Console()

# Utility Functions
def show_options(options: list) -> int:
    output = ""

    for idx in range(len(options)):
        output += f"{idx+1}.{options[idx]}\n"
    
    console.rule("[bold green]Select Action")
    console.print(output)
    selected_option = int(console.input(f"Select Action[{1} - {len(options)}]: "))

    return selected_option - 1

# Actions
def add_ques_paper():
    console.print("Adding Ques Paper...")

def edit_ques_paper():
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