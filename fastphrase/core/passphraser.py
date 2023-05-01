from __future__ import annotations

import random
import typing as t

if t.TYPE_CHECKING:
    from fastphrase.core.wordlist import Word, WordList


class Passphraser:
    """Passphraser."""

    DEFAULT_SEPARATOR = "-"

    def __init__(self, wordlists: list[WordList], separator: str = DEFAULT_SEPARATOR):
        self._words = self._get_words(wordlists)
        self._separator = separator
        self._words_count = len(self._words)
        self._random = random.SystemRandom()

    def _get_random_words(self, count: int) -> t.Iterator[Word]:
        """Generator of random words.

        Args:
            count (int): count of random words

        Returns:
            t.Iterator[Word]: iterator of random words

        Yields:
            Iterator[t.Iterator[Word]]: random word
        """

        for _ in range(count):
            word_idx = self._random.randint(0, self._words_count - 1)
            yield self._words[word_idx]

    def get_one(self, length: int) -> str:
        """Generate single random passphrase.

        Args:
            length (int): length (count) of the random passphrase

        Returns:
            str: passphrase
        """
        words: list[Word] = []

        for word in self._get_random_words(length):
            words.append(word)

        return f"{self._separator}".join(words)

    def get_many(self, count: int, length: int) -> t.Iterator[str]:
        """Generator many passphrases.

        Args:
            count (int): count of passphrase
            length (int): length of words to generate passphrase

        Returns:
            t.Iterator[str]: generator

        Yields:
            Iterator[t.Iterator[str]]: passphrase
        """

        for _ in range(count):
            yield self.get_one(length=length)

    def _get_words(self, wordlists: list[WordList]) -> tuple[Word, ...]:
        """_get_words.

        Args:
            wordlists (list[WordList]): WordList

        Returns:
            tuple[Word, ...]: words
        """
        wordlist = wordlists[0]

        for wl in wordlists:
            wordlist += wl

        return wordlist.words
