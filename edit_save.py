import random
from pathlib import Path

import bibite_scripts as bb


root = Path(__file__).absolute().parent


def main():
    src = root / "world_autosave_20220917102459.zip"

    def make_bb8_edit_fn() -> bb.archive.EditFunc:
        def fn(contents: bytes) -> bytes:
            new_genes = {
                "BrainMutationSigma": random.uniform(0.15, 0.4),
                "BrainAverageMutation": random.uniform(1.5, 4.0),
            }
            return bb.bb8.edit_contents(contents, new_genes)
        return fn

    bb.archive.edit(src, make_bb8_edit_fn())


if __name__ == "__main__":
    main()
