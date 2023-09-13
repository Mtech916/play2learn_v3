import time
import threading
import random
from pathlib import Path
import json

timer_lock = threading.Lock()
game_time = 60
timer_stop = threading.Event()
score = 0


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


def start_timer():
    """Start a timer from 60 seconds."""
    global game_time
    while game_time > 0 and not timer_stop.is_set():
        time.sleep(1)
        with timer_lock:
            game_time -= 1


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


def end_game(you_won=False, wl=0):
    """End the game."""
    global score, timer_stop

    if not you_won:
        print("\nTime's up! Game Over")
        print(f"\nYour score is {score}.")
    else:
        print(f"\nYour score is {score}.")
        print(f"\nYou got all the anagrams for {wl} letter words!")
        print("-" * 50)

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
    game_time = 60
    timer_stop = threading.Event()

    time.sleep(1)

    main()


def main():
    """Run the game."""
    global game_time
    global score
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


if __name__ == "__main__":
    main()
