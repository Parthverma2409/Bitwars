"""Virtual file pointer implementation."""

import re
import typing as t
from enum import Enum
from pathlib import Path

import typing_extensions as te

from composio.utils.logging import WithLogger


SCROLL_UP = "up"
SCROLL_DOWN = "down"

SCOPE_FILE = "file"
SCOPE_WINDOW = "window"


class ScrollDirection(Enum):
    UP = "up"
    DOWN = "down"

    def __mul__(self, lines: int) -> int:
        """Multiply the window by scroll direction."""
        return lines * (-1 if self.value == "up" else 1)


class FileOperationScope(str, Enum):
    FILE = "file"
    WINDOW = "window"


class Match(te.TypedDict):
    """Match object."""

    start: int
    end: int
    lineno: int
    content: str


class TextReplacement(te.TypedDict):
    """Text replacement response."""

    replaced_with: str
    replaced_text: str
    error: te.NotRequired[str]


class File(WithLogger):
    """File object for file manager."""

    _start: int
    _end: int

    def __init__(
        self,
        path: Path,
        workdir: Path,
        window: t.Optional[int] = None,
    ) -> None:
        """
        Initialize file object

        :param path: Path to file.
        :param workdir: Current working directory.
        :param window: Size of the view window, default is 100.
        """
        super().__init__()
        self.path = path
        self.workdir = workdir

        # View window
        self._start = 0
        self._end = window or 100
        self._window = window or 100

    def scroll(
        self,
        lines: t.Optional[int] = None,
        direction: t.Optional[ScrollDirection] = None,
    ) -> None:
        """
        Scroll to given number of lines.

        :param lines: Number of lines to scroll.
        :param direction: Direction of scrolling.
        :return: None
        """
        direction = direction or ScrollDirection.DOWN
        lines = direction * (lines or self._window)
        self._start += lines
        self._end += lines

    def goto(self, line: int) -> None:
        """
        Go to the given line number.

        :param line: Number of lines to scroll.
        :return: None
        """
        self._start = line
        self._end = self._start + self._window

    def _find(self, buffer: str, pattern: str, lineno: int) -> t.List[Match]:
        """Find the occurences for given pattern in the buffer."""
        matches: t.List[Match] = []
        for match in re.finditer(pattern=pattern, string=buffer):
            start = match.start()
            end = match.end()
            matches.append(
                {
                    "content": match.string[start:end],
                    "end": end,
                    "start": start,
                    "lineno": lineno,
                }
            )
        return matches

    def _find_window(self, pattern: str) -> t.List[Match]:
        """Find in the current window."""
        offset = self._start
        matches = []
        for lineno, line in enumerate(self._iter_window()):
            matches += self._find(
                buffer=line,
                pattern=pattern,
                lineno=lineno + offset,
            )
        return matches

    def _find_file(
        self,
        pattern: str,
    ) -> t.List[Match]:
        """Find in the whole file."""
        matches = []
        for lineno, line in enumerate(self._iter_file()):
            matches += self._find(
                buffer=line,
                pattern=pattern,
                lineno=lineno,
            )
        return matches

    def find(
        self,
        pattern: str,
        scope: t.Optional[FileOperationScope] = None,
    ) -> t.List[Match]:
        """
        Find pattern in the given file.

        :param pattern: Pattern to search for
        :param scope: Scope for the search, choose between `file` and `windows`.
            if you choose `file`, the search will be performed across the file else
            the search will be performed over the current view window.
        :return: List of matches found for the given pattern
        """
        scope = scope or FileOperationScope.FILE
        if scope == SCOPE_FILE:
            return self._find_file(pattern=pattern)
        return self._find_window(pattern=pattern)

    def _iter_window(self) -> t.Iterable[str]:
        """Iter data from the current window."""
        cursor = 0
        with self.path.open("r") as fp:
            while cursor < self._start:
                _ = fp.readline()
                cursor += 1
            while cursor < self._end:
                yield fp.readline()
                cursor += 1

    def _iter_file(self) -> t.Iterable[str]:
        """Iter data from the current file."""
        with self.path.open(mode="r") as fp:
            while True:
                line = fp.readline()
                if not line:
                    break
                yield line

    def iter(self, scope: t.Optional[FileOperationScope] = None) -> t.Iterable[str]:
        """Iter data from the current window."""
        scope = scope or FileOperationScope.FILE
        if scope == FileOperationScope.WINDOW:
            return self._iter_window()
        return self._iter_file()

    def read(self) -> str:
        """Read data from file."""
        cursor = 0
        buffer = ""
        with self.path.open("r") as fp:
            while cursor < self._start:
                _ = fp.readline()
                cursor += 1
            while cursor < self._end:
                buffer += fp.readline()
                cursor += 1
        return buffer

    def write(
        self,
        text: str,
        start: int,
        end: int,
        scope: t.Optional[FileOperationScope] = None,
    ) -> TextReplacement:
        """
        Write given content to file

        :param text: Content to write to file.
        :param scope: Scope of the file operation
        :param start: Line number to start the edit at
        :param end: Line number where to end the edit
        :return: Replaced text
        """
        scope = scope or FileOperationScope.FILE

        cursor = 0
        buffer = ""
        replaced = ""
        with self.path.open(mode="r") as fp:
            if scope == FileOperationScope.WINDOW:
                while cursor < self._start:
                    _ = fp.readline()
                    cursor += 1
                cursor = 0

            while cursor < (start - 1):
                buffer += fp.readline()
                cursor += 1

            while cursor < (end - 1):
                replaced += fp.readline()
                cursor += 1

            buffer += text
            while True:
                line = fp.readline()
                if not line:
                    break
                buffer += line

        self.path.write_text(data=buffer, encoding="utf-8")
        return {"replaced_text": replaced, "replaced_with": text}

    def replace(self, string: str, replacement: str) -> TextReplacement:
        """Replace given string with replacement."""
        content = self.path.read_text(encoding="utf-8")
        update = re.sub(
            pattern=re.escape(string),
            repl=replacement,
            string=content,
        )
        if content == update:
            return {
                "replaced_text": "",
                "replaced_with": "",
                "error": "Error replacing given string, string not found",
            }
        self.path.write_text(update, encoding="utf-8")
        return {"replaced_text": string, "replaced_with": replacement}

    def __str__(self) -> str:
        """String representation."""
        return f"File(name={self.path})"