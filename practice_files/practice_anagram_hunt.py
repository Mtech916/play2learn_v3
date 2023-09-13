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
    acceptable_range = range(5, 9)
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
    if game_time == 0:
        end_game()


def file_path(relative_path):
    start_dir = Path(__file__).parent
    return Path(start_dir, relative_path)


def get_words():
    """Get a list of words from ../data/anagrams.json, create and return a dictionary of words."""

    anagrams = Path("data/anagrams.json")
    path_to_file = file_path(anagrams)
    with path_to_file.open(encoding="utf-8") as f:
        words = json.load(f)
        words = dict(words)
        return words


def create_words_to_play(words, word_length):
    """Create a list of words to play with from the words dictionary."""
    # TODO: Create a list of words to play with from the words dictionary
    # return 2 items, 1 list from value of the key of word_length chosen by the user saved as words_to_guess and the other is the remaining data in the dictionary
    # return words_to_guess, remaining_words_to_play
    words_to_guess = []
    remaining_words = []
    key = str(word_length)

    words_to_guess = words.pop(key)
    # if key in words:
    #     words_to_guess = words.pop(key)
    # else:
    #     words_to_guess = []

    remaining_words = words
    return words_to_guess, remaining_words


def game_word_lists(words_to_guess):
    """Pick a random block of words from words list for the user play."""
    random_display_words = random.choice(words_to_guess)
    words_to_guess.remove(random_display_words)
    return random_display_words, words_to_guess


def play(current_words, game_play_words):
    """Play the game."""
    global game_time
    global score
    display_word = None
    num_of_words = None
    # correct_guess = False
    user_guess = None
    user_guesses = []
    user_incorrect_guesses = []

    display_word = random.choice(current_words)
    current_words.remove(display_word)
    num_of_words = len(current_words)

    # while not correct_guess and game_time > 0:
    while len(user_guesses) != len(current_words) and game_time > 0:
        print(f" The words is: {display_word}")
        print(f"There are {num_of_words} words left to guess.")
        print(f"You have {game_time} seconds left to guess the word.")
        user_guess = input("Make a guess: ")

        if user_guess not in current_words:
            user_incorrect_guesses.append(user_guess)
            print(f"{user_guess} is not a valid anagram. Please try again.")
            # print(f"The word is: {display_word}")
        elif user_guess in user_incorrect_guesses:
            print(
                f"You already guessed {user_guess} and this word is not a valid anagram. Please try again."
            )
        elif user_guess in user_guesses:
            print(
                f"You already guessed {user_guess} and this word is a valid anagram. Please try again."
            )
        else:
            correct_guess = True
            score += 1
            user_guesses.append(user_guess)
            current_words.remove(user_guess)
            num_of_words = len(current_words)
            if num_of_words == 0:
                print(f"You got all the anagrams for {display_word}!")
                # need to figure out how to replenish the current_words list
                game_word_lists(game_play_words)
            else:
                print(f"{user_guess} is correct!")
                print(f"There are {num_of_words} words left to guess.")
                print(f"You have {game_time} seconds left to guess the word.")

    # check_guess(display_word, num_of_words, current_words)

    # print(f" The words is: {display_word}")
    # print(f"There are {num_of_words} words left to guess.")
    # user_guess = input("Make a guess: ")
    # if user_guess in current_words_to_play:
    #     current_words_to_play.remove(user_guess)
    #     num_of_words = len(current_words_to_play)
    #     score += 1
    #     print(f"{user_guess} is correct!")
    #     print(f"There are {num_of_words} words left to guess.")
    #     print(f"You have {game_time} seconds left to guess the word.")
    # else:
    # return display_word, current_words


def check_guess(display_word, num_of_words, current_words_to_play):
    """Check if the user guess is in the words_to_guess dictionary."""
    # TODO: Check if the user guess is in the words_to_guess dictionary,
    # if correct then score += 1
    # if user guesses all words in words_to_guess, include timer_stop.set() to gracefully stop the timer
    global game_time
    global score
    correct_guess = False
    user_guess = None

    while not correct_guess and game_time > 0:
        print(f" The words is: {display_word}")
        print(f"There are {num_of_words} words left to guess.")
        print(f"You have {game_time} seconds left to guess the word.")
        user_guess = input("Make a guess: ")

        if user_guess not in current_words_to_play:
            print(f"{user_guess} is not a valid anagram. Please try again.")
            # print(f"The word is: {display_word}")
        else:
            correct_guess = True
            score += 1
            current_words_to_play.remove(user_guess)
            num_of_words = len(current_words_to_play)

            print(f"{user_guess} is correct!")
            print(f"There are {num_of_words} words left to guess.")
            print(f"You have {game_time} seconds left to guess the word.")
        return current_words_to_play


def end_game():
    print("Time's up! Game Over")


def main():
    word_length = users_choice()

    # if word_length:
    #     timer_thread = threading.Thread(target=start_timer)
    #     timer_thread.start()

    words = get_words()

    # remaining_words are words from original dictionary that aren't being used yet
    words_to_guess, remaining_words = create_words_to_play(words, word_length)

    # game_play_words are words that might be used in the game
    # current_words_to_play are words that are being used in the game
    current_words, game_play_words = game_word_lists(words_to_guess)

    play(current_words, game_play_words)

    # user_guess = None
    # user_guess = input("Guess the word: ")

    # check_word = check_guess(user_guess, words_to_guess)
    # guessed_words = []


if __name__ == "__main__":
    main()


# correct_guess = False
#     # user_guess = None


#     while not correct_guess and game_time > 0:
#         user_guess = input("Guess the word: ")
#         if user_guess not in words:
#             print("You guessed incorrectly!")
#             print(f"You have {game_time} seconds left to guess the word.")
#         else:
#             correct_guess = True
#             print("You guessed correctly!")
#             print(f"You guessed the word in with {game_time} seconds reamining.")


# words = {3:["cat", " act", "tac"]['ate', 'eat', 'tea']['nat', 'tan', 'bat'], 4: ['late', 'tale', 'teal']['tare', 'tear', 'rate']['eats', 'east', 'seat']}
