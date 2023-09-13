import threading
import random
import time

game_time = 30
game_over = threading.Event()
score = 0


def choose_operation():
    """player chooses operation"""
    operation = None
    operators = ["+", "-", "*", "/"]
    while operation not in operators:
        operation = input(f"Please enter an operation {operators}: ")
        if operation not in operators:
            print(f"You entered operator: {operation}")
            print("That is not a valid operation.")
            operation = input(f"--Try again-- Please enter an operation {operators}: ")
    return operation


def choose_max_number():
    """player chooses max number"""
    max_number = None
    max_num_range = range(1, 101)
    while max_number not in max_num_range:
        max_number = int(input("Please enter a max number between 1 and 100: "))
        if max_number not in max_num_range:
            print(f"You entered max number: {max_number}")
            print("That is not a valid number.")
            max_number = int(
                input("--Try again-- Please enter a max number between 1 and 100: ")
            )
    return max_number


def start_timer():
    """Start the timer."""
    global game_time, game_over
    while game_time > 0 and not game_over.is_set():
        time.sleep(1)
        game_time -= 1


def generate_problem(operation, max_number):
    """Generate a random math problem."""
    rand_num1 = random.randint(1, max_number)
    rand_num2 = random.randint(1, max_number)

    if operation == "/":
        while rand_num1 % rand_num2 != 0:
            rand_num1 = random.randint(1, max_number)
            rand_num2 = random.randint(1, max_number)
    elif operation == "-":
        while rand_num1 - rand_num2 < 0:
            rand_num1 = random.randint(1, max_number)
            rand_num2 = random.randint(1, max_number)

    math_problem = f"{rand_num1} {operation} {rand_num2} = ?"

    return math_problem, rand_num1, rand_num2


def check_answer(operation, rand_num1, rand_num2, user_answer):
    """Check if user answer is truthy"""

    if operation == "+":
        answer = rand_num1 + rand_num2
    elif operation == "-":
        answer = rand_num1 - rand_num2
    elif operation == "*":
        answer = rand_num1 * rand_num2
    elif operation == "/":
        answer = rand_num1 / rand_num2

    if user_answer == answer:
        return True
    else:
        return False


def end_game():
    """End the game."""
    global score

    game_over.set()

    print(f"\nSorry, you didn't get that answer in on time.")
    print(f"\nYour score is {score}.")

    time.sleep(1)
    reset_game()


def reset_game():
    global game_time, score, game_over

    play_again = input("Press enter to play again or 'q' to quit: ")
    if play_again.upper() == "Q":
        return
    else:
        game_time = 30
        score = 0
        game_over = threading.Event()

    time.sleep(1)
    main()


def main():
    global game_time, score, game_over
    operation = choose_operation()
    max_number = choose_max_number()

    if operation and max_number:
        timer_thread = threading.Thread(target=start_timer)
        timer_thread.start()

    while not game_over.is_set():
        display_problem, rand_num1, rand_num2 = generate_problem(operation, max_number)
        print(f"{display_problem}")
        print(f"You have {game_time} seconds left.")
        user_answer = int(input("Enter an answer: "))
        checked = check_answer(operation, rand_num1, rand_num2, user_answer)

        if checked and game_time > 0:
            score += 1
            print(f"{user_answer} is correct!")
            print("-" * 50)
        else:
            if game_time == 0:
                end_game()
            else:
                print(f"{user_answer} is not correct. Please try again.")


if __name__ == "__main__":
    main()
