from pathlib import Path
from game_class import Game
import threading
import random
import json


class AnagramGame(Game):
    """Anagram Game Class"""

    def users_choice(self):
        """Ask the user to choose a word length between 3 and 8."""

        try:
            acceptable_range = range(3, 9)
            while self.word_length not in acceptable_range:
                self.word_length = int(
                    input(
                        f"Please Choose a word length within -> {list(acceptable_range)}: "
                    )
                )
                if self.word_length not in acceptable_range:
                    print(f"Unavailable -> word_length = {self.word_length}")
                    print("That is not an available word length.")
                    self.word_length = int(
                        input(
                            f"-Please Try Again- Choose a word length within -> {list(acceptable_range)}: "
                        )
                    )
            return self.word_length
        except ValueError:
            print("That is not a correct word length.")
            print("-" * 50)
            return self.users_choice()

    def file_path(self, relative_path):
        start_dir = Path(__file__).parent
        return Path(start_dir, relative_path)

    def get_words(self):
        """Get a list of words from anagrams.json, create and return a dictionary of words."""

        anagrams = Path("data/anagrams.json")
        path_to_file = self.file_path(anagrams)
        with path_to_file.open(encoding="utf-8") as f:
            words = json.load(f)
            words = dict(words)
            words = {
                k: [[word.upper() for word in sublist] for sublist in v]
                for k, v in words.items()
            }
            return words

    def create_words_to_play(self, words):
        """Create a list of words to play with from the words dictionary."""

        words_to_guess = []
        key = str(self.word_length)
        words_to_guess = words.pop(key)

        return words_to_guess

    def game_word_lists(self, words_to_guess):
        """Pick a random block of words from words list for the user to play."""

        current_words_to_play = random.choice(words_to_guess)
        words_to_guess.remove(current_words_to_play)

        return current_words_to_play, words_to_guess

    def check_guess(self, user_guess, current_words):
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

        num_of_char = self.users_choice()

        if num_of_char:
            timer_thread = threading.Thread(target=self.start_timer)
            timer_thread.start()

        words = self.get_words()

        words_to_guess = self.create_words_to_play(words)

        # game_play_words are words that might be used in the game
        # current_words are words that are being used in the game
        current_words, game_play_words = self.game_word_lists(words_to_guess)
        # w_o_h is set in order to pass g_p_w back to game_word_lists()
        words_on_hold = game_play_words

        display_word = random.choice(current_words)
        current_words.remove(display_word)
        num_of_words = len(current_words)

        guessed_all = False

        while (not guessed_all) and self.game_time > 0:
            print(f"The word is: {display_word}")
            print(f"There are {num_of_words} words left to guess.")
            print(f"You have {self.game_time} seconds left to guess the word.")

            user_guess = input("Make a guess: ").upper()
            checked = self.check_guess(user_guess, current_words)

            if not checked:
                if user_guess in user_guesses:
                    message = f"You already guessed {user_guess}. Please try again."
                else:
                    message = f"{user_guess} is not a valid anagram. Please try again."
                user_guesses.append(user_guess)
                if self.game_time == 0:
                    print(f"\nSorry, you didn't get that answer in on time.")
                    you_won = False
                    self.end_game(you_won)
                else:
                    print(message)
                    print("-" * 50)
            else:
                self.score += 1
                user_guesses.append(user_guess)
                current_words.remove(user_guess)
                num_of_words = len(current_words)
                if self.game_time == 0:
                    print(f"\nSorry, you didn't get that answer in on time.")
                    you_won = False
                    self.end_game(you_won)
                else:
                    print(f"{user_guess} is correct!")
                    print("-" * 50)

            if num_of_words == 0 and self.game_time > 0:
                guessed_all = True
                print(f"You got all the anagrams for {display_word}!")
                print("-" * 50)

            if guessed_all and game_play_words and self.game_time > 0:
                current_words, game_play_words = self.game_word_lists(words_on_hold)
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
                self.end_game(you_won)


if __name__ == "__main__":
    while True:
        try:
            anagram_game = AnagramGame(60)
            anagram_game.run()

            play_again = input(f"Press enter to play again or 'q' to quit: ")
            if not play_again or play_again.upper() != "Q":
                continue
            elif play_again.upper() == "Q":
                break
        except KeyboardInterrupt:
            anagram_game.quit_game()
            print("\nThanks for playing!")
            break
