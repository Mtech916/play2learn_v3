from pathlib import Path
import threading
import time

class Game:
    def __init__(self, game_time):
        self.game_time = game_time
        self.timer = threading.Thread(target=self.start_timer)
        self.score = 0
        self.game_over = threading.Event()

    def start_timer(self):
        while self.game_time > 0 and not self.game_over.is_set():
            time.sleep(1)
            self.game_time -= 1

    def end_game(self):
        print('\nTime's Up!)
        print(f'\nYour score is {self.score}.')
        play_again = input(f'Press enter to play again or 'q' to quit: ')
        if not play-again:
            self.reset_game()
        elif play_again.upper() == 'Q':
            self.game_over.set()

    def reset_game(self):
        self.game_time = 60
        self.score = 0
        self.game_over = threading.Event()
        time.sleep(1)
        self.run()

    def run(self):
        raise NotImplementedError('You must implement the run method.')

class AnagramGame(Game):
    """Anagram Game Class"""
    def users_choice():
        """Ask the user to choose a word length between 5 and 8."""
        word_length = None
        acceptable_range = range(3, 9)
        while word_length not in acceptable_range:
            word_length = int(
                input(f"Please Choose a word length {list(acceptable_range)}: ")
            )
            if word_length not in acceptable_range:
                print("Wrong Choice -> word_length = ", word_length)
                print("That is not a correct word length.")
                word_length = int(
                    input(
                        f"-Please Try Again- Choose a word length {list(acceptable_range)}: "
                    )
                )
        return word_length

    def file_path(relative_path):
        start_dir = Path(__file__).parent
        return Path(start_dir, relative_path)
        
    def get_words():
        """Get a list of words from anagrams.json, create and return a dictionary of words."""

        anagrams = Path("data/anagrams.json")
        path_to_file = file_path(anagrams)
        with path_to_file.open(encoding="utf-8") as f:
            words = json.load(f)
            words = dict(words)
            words = {
                k: [[word.upper() for word in sublist] for sublist in v]
                for k, v in words.items()
            }
            return words

    def create_words_to_play(words, word_length):
        """Create a list of words to play with from the words dictionary."""

        words_to_guess = []
        key = str(word_length)
        words_to_guess = words.pop(key)

        return words_to_guess

    def game_word_lists(words_to_guess):
        """Pick a random block of words from words list for the user to play."""

        current_words_to_play = random.choice(words_to_guess)
        words_to_guess.remove(current_words_to_play)

        return current_words_to_play, words_to_guess

    def check_guess(user_guess, current_words):
        """Check if the user's guess is correct."""
        if user_guess in current_words:
            return True
        else:
            return False

    def run(self):
        """Run the game."""
        display_word = None
        num_of_words = None
        user_guess = None
        user_guesses = []

        word_length = users_choice()

        if word_length:
            timer_thread = threading.Thread(target=start_timer)
            timer_thread.start()

        words = get_words()

        words_to_guess = create_words_to_play(words, word_length)

        # game_play_words are words that might be used in the game
        # current_words are words that are being used in the game
        current_words, game_play_words = game_word_lists(words_to_guess)
        # w_o_h is set in order to pass g_p_w back to game_word_lists()
        words_on_hold = game_play_words

        display_word = random.choice(current_words)
        current_words.remove(display_word)
        num_of_words = len(current_words)

        guessed_all = False

        while (not guessed_all) and game_time > 0:
            print(f" The word is: {display_word}")
            print(f"There are {num_of_words} words left to guess.")
            print(f"You have {game_time} seconds left to guess the word.")

            user_guess = input("Make a guess: ").upper()
            checked = check_guess(user_guess, current_words)

            if not checked:
                if user_guess in user_guesses:
                    message = f"You already guessed {user_guess}. Please try again."
                else:
                    message = f"{user_guess} is not a valid anagram. Please try again."
                user_guesses.append(user_guess)
                if game_time == 0:
                    print(f"\nSorry, you didn't get that answer in on time.")
                    end_game()
                else:
                    print(message)
            else:
                score += 1
                user_guesses.append(user_guess)
                current_words.remove(user_guess)
                num_of_words = len(current_words)
                if game_time == 0:
                    print(f"\nSorry, you didn't get that answer in on time.")
                    end_game()
                else:
                    print(f"{user_guess} is correct!")

            if num_of_words == 0:
                guessed_all = True
                print(f"You got all the anagrams for {display_word}!")
                print("-" * 50)

            if guessed_all and game_play_words and game_time > 0:
                current_words, game_play_words = game_word_lists(words_on_hold)
                user_guesses = []
                display_word = random.choice(current_words)
                current_words.remove(display_word)
                num_of_words = len(current_words)

            if game_play_words:
                guessed_all = False

            if num_of_words:
                guessed_all = False

            if not game_play_words and not num_of_words:
                guessed_all = True
                you_won = True
                end_game(you_won, word_length)

class MathFactsGame(Game):
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

    def generate_problem(operation, max_number):
        """Generate a random math problem."""
        rand_num1 = random.randint(1, max_number)
        rand_num2 = random.randint(1, max_number)

        if operation == "/":
            while rand_num1 % rand_num2 != 0:
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

    def run(self):
        """Run the game."""
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

if __name__ == '__main__':
    anagram_game = AnagramGame(60)
    math_facts_game = MathFactsGame(30)
    
    anagram_game.run()
    math_facts_game.run()                        
