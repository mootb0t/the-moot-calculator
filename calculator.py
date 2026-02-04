"""the-moot-calculator

A small, dependency-free calculator with a safe expression evaluator.

- Supports: +, -, *, /, //, %, **, parentheses, unary +/-
- Supports numeric literals: int, float (e.g., 3, 3.14, 1e-3)

This module intentionally does NOT allow arbitrary Python execution.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import Union

Number = Union[int, float]


class CalculatorError(Exception):
    """Raised for invalid expressions or evaluation errors."""


@dataclass(frozen=True)
class Calculator:
    """Safe arithmetic evaluator."""

    def evaluate(self, expr: str) -> Number:
        expr = (expr or "").strip()
        if not expr:
            raise CalculatorError("empty expression")

        try:
            node = ast.parse(expr, mode="eval")
        except SyntaxError as e:
            raise CalculatorError(f"syntax error: {e.msg}") from e

        return self._eval(node.body)

    def _eval(self, node: ast.AST) -> Number:
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise CalculatorError("only numeric literals are allowed")

        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            val = self._eval(node.operand)
            return +val if isinstance(node.op, ast.UAdd) else -val

        if isinstance(node, ast.BinOp):
            left = self._eval(node.left)
            right = self._eval(node.right)

            op = node.op
            try:
                if isinstance(op, ast.Add):
                    return left + right
                if isinstance(op, ast.Sub):
                    return left - right
                if isinstance(op, ast.Mult):
                    return left * right
                if isinstance(op, ast.Div):
                    return left / right
                if isinstance(op, ast.FloorDiv):
                    return left // right
                if isinstance(op, ast.Mod):
                    return left % right
                if isinstance(op, ast.Pow):
                    return left ** right
            except ZeroDivisionError as e:
                raise CalculatorError("division by zero") from e

            raise CalculatorError(f"operator not allowed: {type(op).__name__}")

        # Disallow names, calls, attributes, subscripts, comprehensions, etc.
        raise CalculatorError(f"expression not allowed: {type(node).__name__}")


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        prog="the-moot-calculator",
        description="A tiny safe calculator for arithmetic expressions.",
    )
    parser.add_argument("expr", nargs="?", help='Expression to evaluate (e.g., "(2+3)*4")')
    args = parser.parse_args()

    calc = Calculator()

    if args.expr:
        try:
            print(calc.evaluate(args.expr))
        except CalculatorError as e:
            raise SystemExit(f"error: {e}")
        return

    # REPL
    print("the-moot-calculator — type an expression, or 'quit' to exit")
    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not line:
            continue
        if line.lower() in {"q", "quit", "exit"}:
            break
        try:
            print(calc.evaluate(line))
        except CalculatorError as e:
            print(f"error: {e}")


if __name__ == "__main__":
    main()
