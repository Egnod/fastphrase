import pytest

from fastphrase.core.passphraser import Passphraser
from fastphrase.core.wordlist import Word, WordList


@pytest.fixture
def wordlists() -> list[WordList]:
    return [
        WordList(words=tuple(Word(word) for word in ["apple", "banana", "cherry"]), is_composite=True),
        WordList(words=tuple(Word(word) for word in ["date", "elderberry", "fig"]), is_composite=True),
    ]


@pytest.mark.parametrize(
    "length, expected_length",
    [
        (1, 1),
        (2, 2),
        (3, 3),
    ],
    ids=["length_1", "length_2", "length_3"],
)
def test_get_one(wordlists: list[WordList], length: int, expected_length: int) -> None:
    # Arrange
    passphraser = Passphraser(wordlists)

    # Act
    result = passphraser.get_one(length)

    # Assert
    assert len(result.split(passphraser.DEFAULT_SEPARATOR)) == expected_length


@pytest.mark.parametrize(
    "count, length, expected_count",
    [
        (1, 1, 1),
        (2, 2, 2),
        (3, 3, 3),
    ],
    ids=["count_1_length_1", "count_2_length_2", "count_3_length_3"],
)
def test_get_many(wordlists: list[WordList], count: int, length: int, expected_count: int) -> None:
    # Arrange
    passphraser = Passphraser(wordlists)

    # Act
    result = list(passphraser.get_many(count, length))

    # Assert
    assert len(result) == expected_count
    for passphrase in result:
        assert len(passphrase.split(passphraser.DEFAULT_SEPARATOR)) == length


@pytest.mark.parametrize(
    "expected_words",
    [
        ("apple", "banana", "cherry", "date", "elderberry", "fig"),
        ("apple", "banana", "cherry", "date", "elderberry", "fig"),
    ],
    ids=["single_wordlist", "multiple_wordlists"],
)
def test_get_words(wordlists: list[WordList], expected_words: tuple[str, str]) -> None:
    # Arrange
    passphraser = Passphraser(wordlists)

    # Act
    result = passphraser._get_words(wordlists)

    # Assert
    assert result == expected_words


@pytest.mark.parametrize(
    "separator, expected_separator",
    [
        ("-", "-"),
        ("_", "_"),
    ],
    ids=["default_separator", "custom_separator"],
)
def test_separator(wordlists: list[WordList], separator: str, expected_separator: str) -> None:
    # Arrange
    passphraser = Passphraser(wordlists, separator)

    # Act
    result = passphraser.get_one(2)

    # Assert
    assert expected_separator in result


@pytest.mark.parametrize(
    "length",
    [
        (0),
        (-1),
    ],
    ids=["length_0", "length_negative"],
)
def test_get_one_invalid_length(wordlists: list[WordList], length: int) -> None:
    # Arrange
    passphraser = Passphraser(wordlists)

    # Act & Assert
    with pytest.raises(ValueError):
        passphraser.get_one(length)


@pytest.mark.parametrize(
    "count, length",
    [
        (0, 1),
        (-1, 1),
    ],
    ids=["count_0", "count_negative"],
)
def test_get_many_invalid_count(wordlists: list[WordList], count: int, length: int) -> None:
    # Arrange
    passphraser = Passphraser(wordlists)

    # Act & Assert
    with pytest.raises(ValueError):
        list(passphraser.get_many(count, length))
