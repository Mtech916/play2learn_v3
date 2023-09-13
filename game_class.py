import threading
import time


class Game:
    def __init__(self, game_time):
        """Initialize the game."""
        self.game_time = game_time
        self.timer = threading.Thread(target=self.start_timer)
        self.score = 0
        self.game_over = threading.Event()
        self.word_length = None

    def start_timer(self):
        """Start the timer."""
        while self.game_time > 0 and not self.game_over.is_set():
            time.sleep(1)
            self.game_time -= 1

    def end_game(self, you_won):
        """End the game."""

        won = you_won

        if not won:
            print("\nTime's Up!")
            print(f"\nYour score is {self.score}.")
            print("-" * 50)
        else:
            print("\nYou Won!")
            print(f"\nYour score is {self.score}.")
            print(f"\nYou got all the anagrams for {self.word_length} letter words!")
            print("-" * 50)

        self.game_over.set()

    def run(self):
        """Create a run method."""
        raise NotImplementedError("You must implement the run method.")
