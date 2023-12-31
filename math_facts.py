from game_class import Game
import threading
import random


class MathFactsGame(Game):
    """Math Facts Game"""

    def choose_operation(self):
        """player chooses operation"""
        operation = None
        operators = ["+", "-", "*", "/"]
        while operation not in operators:
            operation = input(f"Please enter an operation {operators}: ")
            if operation not in operators:
                print(f"You entered operator: {operation}")
                print("That is not a valid operation.")
                operation = input(
                    f"--Try again-- Please enter an operation {operators}: "
                )
        return operation

    def choose_max_number(self):
        """player chooses max number"""
        try:
            max_number = None
            max_num_range = range(1, 101)
            while max_number not in max_num_range:
                max_number = int(input("Please enter a max number between 1 and 100: "))
                if max_number not in max_num_range:
                    print(f"You entered max number: {max_number}")
                    print("That is not a valid number.")
                    max_number = int(
                        input(
                            "--Try again-- Please enter a max number between 1 and 100: "
                        )
                    )
            return max_number
        except ValueError:
            print("That is not a valid number.")
            print("-" * 50)
            return self.choose_max_number()

    def generate_problem(self, operation, max_number):
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

    def check_user_answer(self, display_problem):
        """Check if user answer is a valid integer"""

        try:
            user_answer = int(input("Enter an answer: "))
            return user_answer
        except ValueError:
            print("That is not a valid number.")
            print("-" * 50)
            print(f"{display_problem}")
            print(f"You have {self.game_time} seconds left.")
            return self.check_user_answer(display_problem)

    def check_answer(self, operation, rand_num1, rand_num2, user_answer):
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

    def run(self):
        """Run the game."""
        operation = self.choose_operation()
        max_number = self.choose_max_number()

        if operation and max_number:
            timer_thread = threading.Thread(target=self.start_timer)
            timer_thread.start()

        while not self.game_over.is_set():
            display_problem, rand_num1, rand_num2 = self.generate_problem(
                operation, max_number
            )

            last_guess_correct = False

            while not last_guess_correct:
                print(f"{display_problem}")
                print(f"You have {self.game_time} seconds left.")
                user_answer = self.check_user_answer(display_problem)
                checked = self.check_answer(
                    operation, rand_num1, rand_num2, user_answer
                )

                if checked and self.game_time > 0:
                    # last_guess_correct = True
                    self.score += 1
                    print(f"{user_answer} is correct!")
                    print("-" * 50)
                    break
                elif self.game_time == 0:
                    # last_guess_correct = True
                    you_won = False
                    print(f"\nSorry, you didn't get that answer in on time.")
                    self.end_game(you_won)
                    break
                else:
                    print(f"{user_answer} is not correct. Please try again.")
                    print("-" * 50)


if __name__ == "__main__":
    while True:
        try:
            math_facts_game = MathFactsGame(30)
            math_facts_game.run()

            play_again = input(f"Press enter to play again or 'q' to quit: ")
            if not play_again or play_again.upper() != "Q":
                continue
            elif play_again.upper() == "Q":
                break
        except KeyboardInterrupt:
            math_facts_game.quit_game()
            print("\nThanks for playing!")
            break
