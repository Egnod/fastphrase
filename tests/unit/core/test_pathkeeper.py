import os
import typing as t
from pathlib import Path
from unittest.mock import patch

import pytest

from fastphrase.core.pathkeeper import PathKeeper


@pytest.fixture
def mock_env_paths() -> t.Iterator[None]:
    with patch.dict(os.environ, {"XDG_DATA_DIRS": "/mock/share/:/mock/usr/share/"}):
        yield


@pytest.fixture
def mock_path_exists() -> t.Iterator[None]:
    with patch("pathlib.Path.exists", return_value=True):
        yield


@pytest.fixture
def mock_glob() -> t.Iterator[None]:
    with patch("pathlib.Path.glob", return_value=[Path("/mock/share/dict/wordlist.txt")]):
        yield


@pytest.mark.parametrize(
    "env_paths, excepted_in",
    [
        ("/mock/share/:/mock/usr/share/", True),
        ("/empty/path", False),
    ],
    ids=["multiple_paths", "empty_path"],
)
def test_get_dict_paths(
    mock_env_paths: t.Iterator[None], mock_path_exists: t.Iterator[None], env_paths: str, excepted_in: bool
) -> None:
    # Arrange
    with patch.dict(os.environ, {"XDG_DATA_DIRS": env_paths}):
        with patch("pathlib.Path.is_dir", return_value=excepted_in):
            with patch("pathlib.Path.is_file", return_value=excepted_in):
                with patch("pathlib.Path.iterdir", return_value=[""] if excepted_in else []):
                    # Act
                    result = PathKeeper.get_dict_paths()

    # Assert
    for env_path in env_paths.split(":"):
        path = Path(env_path)

        assert (path / "dict" in result) if excepted_in else path / "dict" not in result
