import pytest

from app.main import add, greet


def test_add():
    assert add(2, 3) == 5


def test_greet():
    assert greet("World") == "Hello, World!"

def  test_greet2():
    assert greet("Person") == "Hello, Person!"

def  test_greet2():
    assert greet("Norou") == "Hello, Norou!"

def test_greet_empty_raises():
    with pytest.raises(ValueError):
        greet("   ")
