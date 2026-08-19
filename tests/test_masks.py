import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("1234567890123456", "1234 56** **** 3456"),
        ("0000111122223333", "0000 11** **** 3333"),
        ("9876543210987654", "9876 54** **** 7654"),
    ],
)
def test_get_mask_card_number(card_number: str, expected: str) -> None:
    """Проверяет правильность маскирования номера карты."""
    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize(
    "card_number",
    [
        "123456789012345",
        "12345678901234567",
        "",
        "1234",
    ],
)
def test_get_mask_card_number_invalid(card_number: str) -> None:
    """Проверяет ошибку при неправильной длине номера карты."""
    with pytest.raises(ValueError):
        get_mask_card_number(card_number)


@pytest.mark.parametrize(
    "account_number, expected",
    [
        ("1234", "**1234"),
        ("12345678", "**5678"),
        ("12345678901234567890", "**7890"),
    ],
)
def test_get_mask_account(account_number: str, expected: str) -> None:
    """Проверяет правильность маскирования номера счета."""
    assert get_mask_account(account_number) == expected


@pytest.mark.parametrize(
    "account_number",
    [
        "",
        "1",
        "12",
        "123",
    ],
)
def test_get_mask_account_invalid(account_number: str) -> None:
    """Проверяет ошибку для слишком короткого номера счета."""
    with pytest.raises(ValueError):
        get_mask_account(account_number)
