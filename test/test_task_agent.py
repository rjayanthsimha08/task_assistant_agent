import pytest

from task_agent import add, calculate, power, run_agent, select_tool


def test_add():
    assert add(2, 3) == 5


def test_calculate_multiplication():
    assert calculate(4, "*", 3) == 12


def test_calculate_division():
    assert calculate(8, "/", 2) == 4


def test_division_by_zero():
    with pytest.raises(ValueError, match="divide by zero"):
        calculate(8, "/", 0)


def test_unsupported_operator():
    with pytest.raises(ValueError, match="Unsupported operator"):
        calculate(2, "%", 3)


def test_tool_selection():
    assert select_tool("add 2 3") == "add"
    assert select_tool("calculate 8 / 2") == "calculate"
    assert select_tool("help") == "help"
    assert select_tool("do something") == "unknown"


def test_agent_add_command():
    assert run_agent("add 2 3") == "Result: 5"


def test_agent_calculate_command():
    assert run_agent("calculate 8 / 2") == "Result: 4"


def test_agent_invalid_command():
    assert "don't understand" in run_agent("launch a rocket")


def test_agent_malformed_add():
    assert "Error:" in run_agent("add two three")


def test_agent_division_by_zero():
    assert "divide by zero" in run_agent("calculate 8 / 0")

def test_power():
    assert power(2, 3) == 8


def test_power_with_zero_exponent():
    assert power(5, 0) == 1


def test_power_rejects_large_exponent():
    with pytest.raises(ValueError, match="Exponent must be"):
        power(2, 101)


def test_power_tool_selection():
    assert select_tool("power 2 3") == "power"


def test_agent_power_command():
    assert run_agent("power 2 3") == "Result: 8"


def test_agent_invalid_power_command():
    assert "Error:" in run_agent("power 2 invalid")