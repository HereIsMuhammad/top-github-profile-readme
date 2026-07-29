# 003: Rock, Paper, Scissors

A command-line Rock/Paper/Scissors game against the computer, with a running scoreboard (wins/losses/ties) tracked across the whole session.

## Features

- Play rock, paper, or scissors against a randomly-choosing computer
- Accepts full words (`rock`) or short forms (`r`) — case-insensitive
- Input validation — invalid input is rejected without crashing, and the game re-prompts
- Running scoreboard shown after every round, plus a final summary when you quit
- Clean internal design using an `Enum` for moves and a lookup table for win conditions (no long if/elif chains)
- No external dependencies — pure Python standard library

## How to run

```bash
python rock_paper_scissors.py
```

Example session:

```
=== Rock, Paper, Scissors ===
Choose (r)ock, (p)aper, or (s)cissors: rock
You chose rock. Computer chose scissors.
You win! Rock beats scissors.
Wins: 1  Losses: 0  Ties: 0

Play again? (y/n): y
Choose (r)ock, (p)aper, or (s)cissors: p
You chose paper. Computer chose paper.
It's a tie!
Wins: 1  Losses: 0  Ties: 1

Play again? (y/n): n

Final score — Wins: 1  Losses: 0  Ties: 1
Thanks for playing. Goodbye!
```

## How it works

- Moves are modeled with an `Enum` (`Move.ROCK`, `Move.PAPER`, `Move.SCISSORS`) instead of raw strings, which avoids typos and makes the code self-documenting.
- A `BEATS` dictionary maps each move to the move it beats (e.g. `ROCK → SCISSORS`), so the win/loss/tie logic is a simple lookup instead of a chain of `if` statements.
- A `Scoreboard` class tracks wins/losses/ties and formats them for display.

## Requirements

None — uses only the Python standard library (`random`, `enum`). Tested on Python 3.10+.

## Possible extensions

- Add "Rock, Paper, Scissors, Lizard, Spock" (5-move variant)
- Add a "best of N rounds" mode
- Save match history to a file
- Wrap it in a simple Tkinter or web GUI