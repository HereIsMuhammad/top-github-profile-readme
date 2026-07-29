"""
Number Guessing Game
---------------------
The computer picks a random number, and the player tries to guess it
within a limited number of attempts. Includes selectable difficulty
levels (which control the number range and attempts allowed) and a
best-score tracker for the current session.
"""

from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass(frozen=True)
class Difficulty:
    name: str
    lower_bound: int
    upper_bound: int
    max_attempts: int


DIFFICULTIES: dict[str, Difficulty] = {
    "1": Difficulty("Easy", 1, 50, 10),
    "2": Difficulty("Medium", 1, 100, 7),
    "3": Difficulty("Hard", 1, 200, 6),
}


def choose_difficulty() -> Difficulty:
    print("Select a difficulty:")
    for key, difficulty in DIFFICULTIES.items():
        print(
            f"  {key}. {difficulty.name} "
            f"(1-{difficulty.upper_bound}, {difficulty.max_attempts} attempts)"
        )

    while True:
        choice = input("Enter 1, 2, or 3: ").strip()
        if choice in DIFFICULTIES:
            return DIFFICULTIES[choice]
        print("Invalid choice. Please enter 1, 2, or 3.")


def get_guess(lower_bound: int, upper_bound: int) -> int:
    while True:
        raw = input(f"Your guess ({lower_bound}-{upper_bound}): ").strip()
        try:
            guess = int(raw)
        except ValueError:
            print("Please enter a whole number.")
            continue

        if not (lower_bound <= guess <= upper_bound):
            print(f"Guess must be between {lower_bound} and {upper_bound}.")
            continue

        return guess


def play_round(difficulty: Difficulty) -> int | None:
    """Plays one round. Returns the number of attempts used to win, or None if lost."""
    target = random.randint(difficulty.lower_bound, difficulty.upper_bound)
    attempts_used = 0

    print(
        f"\nI'm thinking of a number between {difficulty.lower_bound} "
        f"and {difficulty.upper_bound}. You have {difficulty.max_attempts} attempts."
    )

    while attempts_used < difficulty.max_attempts:
        guess = get_guess(difficulty.lower_bound, difficulty.upper_bound)
        attempts_used += 1
        remaining = difficulty.max_attempts - attempts_used

        if guess == target:
            print(f"Correct! The number was {target}. "
                  f"You got it in {attempts_used} attempt(s).")
            return attempts_used
        elif guess < target:
            print(f"Too low.{f' {remaining} attempts left.' if remaining else ''}")
        else:
            print(f"Too high.{f' {remaining} attempts left.' if remaining else ''}")

    print(f"Out of attempts! The number was {target}.")
    return None


def main() -> None:
    print("=== Number Guessing Game ===")
    best_score: int | None = None  # fewest attempts to win, across this session

    while True:
        difficulty = choose_difficulty()
        attempts = play_round(difficulty)

        if attempts is not None:
            print("Nice job!")
            if best_score is None or attempts < best_score:
                best_score = attempts
                print(f"New best score this session: {best_score} attempt(s)!")
            else:
                print(f"Your best score this session is still {best_score} attempt(s).")

        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing. Goodbye!")
            break


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")