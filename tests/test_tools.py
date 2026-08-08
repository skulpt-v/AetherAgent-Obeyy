import pytest

from tools.calculator import Calculator


@pytest.fixture
def calculator():
    return Calculator()


def test_basic_addition(calculator):
    result = calculator.calculate("2 + 3")

    assert result == 5


def test_multiplication(calculator):
    result = calculator.calculate("6 * 7")

    assert result == 42


def test_division(calculator):
    result = calculator.calculate("20 / 4")

    assert result == 5


def test_math_expression(calculator):
    result = calculator.calculate(
        "(10 + 5) * 2"
    )

    assert result == 30


def test_power(calculator):
    result = calculator.calculate(
        "2 ** 3"
    )

    assert result == 8


def test_invalid_expression(calculator):
    with pytest.raises(Exception):
        calculator.calculate(
            "this is not mathematics"
        )