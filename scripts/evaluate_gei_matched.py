
from pathlib import Path
import sys
import csv
import json
import numpy as np

# Resolve both repositories without modifying Project 1.
PROJECT2 = Path(__file__).resolve().parents[1]
PROJECT1 = PROJECT2.parent / "biometrics-project1-gait-recognition"

sys.path.insert(0, str(PROJECT1 / "src"))
from gei import generate_gei

DATA = PROJECT1 / "data/raw/CASIA-B/GaitDatasetB-silh"
OUTPUT = PROJECT2 / "results/tables"

VIEW = "090"
GALLERY = ["nm-01", "nm-02", "nm-03", "nm-04"]
PROBE = ["nm-05", "nm-06"]
SUBJECTS = [f"{i:03d}" for i in range(75, 125)]


def feature(subject, sequence):
    path = DATA / subject / sequence / VIEW
    gei, frames = generate_gei(path)
    return gei.astype(np.float32).flatten() / 255.0, frames


def main():
    if not DATA.is_dir():
        raise FileNotFoundError(DATA)

    gallery_features = []
    gallery_labels = []
    probes = []
    excluded = []

    for subject in SUBJECTS:
        samples = {}
        try:
            for sequence in GALLERY + PROBE:
                samples[sequence] = feature(subject, sequence)
        except (FileNotFoundError, ValueError) as error:
            excluded.append({
                "subject": subject,
                "reason": str(error)
            })
            continue

        for sequence in GALLERY:
            gallery_features.append(samples[sequence][0])
            gallery_labels.append(subject)

        for sequence in PROBE:
            vector, frames = samples[sequence]
            probes.append((subject, sequence, vector, frames))

    if not gallery_features or not probes:
        raise RuntimeError("No valid gallery/probe data found.")

    gallery_features = np.stack(gallery_features)
    gallery_labels = np.array(gallery_labels)

    results = []
    correct = 0

    for subject, sequence, vector, frames in probes:
        distances = np.linalg.norm(
            gallery_features - vector, axis=1
        )
        index = int(np.argmin(distances))
        predicted = str(gallery_labels[index])
        matched = predicted == subject
        correct += int(matched)

        results.append({
            "true_subject": subject,
            "probe_sequence": sequence,
            "view": VIEW,
            "frames": frames,
            "predicted_subject": predicted,
            "distance": float(distances[index]),
            "correct": matched,
        })

    accuracy = 100 * correct / len(results)

    OUTPUT.mkdir(parents=True, exist_ok=True)

    with (OUTPUT / "gei_matched_predictions.csv").open(
        "w", newline=""
    ) as f:
        writer = csv.DictWriter(
            f, fieldnames=results[0].keys()
        )
        writer.writeheader()
        writer.writerows(results)

    summary = {
        "method": "Project 1 GEI Euclidean",
        "view": VIEW,
        "subjects_requested": len(SUBJECTS),
        "subjects_included": len(probes) // len(PROBE),
        "subjects_excluded": excluded,
        "gallery_sequences": GALLERY,
        "probe_sequences": PROBE,
        "correct": correct,
        "total": len(results),
        "rank1_percent": accuracy,
    }

    with (OUTPUT / "gei_matched_summary.json").open("w") as f:
        json.dump(summary, f, indent=2)

    print("GEI Held-Out Baseline")
    print("---------------------")
    print("Subjects included:", summary["subjects_included"])
    print("Subjects excluded:", len(excluded))
    print("Correct:", correct)
    print("Total probes:", len(results))
    print(f"Rank-1 accuracy: {accuracy:.2f}%")
    print("Results saved to:", OUTPUT)


if __name__ == "__main__":
    main()
