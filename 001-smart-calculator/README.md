# 001: Smart Calculator

A command-line calculator that handles `+`, `-`, `*`, `/`, `%`, and parentheses — with correct operator precedence (e.g. multiplication before addition).

Unlike many beginner calculators, this one does **not** use Python's built-in `eval()`. Instead, it parses expressions manually using a small **recursive descent parser** (the same technique real interpreters/compilers use). This avoids the security risks of `eval()` and is a good introduction to how parsing works under the hood.

## Features

- Supports `+`, `-`, `*`, `/`, `%`, and nested parentheses
- Correct operator precedence (`*`, `/`, `%` before `+`, `-`)
- Handles negative numbers and decimals
- Friendly error messages (division/modulo by zero, invalid characters, unbalanced parentheses)
- No external dependencies — pure Python standard library

## How to run

```bash
python calculator.py
```

Then type expressions at the prompt:

Smart Calculator — supports + - * / % and parentheses
Type 'quit' or 'exit' to leave.

5 + 3 * (2 - 1)
8
10 / 4
2.5
7 % 3
1
(2 + 3) * (4 - 1)
15
2 / 0
Error: Division by zero
quit
Goodbye!


## How it works

1. **Tokenizer** — breaks the raw string into a list of tokens (numbers, operators, parentheses).
2. **Parser** — walks the tokens using three levels of grammar rules (`expr → term → factor`) so that multiplication/division/modulo always bind tighter than addition/subtraction, and parentheses override precedence entirely.

## Requirements

None — uses only the Python standard library. Tested on Python 3.10+.

## Possible extensions

- Add support for exponentiation (`^` or `**`)
- Add support for functions like `sqrt()`, `sin()`, `cos()`
- Add a history of previous calculations
- Wrap it in a simple Tkinter GUI
