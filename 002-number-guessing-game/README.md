# 002: Number Guessing Game

A command-line number guessing game with three difficulty levels. The computer picks a random number and the player has a limited number of attempts to guess it, with "too high" / "too low" hints after each try. Tracks your best score (fewest attempts) for the current session.

## Features

- Three difficulty levels (Easy / Medium / Hard) — each with a different number range and attempt limit
- Input validation (rejects non-numbers and out-of-range guesses without crashing)
- "Too high" / "too low" feedback with remaining attempts shown
- Best-score tracker across multiple rounds in the same session
- Play multiple rounds without restarting the program
- No external dependencies — pure Python standard library

## How to run

```bash
python guessing_game.py
```

Example session:

```
=== Number Guessing Game ===
Select a difficulty:
  1. Easy (1-50, 10 attempts)
  2. Medium (1-100, 7 attempts)
  3. Hard (1-200, 6 attempts)
Enter 1, 2, or 3: 2

I'm thinking of a number between 1 and 100. You have 7 attempts.
Your guess (1-100): 50
Too low. 6 attempts left.
Your guess (1-100): 75
Correct! The number was 75. You got it in 2 attempt(s).
New best score this session: 2 attempt(s)!

Play again? (y/n): n
Thanks for playing. Goodbye!
```

## Difficulty levels

| Level  | Range   | Attempts |
|--------|---------|----------|
| Easy   | 1–50    | 10       |
| Medium | 1–100   | 7        |
| Hard   | 1–200   | 6        |

## Requirements

None — uses only the Python standard library (`random`, `dataclasses`). Tested on Python 3.10+.

## Possible extensions

- Add a "hot/cold" hint based on how close the guess is
- Save best scores to a file so they persist across sessions
- Add a reverse mode where the player picks a number and the computer guesses it (binary search)
- Wrap it in a simple Tkinter or web GUI