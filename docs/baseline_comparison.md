# Project 2 — GEI vs. GaitPart Comparison

## Objective

Compare the GaitPart gait recognition method with the Gait Energy Image (GEI) baseline developed in Project 1.

The objective is to evaluate both methods under a consistent identification protocol, rather than directly comparing results obtained under different conditions.

## Methods

### Project 1 — GEI Baseline

The baseline constructs a Gait Energy Image by averaging preprocessed silhouettes from a walking sequence.

The resulting image is flattened into a feature vector and compared against gallery features using Euclidean nearest-neighbor matching.

### Project 2 — GaitPart

GaitPart learns identity representations from silhouette sequences using part-based spatial and temporal feature extraction.

Its learned embeddings are compared using Euclidean distance.

## Matched Evaluation Protocol

| Parameter | Value |
|---|---|
| Dataset | CASIA-B |
| Evaluation subjects | 075–124 |
| Number of subjects | 50 |
| Gallery sequences | nm-01 through nm-04 |
| Probe sequences | nm-05 and nm-06 |
| Camera viewpoint | 90° |
| Matching metric | Euclidean distance |
| Evaluation metric | Rank-1 identification accuracy |

The methods retain their original preprocessing and feature-extraction procedures.

GaitPart is trained on subjects 001–074, while GEI uses a nonlearned feature representation.

## Verified GEI Results

The held-out GEI baseline produced:

- Subjects evaluated: 50
- Correct predictions: 95
- Total probes: 100
- Rank-1 accuracy: 95.00%

The experiment was implemented in:

`scripts/evaluate_gei_matched.py`

Results are saved under:

`results/tables/`

## GaitPart Matched Results

Pending execution of the matched-view evaluation.

The OpenGait evaluator computes a matrix of identification accuracy for each probe-view and gallery-view pair.

For the normal-walking 90° → 90° experiment, the relevant value is:

`acc["NM"][5, 5, 0]`

A reproducible evaluator modification is stored in:

`patches/gaitpart_matched_90.patch`

## Interpretation

A matched comparison will establish which method performs better under the controlled 90° normal-walking identification task.

This does not necessarily establish which model is superior under clothing variation, bag carrying, or cross-view conditions.

Those conditions are investigated separately.

## Limitations

- GEI and GaitPart use different feature representations and preprocessing.
- GaitPart uses learned representations, whereas GEI does not.
- The controlled 90° comparison is only one part of the broader CASIA-B evaluation.
- Any missing sequences or subject exclusions must be documented and handled consistently.
- Final conclusions will be added after the matched GaitPart evaluation is completed.
