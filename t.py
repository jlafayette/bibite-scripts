"""Scratch file for testing out ideas."""
import shutil
import zipfile
import random
from pathlib import Path

import numpy as np

import bibite_scripts as bb

root = Path(__file__).absolute().parent


def delete(path: Path):
    if path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def count_autosaves():
    autosaves = Path.home() / r"AppData\LocalLow\The Bibites\The Bibites\autosaves"
    count = 0
    for f in autosaves.iterdir():
        if f.name.endswith(".zip"):
            count += 1
    return count


def unzip_save(src: Path, dst: Path) -> None:
    if dst.exists():
        print(f"Deleting folder and contents {dst.name}...")
        shutil.rmtree(dst)
    with zipfile.ZipFile(src, 'r') as zip_ref:
        zip_ref.extractall(dst)


def main():
    src = root / "world_20220916021433__4_21_hrs.zip"
    dst = root / f"{src.stem}"
    # if not dst.exists():
    delete(dst)
    unzip_save(src, dst)

    # read data from all Bibites in the simulation
    # bibites = []
    # raw_0 = b''
    for bf in (dst / "bibites").iterdir():
        # raw_0 = bf.read_bytes()
        # (root / "z_raw_orig.bb8").write_bytes(raw_0)
        # data = bb.bb8.read(bf)
        # data["genes"]["genes"]["BrainMutationSigma"] = 0.2
        # data["genes"]["genes"]["BrainAverageMutation"] = 2.0
        # bb.bb8.write(data, bf)
        # bibites.append(data)

        # bb.bb8.edit(bf, {b"BrainMutationSigma": 0.2, b"BrainAverageMutation": 2.0})
        pass
        # break

    # write archive
    delete((root / f"{dst.stem}__1.zip"))
    shutil.make_archive(f"{dst.stem}__1", 'zip', dst)

    return

    print("Sigma:")
    a = np.array([x["genes"]["genes"]["BrainMutationSigma"] for x in bibites])
    print(np.min(a), np.max(a), np.median(a), np.mean(a))
    print(a[0])

    print("Average:")
    a = np.array([x["genes"]["genes"]["BrainAverageMutation"] for x in bibites])
    print(np.min(a), np.max(a), np.median(a), np.mean(a))
    print(a[0])
    # Save an edited Bibite
    b = bibites[0]
    print(b["genes"]["genes"]["BrainMutationSigma"])
    print(b["genes"]["genes"]["BrainAverageMutation"])

    bb.bb8.write(b, (root / "z_orig.bb8"))
    # raw_0_2 = (root / "z_orig.bb8").read_bytes()

    b["genes"]["genes"]["BrainMutationSigma"] = 0.2
    b["genes"]["genes"]["BrainAverageMutation"] = 2.0
    bb.bb8.write(b, (root / "z_NEW.bb8"))


def resave():
    import json
    f = root / "MyBibite.bb8"
    c = f.read_text()
    print(c[:4])
    data = json.loads(c)
    # print(data["genes"])
    f2 = root / "MyBibite2.bb8"
    s = json.dumps(data, separators=(',', ':'))
    f2.write_bytes(s.encode('utf-8'))

    # from archive
    f = root / "world_20220916021433__4_21_hrs/bibites/bibite_1.bb8"
    c = f.read_bytes()
    print(c[:4])


def t():
    src = root / "world_autosave_20220917102459.zip"
    dst = root / f"{src.stem}"
    if dst.exists():
        print(f"Deleting folder and contents {dst.name}")
        shutil.rmtree(dst)
    with zipfile.ZipFile(src, 'r') as zin:
        # zip_ref.extractall(dst)

        # write archive
        dst_zip = root / f"{dst.stem}__1.zip"
        if dst_zip.exists():
            print(f"Deleting existing zip {dst_zip.name}")
            dst_zip.unlink()
        with zipfile.ZipFile(dst_zip, 'w') as zout:
            zout.comment = zin.comment  # preserve the comment
            for item in zin.infolist():
                contents = zin.read(item.filename)

                if item.filename.endswith(".bb8"):
                    new_genes = {
                        "BrainMutationSigma": random.uniform(0.15, 0.4),
                        "BrainAverageMutation": random.uniform(1.5, 4.0),
                    }
                    try:
                        contents = bb.bb8.edit_contents(contents, item.filename, new_genes)
                    except KeyError as err:
                        print(f"failed to update {item.filename} with {err.__class__.__name__}: {err}")
                zout.writestr(item, contents)


def t2():
    src = root / "world_autosave_20220917102459.zip"

    def make_fn() -> bb.archive.EditFunc:
        def f(contents: bytes) -> bytes:
            new_genes = {
                "BrainMutationSigma": random.uniform(0.15, 0.4),
                "BrainAverageMutation": random.uniform(1.5, 4.0),
            }
            return bb.bb8.edit_contents(contents, new_genes)
        return f

    bb.archive.edit(src, make_fn())


if __name__ == "__main__":
    # main()
    # resave()
    t2()
