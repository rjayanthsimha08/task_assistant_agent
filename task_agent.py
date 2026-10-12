
"""A small, deterministic task assistant with tool selection."""

import operator
import re
from collections.abc import Callable


def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b

def power(base: float, exponent: int) -> float:
    """Raise a number to an integer power."""
    if not -100 <= exponent <= 100:
        raise ValueError("Exponent must be between -100 and 100")

    return base**exponent

def calculate(a: float, op: str, b: float) -> float:
    """Calculate using an explicitly supported arithmetic operator."""
    operations: dict[str, Callable[[float, float], float]] = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv,
    }

    if op not in operations:
        raise ValueError(f"Unsupported operator: {op}")

    if op == "/" and b == 0:
        raise ValueError("Cannot divide by zero")

    return operations[op](a, b)


def select_tool(task: str) -> str:
    """Choose a tool based on the user's task."""
    command = task.strip().lower()

    if command == "help":
        return "help"
    if command.startswith("add "):
        return "add"
    if command.startswith("calculate "):
        return "calculate"
    if command.startswith("power "):
        return "power"

    return "unknown"


def run_agent(task: str) -> str:
    """Route the task to a tool and return its result."""
    tool = select_tool(task)
    command = task.strip()

    if tool == "help":
        return (
            "Available commands:\n"
            "  add <number> <number>\n"
            "  calculate <number> <+|-|*|/> <number>\n"
            "  help"
            "  power <base> <integer exponent>"
        )
    if tool == "power":
            match = re.fullmatch(
                r"power\s+(-?\d+(?:\.\d+)?)\s+(-?\d+)",
                command,
                re.IGNORECASE,
            )
            if not match:
                return "Error: use 'power <base> <integer exponent>'"

            base = float(match.group(1))
            exponent = int(match.group(2))
            return f"Result: {power(base, exponent):g}"
    

    try:
        if tool == "add":
            match = re.fullmatch(
                r"add\s+(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)",
                command,
                re.IGNORECASE,
            )
            if not match:
                return "Error: use 'add <number> <number>'"

            result = add(float(match.group(1)), float(match.group(2)))
            return f"Result: {result:g}"

        if tool == "calculate":
            match = re.fullmatch(
                r"calculate\s+(-?\d+(?:\.\d+)?)\s+([+\-*/])\s+"
                r"(-?\d+(?:\.\d+)?)",
                command,
                re.IGNORECASE,
            )
            if not match:
                return "Error: use 'calculate <number> <operator> <number>'"

            a, op, b = float(match.group(1)), match.group(2), float(match.group(3))
            return f"Result: {calculate(a, op, b):g}"

        return "I don't understand that task. Type 'help' for commands."

    except ValueError as exc:
        return f"Error: {exc}"


if __name__ == "__main__":
    print("Task Assistant Agent. Type 'quit' to exit.")

    while True:
        user_task = input("\nTask: ").strip()

        if user_task.lower() == "quit":
            print("Goodbye!")
            break

        print(run_agent(user_task))
