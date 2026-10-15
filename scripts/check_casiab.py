from pathlib import Path
import csv
from collections import Counter


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

# This script lives at:
# biometrics-project2-gaitpart/scripts/check_casiab.py

PROJECT2_ROOT = Path(__file__).resolve().parents[1]

PROJECT1_ROOT = PROJECT2_ROOT.parent / "biometrics-project1-gait-recognition"

DATASET_ROOT = (
    PROJECT1_ROOT
    / "data"
    / "raw"
    / "CASIA-B"
    / "GaitDatasetB-silh"
)

OUTPUT_FILE = (
    PROJECT2_ROOT
    / "results"
    / "tables"
    / "casiab_dataset_audit.csv"
)


# ---------------------------------------------------------
# CASIA-B protocol
# ---------------------------------------------------------

SUBJECTS = [f"{i:03d}" for i in range(1, 125)]

CONDITIONS = [
    "nm-01",
    "nm-02",
    "nm-03",
    "nm-04",
    "nm-05",
    "nm-06",
    "bg-01",
    "bg-02",
    "cl-01",
    "cl-02",
]

VIEWS = [
    "000",
    "018",
    "036",
    "054",
    "072",
    "090",
    "108",
    "126",
    "144",
    "162",
    "180",
]


def get_split(subject):
    """
    GaitPart CASIA-B split:

    Train: subjects 001-074
    Test:  subjects 075-124
    """

    if int(subject) <= 74:
        return "train"

    return "test"


def main():

    # -----------------------------------------------------
    # Verify dataset exists
    # -----------------------------------------------------

    if not DATASET_ROOT.exists():
        print("ERROR: CASIA-B dataset was not found.")
        print()
        print("Expected location:")
        print(DATASET_ROOT)
        return

    print()
    print("Dataset root:")
    print(DATASET_ROOT)
    print()

    rows = []

    missing_sequences = 0
    empty_sequences = 0
    short_nonempty_sequences = 0

    # -----------------------------------------------------
    # Audit every subject / condition / view
    # -----------------------------------------------------

    for subject in SUBJECTS:

        split = get_split(subject)

        for condition in CONDITIONS:

            for view in VIEWS:

                sequence_path = (
                    DATASET_ROOT
                    / subject
                    / condition
                    / view
                )

                exists = sequence_path.exists()

                if exists:
                    frames = list(sequence_path.glob("*.png"))
                    frame_count = len(frames)
                else:
                    frame_count = 0

                # Folder does not exist
                if not exists:
                    missing_sequences += 1

                # Folder exists but contains no PNG frames
                if exists and frame_count == 0:
                    empty_sequences += 1

                # Folder contains frames, but fewer than 15
                if exists and 0 < frame_count < 15:
                    short_nonempty_sequences += 1

                rows.append(
                    {
                        "subject": subject,
                        "split": split,
                        "condition": condition,
                        "view": view,
                        "exists": exists,
                        "frame_count": frame_count,
                        "empty": exists and frame_count == 0,
                        "less_than_15_frames": frame_count < 15,
                        "less_than_30_frames": frame_count < 30,
                    }
                )

    # -----------------------------------------------------
    # Save CSV
    # -----------------------------------------------------

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=[
                "subject",
                "split",
                "condition",
                "view",
                "exists",
                "frame_count",
                "empty",
                "less_than_15_frames",
                "less_than_30_frames",
            ],
        )

        writer.writeheader()
        writer.writerows(rows)

    # -----------------------------------------------------
    # Summary calculations
    # -----------------------------------------------------

    expected_sequences = (
        len(SUBJECTS)
        * len(CONDITIONS)
        * len(VIEWS)
    )

    total_under_15 = sum(
        1
        for row in rows
        if row["frame_count"] < 15
    )

    train_under_15 = sum(
        1
        for row in rows
        if (
            row["split"] == "train"
            and row["frame_count"] < 15
        )
    )

    test_under_15 = sum(
        1
        for row in rows
        if (
            row["split"] == "test"
            and row["frame_count"] < 15
        )
    )

    # Count affected sequences per subject
    affected_subjects = Counter(
        row["subject"]
        for row in rows
        if row["frame_count"] < 15
    )

    # -----------------------------------------------------
    # Print results
    # -----------------------------------------------------

    print("CASIA-B Dataset Audit")
    print("---------------------")

    print(f"Subjects expected:             {len(SUBJECTS)}")
    print("Training subjects:             74")
    print("Testing subjects:              50")
    print(f"Expected sequences:            {expected_sequences}")
    print()

    print(f"Missing sequence folders:      {missing_sequences}")
    print(f"Empty sequences:               {empty_sequences}")
    print(
        f"Non-empty sequences <15:       "
        f"{short_nonempty_sequences}"
    )
    print(f"Total sequences <15 frames:    {total_under_15}")
    print()

    print(f"Training sequences <15:        {train_under_15}")
    print(f"Testing sequences <15:         {test_under_15}")

    print()
    print("Most affected subjects")
    print("----------------------")

    for subject, count in affected_subjects.most_common():
        print(f"Subject {subject}: {count}")

    print()
    print("Audit saved to:")
    print(OUTPUT_FILE)
    print()


if __name__ == "__main__":
    main()