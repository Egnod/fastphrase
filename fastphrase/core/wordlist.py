from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path


class Word(str):
    pass


@dataclass(frozen=True)
class WordList:
    """WordList."""

    path: Path | None = field(default=None)
    name: str | None = field(default=None)
    separator: str = field(default="\n")
    words: tuple[Word, ...] = field(default_factory=tuple, repr=False)
    is_composite: bool = field(default=False)

    def __post_init__(self) -> None:
        """__post_init__

        Raises:
            RuntimeError: _description_
        """
        if self.path:
            words = set()

            for word in self.path.read_text().split(self.separator):
                word = re.sub(r"^[0-9]+\t", "", word)

                if word:
                    words.add(word)

            object.__setattr__(self, "words", tuple(words))
            object.__setattr__(self, "name", self.path.stem)

        elif not self.is_composite:
            raise RuntimeError("Path for wordlist is not defined.")

    def __len__(self) -> int:
        """Length of wordlist.

        Returns:
            int: length
        """
        return len(self.words)

    def __add__(self, __value: WordList) -> WordList:
        """__add__

        Args:
            __value (WordList): _description_

        Returns:
            WordList: _description_
        """
        return WordList(words=tuple(list(self.words) + list(__value.words)), is_composite=True)
