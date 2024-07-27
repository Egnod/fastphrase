from unittest.mock import MagicMock, patch

import pytest

from fastphrase.cli.app import App


@pytest.mark.parametrize(
    "args, expected_output",
    [
        (["--version"], "1.0.0\n"),
        (["--wordlists"], "wordlist1\nwordlist2\n"),
        (["--count", "2", "--length", "3", "--separator", "-", "--wordlists-names", "wordlist1"], "phrase1\nphrase2\n"),
        (
            ["--count", "1", "--length", "1", "--separator", "-", "--wordlists-names", "nonexistent"],
            "Wordlist nonexistent is unavailable!\n",
        ),
    ],
    ids=["version", "wordlists", "generate_passphrases", "unavailable_wordlist"],
)
def test_app(args: list[str], expected_output: str) -> None:
    # Arrange
    app = App()
    with patch("fastphrase.cli.app.__version__", "1.0.0"):
        with patch(
            "fastphrase.cli.app.PathKeeper.get_wordlist_paths",
            return_value=[MagicMock(stem="wordlist1"), MagicMock(stem="wordlist2")],
        ):
            with patch("fastphrase.cli.app.WordList"):
                with patch("fastphrase.cli.app.Passphraser.get_many", return_value=["phrase1", "phrase2"]):
                    with patch("builtins.print") as mock_print:

                        # Act
                        with patch("sys.argv", ["app.py"] + args):
                            app.start()

                        # Assert
                        mock_print.assert_called_with(expected_output.strip())


@pytest.mark.parametrize(
    "args",
    [
        ["--count", "-1"],
        ["--length", "-1"],
    ],
    ids=["count_negative", "length_negative"],
)
def test_app_invalid_args(args: list[str]) -> None:
    # Arrange
    app = App()
    with patch("builtins.print") as mock_print:
        # Act
        with patch("sys.argv", ["app.py"] + args):
            app.start()

        # Assert
        mock_print.assert_called_once_with("Count and length must be greater than or equal to 1")
