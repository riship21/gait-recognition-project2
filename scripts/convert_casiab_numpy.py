import argparse
import pickle
from pathlib import Path

import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("--stage", choices=["export", "repack"], required=True)
args = parser.parse_args()

root = Path(__file__).resolve().parents[1] / "data/processed"

original = root / "CASIA-B-pkl"
intermediate = root / "CASIA-B-npy-intermediate"
compatible = root / "CASIA-B-pkl-compatible"

if args.stage == "export":
    source = original
    destination = intermediate
    extension = ".pkl"
else:
    source = intermediate
    destination = compatible
    extension = ".npy"

files = sorted(source.rglob(f"*{extension}"))
print(f"Stage: {args.stage}")
print(f"Files found: {len(files)}", flush=True)

if len(files) != 13592:
    raise RuntimeError(f"Expected 13592 files, found {len(files)}")

for index, file in enumerate(files, start=1):
    relative = file.relative_to(source)

    if args.stage == "export":
        target = destination / relative.with_suffix(".npy")
    else:
        target = destination / relative.with_suffix(".pkl")

    target.parent.mkdir(parents=True, exist_ok=True)

    if target.exists():
        raise FileExistsError(f"Refusing to overwrite: {target}")

    if args.stage == "export":
        with file.open("rb") as f:
            data = pickle.load(f)

        if not isinstance(data, np.ndarray):
            raise TypeError(f"Not a NumPy array: {file}")

        if data.ndim != 3 or data.shape[1:] != (64, 64):
            raise ValueError(f"Unexpected shape {data.shape}: {file}")

        if data.dtype != np.uint8:
            raise TypeError(f"Unexpected dtype {data.dtype}: {file}")

        with target.open("wb") as f:
            np.save(f, data, allow_pickle=False)

    else:
        data = np.load(file, allow_pickle=False)

        with target.open("wb") as f:
            pickle.dump(data, f, protocol=4)

    if index % 500 == 0 or index == len(files):
        print(f"Processed {index}/{len(files)}", flush=True)

print("Stage completed successfully!")
