from pathlib import Path

import pytest

from fastphrase.core.wordlist import WordList


@pytest.fixture
def tmp_path(tmpdir: str) -> Path:
    return Path(tmpdir)


@pytest.mark.parametrize(
    "file_content, separator, expected_words, expected_name",
    [
        ("word1\nword2\nword3", "\n", ("word1", "word2", "word3"), "testfile"),
        ("1\tword1\n2\tword2\n3\tword3", "\n", ("word1", "word2", "word3"), "testfile"),
        ("word1,word2,word3", ",", ("word1", "word2", "word3"), "testfile"),
    ],
    ids=["newline_separator", "tab_prefix", "comma_separator"],
)
def test_wordlist_initialization(
    tmp_path: Path, file_content: str, separator: str, expected_words: tuple[str, ...], expected_name: str
) -> None:
    # Arrange
    file_path = tmp_path / "testfile.txt"
    file_path.write_text(file_content)

    # Act
    wordlist = WordList(path=file_path, separator=separator)

    # Assert
    assert set(wordlist.words) == set(expected_words)
    assert wordlist.name == expected_name


@pytest.mark.parametrize(
    "words1, words2, expected_words",
    [
        (("word1", "word2"), ("word3", "word4"), ("word1", "word2", "word3", "word4")),
        (("word1",), ("word2",), ("word1", "word2")),
        ((), ("word1", "word2"), ("word1", "word2")),
    ],
    ids=["two_non_empty", "single_word_each", "first_empty"],
)
def test_wordlist_addition(words1: tuple[str, ...], words2: tuple[str, ...], expected_words: tuple[str, ...]) -> None:
    # Act
    wordlist1 = WordList(words=words1, is_composite=True)
    wordlist2 = WordList(words=words2, is_composite=True)
    combined_wordlist = wordlist1 + wordlist2

    # Assert
    assert combined_wordlist.words == expected_words
    assert combined_wordlist.is_composite


@pytest.mark.parametrize(
    "words, expected_length",
    [
        (("word1", "word2", "word3"), 3),
        (("word1",), 1),
        ((), 0),
    ],
    ids=["three_words", "one_word", "no_words"],
)
def test_wordlist_length(words: tuple[str, ...], expected_length: int) -> None:
    # Act
    wordlist = WordList(words=words, is_composite=True)

    # Assert
    assert len(wordlist) == expected_length


def test_wordlist_no_path_raises_runtime_error() -> None:
    # Act & Assert
    with pytest.raises(RuntimeError, match="Path for wordlist is not defined."):
        WordList()
