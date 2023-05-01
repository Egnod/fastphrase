import argparse

from fastphrase.__about__ import __project__, __version__
from fastphrase.core.passphraser import Passphraser
from fastphrase.core.pathkeeper import PathKeeper
from fastphrase.core.wordlist import WordList


class App:
    """App entrypoint."""

    def __init__(self) -> None:
        self._parser = argparse.ArgumentParser(prog=__project__)

    def start(self) -> None:
        self._set_commands()

        command = self._parser.parse_args()

        if command.version:
            self.version()

        elif command.wordlists:
            self.wordlists()

        else:
            self._root(command.count, command.length, command.separator, command.wordlists_names)

    def _set_commands(self) -> None:
        self._parser.add_argument("--version", "-V", action="store_true", help="Print fastphrase version.")
        self._parser.add_argument(
            "--wordlists",
            "-W",
            action="store_true",
            help="Print wordlists (installed in system and fastprase standard).",
        )

        self._parser.add_argument("--count", "-c", type=int, default=1, help="Number of passphrases for generate.")
        self._parser.add_argument(
            "--length",
            "-l",
            type=int,
            default=1,
            help="Length (in words) of generated passphrase.",
        )
        self._parser.add_argument(
            "--separator",
            "-s",
            type=str,
            default="-",
            help="Symbol for separating words in passphrase.",
        )
        self._parser.add_argument(
            "--wordlists-names",
            "-w",
            type=str,
            default="bip0039,eff_short1,eff_short2",
            help=(
                "Concrete wordlists for passphrase generate (separated by commas). Default:"
                " bip0039,eff_short1,eff_short2"
            ),
        )

    def version(self) -> None:
        """Show version."""
        print(__version__)

    def wordlists(self) -> None:
        """Show wordlists names."""
        print("\n".join(p.stem for p in PathKeeper.get_wordlist_paths()))

    def _root(self, count: int = 1, length: int = 5, separator: str = "-", wordlists_names: str = "") -> None:
        """Generate passphrase."""

        use_wordlists = set()
        available_wordlists = {p.stem for p in PathKeeper.get_wordlist_paths()}

        if wordlists_names:
            for wl in wordlists_names.split(","):
                if wl not in available_wordlists:
                    print(f"Wordlist {wl} is unavailable!")
                    return None

                use_wordlists.add(wl)
        else:
            use_wordlists = available_wordlists

        wordlists = [WordList(p) for p in PathKeeper.get_wordlist_paths() if p.stem in use_wordlists]

        generator = Passphraser(wordlists=wordlists, separator=separator)

        for phrase in generator.get_many(count=count, length=length):
            print(phrase)
