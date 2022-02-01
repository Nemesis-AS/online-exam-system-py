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
    options = ["Attempt Question Paper", "My Result", "See Prev Papers", "View Answer Key"]
    
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
