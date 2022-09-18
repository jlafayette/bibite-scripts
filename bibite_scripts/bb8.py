import json
from pathlib import Path
from typing import Any, TypeAlias


JsonData: TypeAlias = dict[str, Any]


class Bb8ReadError(Exception):
    """Error reading from bb8 file."""
    pass


def read(f: Path) -> JsonData:
    """Read bb8 file and return data."""
    contents = f.read_bytes()
    return json.loads(contents)


def edit(f: Path, genes: dict[str, float]) -> None:
    """Edit the genes of a Bibite file."""
    contents = f.read_bytes()
    contents = edit_contents(contents, genes)
    f.write_bytes(contents)


def edit_contents(contents: bytes, genes: dict[str, float]) -> bytes:
    """Return new contents after editing the genes of a Bibite."""
    data = json.loads(contents)
    data["genes"]["genes"].update(genes)
    return json.dumps(data, separators=(",", ":")).encode()


def write(data: JsonData, f: Path) -> None:
    """Write data back to bb8 format.

    Needs testing to confirm that this method does not corrupt the file.

    """
    f.write_text(json.dumps(data, separators=(',', ':')))
