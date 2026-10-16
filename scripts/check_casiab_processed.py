from pathlib import Path
import csv


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

PROJECT2_ROOT = Path(__file__).resolve().parents[1]

PROJECT1_ROOT = (
    PROJECT2_ROOT.parent
    / "biometrics-project1-gait-recognition"
)

RAW_ROOT = (
    PROJECT1_ROOT
    / "data"
    / "raw"
    / "CASIA-B"
    / "GaitDatasetB-silh"
)

PROCESSED_ROOT = (
    PROJECT2_ROOT
    / "data"
    / "processed"
    / "CASIA-B-pkl"
)

OUTPUT_FILE = (
    PROJECT2_ROOT
    / "results"
    / "tables"
    / "casiab_processed_audit.csv"
)


# ---------------------------------------------------------
# CASIA-B structure
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
    if int(subject) <= 74:
        return "train"

    return "test"


def main():

    # -----------------------------------------------------
    # Verify paths
    # -----------------------------------------------------

    if not RAW_ROOT.exists():
        print("ERROR: Raw CASIA-B dataset not found.")
        print(RAW_ROOT)
        return

    if not PROCESSED_ROOT.exists():
        print("ERROR: Processed CASIA-B dataset not found.")
        print(PROCESSED_ROOT)
        return

    rows = []

    raw_empty = 0
    raw_nonempty = 0
    processed_count = 0
    missing_after_processing = []

    # -----------------------------------------------------
    # Compare raw and processed data
    # -----------------------------------------------------

    for subject in SUBJECTS:

        split = get_split(subject)

        for condition in CONDITIONS:

            for view in VIEWS:

                raw_sequence = (
                    RAW_ROOT
                    / subject
                    / condition
                    / view
                )

                processed_file = (
                    PROCESSED_ROOT
                    / subject
                    / condition
                    / view
                    / f"{view}.pkl"
                )

                if raw_sequence.exists():
                    raw_frame_count = len(
                        list(raw_sequence.glob("*.png"))
                    )
                else:
                    raw_frame_count = 0

                pkl_exists = processed_file.exists()

                if raw_frame_count == 0:
                    raw_empty += 1
                else:
                    raw_nonempty += 1

                if pkl_exists:
                    processed_count += 1

                if raw_frame_count > 0 and not pkl_exists:
                    missing_after_processing.append(
                        {
                            "subject": subject,
                            "split": split,
                            "condition": condition,
                            "view": view,
                            "raw_frame_count": raw_frame_count,
                        }
                    )

                rows.append(
                    {
                        "subject": subject,
                        "split": split,
                        "condition": condition,
                        "view": view,
                        "raw_frame_count": raw_frame_count,
                        "processed_pkl_exists": pkl_exists,
                    }
                )

    # -----------------------------------------------------
    # Save audit CSV
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
                "raw_frame_count",
                "processed_pkl_exists",
            ],
        )

        writer.writeheader()
        writer.writerows(rows)

    # -----------------------------------------------------
    # Processed subject count
    # -----------------------------------------------------

    processed_subject_count = len(
        [
            p
            for p in PROCESSED_ROOT.iterdir()
            if p.is_dir()
        ]
    )

    expected_sequences = (
        len(SUBJECTS)
        * len(CONDITIONS)
        * len(VIEWS)
    )

    # -----------------------------------------------------
    # Print results
    # -----------------------------------------------------

    print()
    print("CASIA-B OpenGait Processed Dataset Audit")
    print("----------------------------------------")

    print(f"Expected subjects:                    {len(SUBJECTS)}")
    print(f"Processed subject folders:            {processed_subject_count}")
    print()

    print(f"Expected sequence folders:            {expected_sequences}")
    print(f"Empty raw sequences:                  {raw_empty}")
    print(f"Non-empty raw sequences:              {raw_nonempty}")
    print(f"Processed PKL files:                  {processed_count}")
    print()

    print(
        f"Non-empty sequences missing PKL:      "
        f"{len(missing_after_processing)}"
    )

    if missing_after_processing:

        print()
        print("Sequences lost during preprocessing")
        print("-----------------------------------")

        for item in missing_after_processing:

            print(
                f"Subject {item['subject']} | "
                f"{item['split']} | "
                f"{item['condition']} | "
                f"View {item['view']} | "
                f"Raw frames: {item['raw_frame_count']}"
            )

    print()
    print("Audit saved to:")
    print(OUTPUT_FILE)
    print()


if __name__ == "__main__":
    main()