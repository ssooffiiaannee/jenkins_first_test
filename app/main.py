"""Minimal service used by the Jenkins example pipeline."""

from __future__ import annotations


def add(a: int, b: int) -> int:
    return a + b


def greet(name: str) -> str:
    if not name or not name.strip():
        raise ValueError("name must be non-empty")
    return f"Hello, {name.strip()}!"


if __name__ == "__main__":
    print(greet("Jenkins"))
