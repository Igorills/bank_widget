import pytest
from _pytest.capture import CaptureFixture

from src.decorators import log

# Тестирование вывода в КОНСОЛЬ (filename=None)


def test_log_console_success(capsys: CaptureFixture[str]) -> None:
    """Проверка логирования успешного выполнения функции в консоль."""

    @log()
    def add(x: int, y: int) -> int:
        return x + y

    result = add(2, 3)
    assert result == 5

    captured = capsys.readouterr()
    assert captured.out == "add ok\n"


def test_log_console_error(capsys: CaptureFixture[str]) -> None:
    """Проверка логирования ошибки функции в консоль."""

    @log()
    def divide(x: int, y: int) -> float:
        return x / y

    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    captured = capsys.readouterr()
    assert "divide error: ZeroDivisionError. Inputs: (10, 0), {}\n" in captured.out


# Тестирование записи в ФАЙЛ (filename передан)


def test_log_file_success(tmp_path: pytest.TempPathFactory) -> None:
    """Проверка записи успешного выполнения функции в файл."""
    log_file = tmp_path / "test_log.txt"  # type: ignore[operator]

    @log(filename=str(log_file))
    def multiply(x: int, y: int) -> int:
        return x * y

    result = multiply(3, 4)
    assert result == 12

    with open(log_file, "r", encoding="utf-8") as f:
        content = f.read()

    assert content == "multiply ok\n"


def test_log_file_error(tmp_path: pytest.TempPathFactory) -> None:
    """Проверка записи информации об ошибке функции в файл."""
    log_file = tmp_path / "test_error_log.txt"  # type: ignore[operator]

    @log(filename=str(log_file))
    def raise_value_error(val: str) -> int:
        return int(val)

    with pytest.raises(ValueError):
        raise_value_error("abc")

    with open(log_file, "r", encoding="utf-8") as f:
        content = f.read()

    assert "raise_value_error error: ValueError. Inputs: ('abc',), {}\n" in content


def test_log_file_append(tmp_path: pytest.TempPathFactory) -> None:
    """Проверка дозаписи нескольких логов в один файл."""
    log_file = tmp_path / "append_log.txt"  # type: ignore[operator]

    @log(filename=str(log_file))
    def greet(name: str) -> str:
        return f"Hello, {name}"

    greet("Alice")
    greet("Bob")

    with open(log_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    assert lines == ["greet ok\n", "greet ok\n"]
