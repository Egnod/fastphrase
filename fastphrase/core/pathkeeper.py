from __future__ import annotations

import os
from functools import cache
from pathlib import Path


class PathKeeper:
    """PathKeeper."""

    @classmethod
    @cache
    def get_dict_paths(cls) -> tuple[Path, ...]:
        """get_dict_paths."""
        env_paths = os.getenv(
            "XDG_DATA_DIRS",
            "/usr/local/share/:/usr/share/",
        )
        paths = [Path(path) for path in env_paths.split(":")]
        paths.append(Path.home() / ".local" / "share")
        paths.append(Path(__file__).parent.parent / "data")

        return tuple([path / "dict" for path in paths if (path / "dict").exists()])

    @classmethod
    @cache
    def get_wordlist_paths(cls) -> tuple[Path, ...]:
        """get_wordlist_paths."""
        wordlist_paths = []

        for dict_path in cls.get_dict_paths():
            wordlist_paths.extend(
                [
                    path
                    for path in dict_path.glob("*")
                    if not path.is_symlink() and path.is_file() and (not path.suffix or path.suffix == ".txt")
                ],
            )

        return tuple(wordlist_paths)
