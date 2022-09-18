import json
from pathlib import Path
from typing import Any


JsonData = dict[str, Any]


class Bb8ReadError(Exception):
    """Error reading from bb8 file."""
    pass


def read(f: Path) -> JsonData:
    """Read bb8 file and return data."""
    contents = f.read_bytes()
    return _read2(contents, f.name)


def _read2(contents: bytes, name: str) -> JsonData:
    """Read contents of a bb8 file into dict."""
    try:
        return json.loads(contents)
    except ValueError:
        try:
            # trim off bb8 prefix "ï»¿"
            # this prefix is only included on files within a saved game zip archive
            return json.loads(contents[3:])
        except Exception as err:
            raise Bb8ReadError(f"failed to open {name} with {err.__class__.__name__}: {err}") from None


def edit(f: Path, genes: dict[str, float]) -> None:
    """Edit the genes of a Bibite file."""
    contents = f.read_bytes()
    contents = edit_contents(contents, f.name, genes)
    f.write_bytes(contents)


def edit_contents(contents: bytes, name: str, genes: dict[str, float]) -> bytes:
    """Return new contents after editing the genes of a Bibite.

    This acts on the contents of a file.  This may not be necessary since it would
    be easier to edit the json and then write that back, but that method seems to
    corrupt bb8 files read from a save zip file.

    """
    data = _read2(contents, name)

    to_replace = {}
    for k, new_v in genes.items():
        # breakpoint()
        if k not in data["genes"]["genes"].keys():
            print(f"{k} not in genes ({name})")
            continue
        v = data["genes"]["genes"][k]
        # example b'"BrainMutationSigma":0.0806809142,'
        to_replace[k] = b'"' + k.encode() + b'":' + str(v).encode() + b','

    for k, old_bytes in to_replace.items():
        new_bytes = b'"' + k.encode() + b'":' + str(genes[k]).encode() + b','
        contents = contents.replace(old_bytes, new_bytes, 1)
    return contents


def write(data: JsonData, f: Path) -> None:
    """Write data back to bb8 format.

    Needs testing to confirm that this method does not corrupt the file.

    """

    # is this prefix is even needed?
    # contents = f"ï»¿{json.dumps(data, separators=(',', ':'))}"

    f.write_text(json.dumps(data, separators=(',', ':')))
