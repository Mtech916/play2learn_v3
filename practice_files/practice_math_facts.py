import threading
import random
import time

timer_lock = threading.Lock()
game_time = 30
timer_stop = threading.Event()
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
    max_num_range = range(1, 100)
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
    global game_time, 
    while game_time > 0 and not timer_stop.is_set():
        time.sleep(1)
        with timer_lock:
            game_time -= 1


def generate_problem(operation, max_number):
    """Generate a random math problem."""
    rand_num1 = random.randint(1, max_number)
    rand_num2 = random.randint(1, max_number)

    if operation == "/":
        while rand_num1 % rand_num2 != 0:
            rand_num1 = random.randint(1, max_number)
            # rand_num2 = random.randint(1, max_number)

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
    global score, game_time, timer_stop

    print("\nTime's up!")
    print(f"\nSorry, you didn't get that answer in on time.")
    print(f"\nYour score is {score}.")

    play_again = input(f"Press enter to play again or 'q' to quit: ")

    if not play_again:
        timer_stop.set()
        reset_game()
    elif play_again.lower() == "q":
        timer_stop.set()
        return
    else:
        timer_stop.set()
        return


def reset_game():
    """Reset the game."""
    global game_time, score, timer_lock, timer_stop

    score = 0
    timer_lock = threading.Lock()
    game_time = 30
    timer_stop = threading.Event()

    time.sleep(1)

    main()


def main():
    """Run the game."""
    global game_time
    global score

    operation = choose_operation()

    max_number = choose_max_number()

    # print(f"From main -> operation: {operation}")
    # print(f"From main -> max_number: {max_number}")

    if operation and max_number:
        timer_thread = threading.Thread(target=start_timer)
        timer_thread.start()

    while game_time > 0:
        display_problem, rand_num1, rand_num2 = generate_problem(operation, max_number)

        # print(f"From main -> checked: {checked}")
        # print(f"From main -> user_answer: {user_answer}")

        correct_answer = False

        while not correct_answer:
            print(f"{display_problem}")
            print(f"You have {game_time} seconds left.")
            user_answer = int(input("Enter an answer: "))
            checked = check_answer(operation, rand_num1, rand_num2, user_answer)

            if not checked:
                if game_time == 0:
                    # print(f"\nSorry, you didn't get that answer in on time.")
                    end_game()
                else:
                    print(f"{user_answer} is not correct. Please try again.")
            else:
                if game_time == 0:
                    # print(f"\nSorry, you didn't get that answer in on time.")
                    end_game()
                else:
                    score += 1
                    print(f"{user_answer} is correct!")
                    print("-" * 50)
                    correct_answer = True


if __name__ == "__main__":
    main()
