"""
Rock, Paper, Scissors
----------------------
Classic Rock/Paper/Scissors against the computer, with running score
tracking across rounds (wins, losses, ties) for the current session.
"""

from __future__ import annotations

import random
from enum import Enum


class Move(Enum):
    ROCK = "rock"
    PAPER = "paper"
    SCISSORS = "scissors"


# Maps a move to the move it beats.
BEATS: dict[Move, Move] = {
    Move.ROCK: Move.SCISSORS,
    Move.PAPER: Move.ROCK,
    Move.SCISSORS: Move.PAPER,
}

SHORTCUTS: dict[str, Move] = {
    "r": Move.ROCK,
    "p": Move.PAPER,
    "s": Move.SCISSORS,
    "rock": Move.ROCK,
    "paper": Move.PAPER,
    "scissors": Move.SCISSORS,
}


class Scoreboard:
    def __init__(self) -> None:
        self.wins = 0
        self.losses = 0
        self.ties = 0

    def record(self, result: str) -> None:
        if result == "win":
            self.wins += 1
        elif result == "loss":
            self.losses += 1
        else:
            self.ties += 1

    def __str__(self) -> str:
        return f"Wins: {self.wins}  Losses: {self.losses}  Ties: {self.ties}"


def get_player_move() -> Move:
    while True:
        raw = input("Choose (r)ock, (p)aper, or (s)cissors: ").strip().lower()
        if raw in SHORTCUTS:
            return SHORTCUTS[raw]
        print("Invalid choice. Please enter rock, paper, or scissors (or r/p/s).")


def get_computer_move() -> Move:
    return random.choice(list(Move))


def decide_winner(player: Move, computer: Move) -> str:
    """Returns 'win', 'loss', or 'tie' from the player's perspective."""
    if player == computer:
        return "tie"
    if BEATS[player] == computer:
        return "win"
    return "loss"


def play_round(scoreboard: Scoreboard) -> None:
    player_move = get_player_move()
    computer_move = get_computer_move()

    print(f"You chose {player_move.value}. Computer chose {computer_move.value}.")

    result = decide_winner(player_move, computer_move)
    scoreboard.record(result)

    if result == "win":
        print(f"You win! {player_move.value.capitalize()} beats {computer_move.value}.")
    elif result == "loss":
        print(f"You lose! {computer_move.value.capitalize()} beats {player_move.value}.")
    else:
        print("It's a tie!")

    print(scoreboard)


def main() -> None:
    print("=== Rock, Paper, Scissors ===")
    scoreboard = Scoreboard()

    while True:
        play_round(scoreboard)

        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            print(f"\nFinal score — {scoreboard}")
            print("Thanks for playing. Goodbye!")
            break


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")