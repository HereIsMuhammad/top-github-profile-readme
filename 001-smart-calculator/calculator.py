from __future__ import annotations


class CalculatorError(Exception):
    """Raised when an expression is invalid or cannot be evaluated."""


class Tokenizer:
    """Breaks an input string into a list of tokens (numbers/operators/parens)."""

    def __init__(self, expression: str) -> None:
        self.expression = expression
        self.position = 0

    def tokenize(self) -> list[str]:
        tokens: list[str] = []
        i = 0
        expr = self.expression.replace(" ", "")

        while i < len(expr):
            char = expr[i]

            if char.isdigit() or char == ".":
                start = i
                while i < len(expr) and (expr[i].isdigit() or expr[i] == "."):
                    i += 1
                tokens.append(expr[start:i])
                continue

            if char in "+-*/%()":
                tokens.append(char)
                i += 1
                continue

            raise CalculatorError(f"Unexpected character: '{char}'")

        return tokens


class Parser:
    """
    Recursive descent parser/evaluator.

    Grammar (highest to lowest precedence):
        factor  := NUMBER | '(' expr ')'
        term    := factor (('*' | '/' | '%') factor)*
        expr    := term (('+' | '-') term)*
    """

    def __init__(self, tokens: list[str]) -> None:
        self.tokens = tokens
        self.position = 0

    def peek(self) -> str | None:
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def consume(self) -> str:
        token = self.peek()
        if token is None:
            raise CalculatorError("Unexpected end of expression")
        self.position += 1
        return token

    def parse(self) -> float:
        result = self.parse_expr()
        if self.peek() is not None:
            raise CalculatorError(f"Unexpected token: '{self.peek()}'")
        return result

    def parse_expr(self) -> float:
        result = self.parse_term()
        while self.peek() in ("+", "-"):
            op = self.consume()
            rhs = self.parse_term()
            result = result + rhs if op == "+" else result - rhs
        return result

    def parse_term(self) -> float:
        result = self.parse_factor()
        while self.peek() in ("*", "/", "%"):
            op = self.consume()
            rhs = self.parse_factor()
            if op == "*":
                result = result * rhs
            elif op == "/":
                if rhs == 0:
                    raise CalculatorError("Division by zero")
                result = result / rhs
            else:  # modulo
                if rhs == 0:
                    raise CalculatorError("Modulo by zero")
                result = result % rhs
        return result

    def parse_factor(self) -> float:
        token = self.peek()

        if token == "(":
            self.consume()
            result = self.parse_expr()
            if self.peek() != ")":
                raise CalculatorError("Missing closing parenthesis")
            self.consume()
            return result

        if token == "-":
            self.consume()
            return -self.parse_factor()

        if token is None:
            raise CalculatorError("Unexpected end of expression")

        try:
            value = float(token)
        except ValueError as exc:
            raise CalculatorError(f"Invalid number: '{token}'") from exc

        self.consume()
        return value


def evaluate(expression: str) -> float:
    """Tokenize, parse, and evaluate a math expression string."""
    tokens = Tokenizer(expression).tokenize()
    if not tokens:
        raise CalculatorError("Empty expression")
    return Parser(tokens).parse()


def format_result(value: float) -> str:
    """Show whole numbers without a trailing .0"""
    if value == int(value):
        return str(int(value))
    return str(round(value, 10))


def main() -> None:
    print("Smart Calculator — supports + - * / % and parentheses")
    print("Type 'quit' or 'exit' to leave.\n")

    while True:
        try:
            expression = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if expression.lower() in ("quit", "exit"):
            print("Goodbye!")
            break

        if not expression:
            continue

        try:
            result = evaluate(expression)
            print(format_result(result))
        except CalculatorError as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()