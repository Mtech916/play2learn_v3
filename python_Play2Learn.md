## anagram_hunt.py

- Runs in console
  1 - user is prompted to enter a numeric word length: 5, 6, 7, 8
  ex: Please enter a word length [5, 6, 7, 8]:
  - if word length enter isn't correct, user is prompted again to enter a word length
    ex: That is not a correct word length. Please try again [5, 6, 7, 8]:
    2 - Game Start Params:
  - User enters correct word length,
  - Timer starts counting down from 60 by 1 sec
    - Everytime a msg is logged to console, value of timer needs to be displayed
  - similar to the JS json file, use a list/array of arrays for anagram words
    - From list display a random word based on the word length
      ex: The word is: BEARD
      There are 3 unguessed anagrams.
      You have 60 seconds left.
      Make a guess:
  - If user submits wrong guess, user needs a warning and another prompt:
    ex: BRAID is not a valid anagram. Please try again.
    The word is: BEARD
    There are 3 unguessed anagrams.
    You have 55 seconds left.
    Make a guess:
  - If user submits correct guess, program should tell user and prompt again:
    ex: BREAD is correct!
    The word is: BEARD
    There are 2 unguessed anagrams.
    You have 49 seconds left.
    Make a guess:
  - if user guess a word they have already guessed, user needs a warning and another prompt:
    ex: You already got BREAD. Try again.
    The word is: BEARD
    There are 2 unguessed anagrams.
    You have 44 seconds left.
    Make a guess:
  - if user guesses all the anagrams for a word, a new word should be displayed
    ex: You got all the anagrams for BEARD!
    The word is: REACT
    There are 4 unguessed anagrams.
    You have 38 seconds left.
    Make a guess:
    3 - Game ends when timer runs out or when user guesses all the anagram sets for the specific word length
    ex: Time is up!
    You got 7 anagrams for 5-letter words!
    Press Enter to play again.
  - if time is already up when the user submits an answer, user gets a msg like this:
    ex: Time is up!
    Sorry, you didn’t get that last one in on time.
    You got 7 anagrams for 5-letter words!
    Press Enter to play again.

## math_facts.py

- Runs in console
  1 - User is prmpted to pick an operation:
  ex: Please enter an operation [+, -, x, /]:
  - if user didn't enter a correct operation, user gets an error msg and prmpt to enter another operation again:
    ex: That is not a correct operation. Please try again [+, -, x, /]:
  - After user enter correct operation, user is prmpted for a max number:
    ex: Please enter a max number between 1 and 100:
  - An invalid number gets an error msg and another prmpt  
     ex: That is not a correct operation. Please enter a max number between 1 and 100:
    2 - Game Starts:
  - Timer starts counting down from 30 by 1 sec w/msg logged to console w/value of timer for ea. printed msg
  - A random problem w/selected operation and numbers equal to the max number are displayed:
    ex: 5 x 5 = ?
    You have 30 seconds left.
    Enter an answer:
  - if answer is wrong, user gets an error and prmpt:
    ex: 26 is not correct. Try again! 5 x 5 =?
    You have 28 seconds left.
    Enter an answer:
  - If answer is correct, program shows user and displays new problem:
    ex: 25 is correct!
    3 x 5 = ?
    You have 24 seconds left.
    Enter an answer:  
    3 - Game ends when timer runs out:
    ex: Time is up!
    Sorry, you didn’t get that answer in on time.
    You answered 15 problems!
    Press Enter to play again.

Please Choose a word length [5, 6, 7, 8]: 5
From main func display_word: ['below', 'bowel', 'elbow']
From main func game_play_words: [['abets', 'baste', 'betas', 'beast', 'beats'], ['acres', 'cares', 'races', 'scare'], ['alert', 'alter', 'later'], ['angel', 'angle', 'glean'], ['baker', 'brake', 'break'], ['bared', 'beard', 'bread', 'debar'], ['dater', 'rated', 'trade', 'tread'], ['caret', 'cater', 'crate', 'trace', 'react']]

pulled from line 110

# user_incorrect_guesses = []

pulled from line 149

# if not checked:

        #     user_incorrect_guesses.append(user_guess)
        #     print(f"{user_guess} is not a valid anagram. Please try again.")
        #     # print(f"The word is: {display_word}")
        # elif user_guess in user_incorrect_guesses:
        #     print(
        #         f"You already tried '{user_guess}' and this word is not a valid anagram. Please try again."
        #     )
        # elif user_guess in user_guesses:
        #     print(f"You already guessed {user_guess}. Please try again.")

if game_time == 0: # print(f"\nSorry, you didn't get that answer in on time.") # end_game() # else: # print(f"You already guessed {user_guess}. Please try again.") # else: # user_guesses.append(user_guess) # if game_time == 0: # print(f"\nSorry, you didn't get that answer in on time.") # end_game() # else: # print(f"{user_guess} is not a valid anagram. Please try again.")
