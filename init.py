import config
import mysql.connector
from rich.console import Console

console = Console()

db = mysql.connector.connect(
    username="root",
    passwd=config.MYSQL_PASSWORD,
    host="localhost",
    charset="utf8"
)
cursor = db.cursor()


def init_db(db_name: str) -> None:
    cursor.execute("SHOW DATABASES")
    dbs = cursor.fetchall()
    found = False

    for item in dbs:
        if item[0].lower() == db_name.lower():
            found = True
            break

    if found:
        console.print("[green bold]Database Found[/]")
    else:
        console.print("[yellow bold]Creating Database...[/]")
        create_databases(db_name)


def create_databases(db_name: str) -> None:
    cursor.execute(f"CREATE DATABASE {db_name}")
    cursor.execute(f"USE {db_name}")

    # Create Tables
    cursor.execute(
        "CREATE TABLE Users(username VARCHAR(40) PRIMARY KEY, password VARCHAR(40) NOT NULL, admin BOOL DEFAULT FALSE, class TINYINT)")
    cursor.execute(
        "CREATE TABLE Papers(id INT PRIMARY KEY AUTO_INCREMENT, title VARCHAR(50) DEFAULT 'Question Paper', subject VARCHAR(5) NOT NULL, max_marks TINYINT DEFAULT 20, noq TINYINT DEFAULT 5, start TIMESTAMP DEFAULT CURRENT_TIMESTAMP, duration INT, class TINYINT NOT NULL)")
    cursor.execute(
        "CREATE TABLE Questions(id INT PRIMARY KEY AUTO_INCREMENT, ques_text VARCHAR(50) NOT NULL, opt_a VARCHAR(25) NOT NULL,  opt_b VARCHAR(25) NOT NULL,  opt_c VARCHAR(25) NOT NULL,  opt_d VARCHAR(25) NOT NULL, answer CHAR(1), ques_order INT, ques_paper_id INT)")
    cursor.execute(
        "CREATE TABLE Results(id INT PRIMARY KEY AUTO_INCREMENT, paper_id INT, user_id VARCHAR(50), marks INT, answers VARCHAR(100))")
    cursor.execute(
        "CREATE TABLE Complaints(id INT PRIMARY KEY AUTO_INCREMENT, body VARCHAR(250) NOT NULL, resolved BOOL DEFAULT FALSE, response VARCHAR(250))")
    db.commit()

    # Populate Tables
    cursor.execute("INSERT INTO Users VALUES('akshat', 'password1', TRUE, 12)")
    cursor.execute("INSERT INTO Users VALUES('kaif', 'password2', TRUE, 12)")
    db.commit()

    console.print("[green bold]Database Created![/]")
