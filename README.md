# the-moot-calculator

A small, dependency‑free calculator written in Python.

It *looks* like a toy, but it’s deliberately built like a tiny “serious” tool:
- safe evaluation (no `eval()`)
- predictable operator support
- clear error messages
- minimal surface area

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Features](#features)
3. [Non‑Goals](#non-goals)
4. [Usage](#usage)
   - [CLI (single expression)](#cli-single-expression)
   - [REPL mode](#repl-mode)
5. [Expression Language](#expression-language)
   - [Allowed literals](#allowed-literals)
   - [Allowed operators](#allowed-operators)
   - [Operator precedence](#operator-precedence)
   - [Examples](#examples)
6. [Security Model](#security-model)
7. [Architecture](#architecture)
   - [Parsing](#parsing)
   - [Evaluation](#evaluation)
   - [Error handling](#error-handling)
8. [Testing](#testing)
9. [Performance Notes](#performance-notes)
10. [Roadmap](#roadmap)
11. [FAQ](#faq)
12. [License](#license)

---

## Quick Start

```bash
python3 calculator.py "(2 + 3) * 4"
```

Output:

```text
20
```

---

## Features

- **Safe evaluation** using Python’s `ast` module (no arbitrary code execution)
- Supports standard arithmetic:
  - `+  -  *  /  //  %  **`
  - parentheses: `(...)`
  - unary plus/minus: `+3`, `-7`, `-(2+5)`
- Supports numeric literals:
  - integers: `42`
  - floats: `3.14159`
  - scientific notation: `1e-3`
- **REPL mode** for interactive use

---

## Non‑Goals

This project is intentionally *not*:

- a symbolic math system
- a programmable environment
- a full spreadsheet engine
- a parser for variables, functions, or units

If you want variables and functions, you want a different tool. This tool aims to be *tiny, boring, safe*.

---

## Usage

### CLI (single expression)

```bash
python3 calculator.py "2**10 + 5"
```

### REPL mode

Run without arguments:

```bash
python3 calculator.py
```

Example session:

```text
the-moot-calculator — type an expression, or 'quit' to exit
> 1 + 2
3
> (8 // 3) * 7
14
> quit
```

---

## Expression Language

### Allowed literals

- `int` and `float` constants only

Allowed:
- `0`, `123`, `-45`
- `3.14`, `0.001`
- `1e9`, `2.5e-4`

Not allowed:
- strings: `"hello"`
- booleans: `True` / `False`
- complex: `1+2j`

### Allowed operators

Binary:
- addition: `a + b`
- subtraction: `a - b`
- multiplication: `a * b`
- division: `a / b` (floating division)
- floor division: `a // b`
- modulo: `a % b`
- exponentiation: `a ** b`

Unary:
- `+a`, `-a`

### Operator precedence

This follows Python’s precedence rules:

1. Parentheses `( … )`
2. Exponentiation `**` (right‑associative)
3. Unary `+x`, `-x`
4. Multiplicative `* / // %`
5. Additive `+ -`

### Examples

| Expression | Meaning | Example result |
|---|---|---|
| `2 + 3 * 4` | multiplication first | `14` |
| `(2 + 3) * 4` | parentheses override | `20` |
| `2 ** 3 ** 2` | right assoc: `2 ** (3 ** 2)` | `512` |
| `7 % 4` | remainder | `3` |
| `7 // 4` | floor division | `1` |

---

## Security Model

This calculator **does not** call Python `eval()`.

Instead:

1. Your input string is parsed into an AST (Abstract Syntax Tree) with `ast.parse(..., mode="eval")`.
2. The evaluator walks the AST and only accepts a very small whitelist of node types:
   - `Constant` (numbers)
   - `UnaryOp` with `UAdd` / `USub`
   - `BinOp` with `Add/Sub/Mult/Div/FloorDiv/Mod/Pow`
3. Everything else is rejected (names, function calls, attributes, indexing, etc.).

So inputs like these are **blocked**:

```text
__import__("os").system("rm -rf /")
open("secrets.txt").read()
foo + 1
(1).__class__
```

If the evaluator encounters anything outside the whitelist, it fails with a clear error.

---

## Architecture

### Parsing

- Uses `ast.parse(expr, mode="eval")`.
- Syntax errors are caught and presented as `CalculatorError`.

### Evaluation

- The evaluator is a small recursive descent over AST nodes.
- Only approved nodes are evaluated.
- Division by zero is caught and mapped to a friendly message.

### Error handling

All user-visible errors raise/print `CalculatorError` with messages like:
- `empty expression`
- `syntax error: ...`
- `division by zero`
- `expression not allowed: ...`

---

## Testing

This repo keeps things simple. Options:

- **Smoke test** manually:

```bash
python3 calculator.py "(2+3)*4"
python3 calculator.py "2**3**2"
python3 calculator.py "1/0"  # should error
```

- If you want automated tests, a good next step is adding `pytest` and a small suite for:
  - precedence
  - unary ops
  - invalid node types
  - numeric edge cases

---

## Performance Notes

- Parsing is O(n) in input length for typical cases.
- Evaluation is proportional to the number of AST nodes.
- This is meant for *human-sized expressions*, not huge generated formulas.

---

## Roadmap

Ideas (intentionally not implemented yet):

- [ ] add `pytest` test suite
- [ ] add `pre-commit` hooks (format/lint)
- [ ] optional support for constants (`pi`, `e`) without opening the door to arbitrary names
- [ ] packaging (`pyproject.toml`) so you can `pipx install` it
- [ ] a tiny TUI mode

---

## FAQ

**Why not use `eval()`?**

Because `eval()` evaluates *Python*, not arithmetic, which is unsafe for untrusted input. AST whitelisting keeps the surface area tiny.

**Is this “secure”?**

It’s designed to be safe for typical use: it rejects names, calls, and attribute access. Nothing is perfect, but the attack surface is dramatically smaller than raw `eval()`.

**Can it do variables/functions?**

Not by design. If you want those, we can add them explicitly (e.g., a controlled environment of allowed names and pure math functions), but it’s a different scope.

---

## License

MIT (recommended). If you prefer another license, say so.
