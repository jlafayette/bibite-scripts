import zipfile
from pathlib import Path
from typing import TypeAlias, Callable, Optional


EditFunc: TypeAlias = Callable[[bytes], bytes]


def edit(src: Path, bb8_fn: EditFunc, dst_zip: Optional[Path] = None):
    """Edit a saved archive (.zip) file.

    Args:
        src: The source archive to edit (creates a copy, will not overwrite).
        bb8_fn: A function to run on the content of each .bb8 Bibite file in the save.
            This needs to take the contents of the file as its argument, and return
            the new contents for the .bb8 file (both in bytes).
        dst_zip: Path to save the modified save file. If None, this will be named
            after the src zip, but with a unique version number appended.

    """
    if dst_zip is None:
        dst_zip = _version_up(src)
    if dst_zip.exists():
        print(f"Deleting existing zip {dst_zip.name}")
        dst_zip.unlink()

    with zipfile.ZipFile(src, 'r') as zin:
        with zipfile.ZipFile(dst_zip, 'w') as zout:
            zout.comment = zin.comment
            for item in zin.infolist():
                contents = zin.read(item.filename)
                if item.filename.endswith(".bb8"):
                    contents = bb8_fn(contents)
                zout.writestr(item, contents)


class ArchiveVersioningError(Exception):
    pass


def _version_up(path: Path) -> Path:
    """Try to return a path with versioned up filename.

    For example: mysave.zip -> mysave__1.zip
    But if mysave__1.zip already exists, then mysave__2.zip, and so on up to __999

    """
    for i in range(1, 1000):
        p = path.parent / f"{path.stem}__{i}{path.suffix}"
        if not p.exists():
            return p
    low = f"{path.stem}__{1}{path.suffix}"
    high = f"{path.stem}__{999}{path.suffix}"
    raise ArchiveVersioningError(f"Failed to automatically version file, {low} .. {high} already exist")
