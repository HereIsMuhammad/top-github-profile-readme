"""
Unit & Currency Converter
--------------------------
Converts between common units of length, weight, and temperature, plus
currency conversion. Currency rates are fetched live from a free public
API when internet access is available; if the request fails (offline,
API down, etc.), it automatically falls back to a small built-in table
of approximate rates so the program still works.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass

# ---------------------------------------------------------------------------
# Length (base unit: meters)
# ---------------------------------------------------------------------------
LENGTH_TO_METERS: dict[str, float] = {
    "mm": 0.001,
    "cm": 0.01,
    "m": 1.0,
    "km": 1000.0,
    "inch": 0.0254,
    "foot": 0.3048,
    "yard": 0.9144,
    "mile": 1609.344,
}

# ---------------------------------------------------------------------------
# Weight (base unit: grams)
# ---------------------------------------------------------------------------
WEIGHT_TO_GRAMS: dict[str, float] = {
    "mg": 0.001,
    "g": 1.0,
    "kg": 1000.0,
    "oz": 28.349523125,
    "lb": 453.59237,
}

# ---------------------------------------------------------------------------
# Fallback currency rates (approximate, relative to 1 USD).
# Used only if a live rate lookup fails (e.g. no internet connection).
# ---------------------------------------------------------------------------
FALLBACK_USD_RATES: dict[str, float] = {
    "USD": 1.0,
    "EUR": 0.92,
    "GBP": 0.79,
    "PKR": 278.0,
    "INR": 83.5,
    "JPY": 156.0,
    "CAD": 1.36,
    "AUD": 1.51,
}

CURRENCY_API_URL = "https://open.er-api.com/v6/latest/USD"


@dataclass(frozen=True)
class ConversionResult:
    value: float
    from_unit: str
    to_unit: str
    source: str = "offline"  # "live" for currency fetched from the API


def convert_length(value: float, from_unit: str, to_unit: str) -> float:
    from_unit, to_unit = from_unit.lower(), to_unit.lower()
    if from_unit not in LENGTH_TO_METERS or to_unit not in LENGTH_TO_METERS:
        raise ValueError(f"Unknown length unit. Supported: {', '.join(LENGTH_TO_METERS)}")
    meters = value * LENGTH_TO_METERS[from_unit]
    return meters / LENGTH_TO_METERS[to_unit]


def convert_weight(value: float, from_unit: str, to_unit: str) -> float:
    from_unit, to_unit = from_unit.lower(), to_unit.lower()
    if from_unit not in WEIGHT_TO_GRAMS or to_unit not in WEIGHT_TO_GRAMS:
        raise ValueError(f"Unknown weight unit. Supported: {', '.join(WEIGHT_TO_GRAMS)}")
    grams = value * WEIGHT_TO_GRAMS[from_unit]
    return grams / WEIGHT_TO_GRAMS[to_unit]


def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    from_unit, to_unit = from_unit.lower(), to_unit.lower()
    valid = {"c", "f", "k"}
    if from_unit not in valid or to_unit not in valid:
        raise ValueError("Unknown temperature unit. Supported: C, F, K")

    # Convert input to Celsius first.
    if from_unit == "c":
        celsius = value
    elif from_unit == "f":
        celsius = (value - 32) * 5 / 9
    else:  # kelvin
        celsius = value - 273.15

    # Convert Celsius to the target unit.
    if to_unit == "c":
        return celsius
    if to_unit == "f":
        return celsius * 9 / 5 + 32
    return celsius + 273.15  # kelvin


def fetch_live_usd_rates() -> dict[str, float] | None:
    """Attempts to fetch live exchange rates. Returns None on any failure."""
    try:
        with urllib.request.urlopen(CURRENCY_API_URL, timeout=4) as response:
            data = json.loads(response.read().decode("utf-8"))
            rates = data.get("rates")
            if isinstance(rates, dict) and rates:
                return rates
    except (urllib.error.URLError, TimeoutError, ValueError, OSError):
        pass
    return None


def convert_currency(value: float, from_code: str, to_code: str) -> ConversionResult:
    from_code, to_code = from_code.upper(), to_code.upper()

    live_rates = fetch_live_usd_rates()
    rates = live_rates if live_rates is not None else FALLBACK_USD_RATES
    source = "live" if live_rates is not None else "offline"

    if from_code not in rates or to_code not in rates:
        raise ValueError(
            f"Unknown currency code. Supported: {', '.join(sorted(rates))}"
        )

    usd_amount = value / rates[from_code]
    converted = usd_amount * rates[to_code]
    return ConversionResult(converted, from_code, to_code, source)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

MENU = """
Unit & Currency Converter
1. Length   (mm, cm, m, km, inch, foot, yard, mile)
2. Weight   (mg, g, kg, oz, lb)
3. Temperature (C, F, K)
4. Currency (USD, EUR, GBP, PKR, INR, JPY, CAD, AUD, ...)
5. Quit
"""


def prompt_float(message: str) -> float:
    while True:
        raw = input(message).strip()
        try:
            return float(raw)
        except ValueError:
            print("Please enter a valid number.")


def handle_length() -> None:
    value = prompt_float("Value: ")
    from_unit = input(f"From unit ({'/'.join(LENGTH_TO_METERS)}): ").strip()
    to_unit = input(f"To unit ({'/'.join(LENGTH_TO_METERS)}): ").strip()
    try:
        result = convert_length(value, from_unit, to_unit)
        print(f"{value} {from_unit} = {result:.6g} {to_unit}")
    except ValueError as error:
        print(f"Error: {error}")


def handle_weight() -> None:
    value = prompt_float("Value: ")
    from_unit = input(f"From unit ({'/'.join(WEIGHT_TO_GRAMS)}): ").strip()
    to_unit = input(f"To unit ({'/'.join(WEIGHT_TO_GRAMS)}): ").strip()
    try:
        result = convert_weight(value, from_unit, to_unit)
        print(f"{value} {from_unit} = {result:.6g} {to_unit}")
    except ValueError as error:
        print(f"Error: {error}")


def handle_temperature() -> None:
    value = prompt_float("Value: ")
    from_unit = input("From unit (C/F/K): ").strip()
    to_unit = input("To unit (C/F/K): ").strip()
    try:
        result = convert_temperature(value, from_unit, to_unit)
        print(f"{value}°{from_unit.upper()} = {result:.2f}°{to_unit.upper()}")
    except ValueError as error:
        print(f"Error: {error}")


def handle_currency() -> None:
    value = prompt_float("Amount: ")
    from_code = input("From currency code (e.g. USD): ").strip()
    to_code = input("To currency code (e.g. PKR): ").strip()
    try:
        result = convert_currency(value, from_code, to_code)
        tag = "live rate" if result.source == "live" else "offline/approximate rate"
        print(f"{value} {result.from_unit} = {result.value:.2f} {result.to_unit} ({tag})")
    except ValueError as error:
        print(f"Error: {error}")


def main() -> None:
    handlers = {
        "1": handle_length,
        "2": handle_weight,
        "3": handle_temperature,
        "4": handle_currency,
    }

    while True:
        print(MENU)
        choice = input("Choose an option (1-5): ").strip()

        if choice == "5":
            print("Goodbye!")
            break

        handler = handlers.get(choice)
        if handler is None:
            print("Invalid option. Please choose 1-5.")
            continue

        handler()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")