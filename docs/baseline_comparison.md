# Project 2 — GEI vs. GaitPart Comparison

## Objective

Compare the GaitPart gait recognition method with the Gait Energy Image (GEI) baseline developed in Project 1.

The objective is to evaluate both methods under a consistent identification protocol, rather than directly comparing results obtained under different conditions.

This investigation addresses the Project 2 requirement to compare and contrast a reproduced modern biometric method with the baseline system from Project 1.

## Methods

### Project 1 — GEI Baseline

The baseline constructs a Gait Energy Image by averaging preprocessed silhouettes from a walking sequence.

Each silhouette is cropped around the subject, resized while preserving its aspect ratio, and centered on a 128 × 128 pixel canvas.

The resulting GEI is flattened into a feature vector and compared against gallery features using Euclidean nearest-neighbor matching.

The GEI baseline does not require neural network training.

### Project 2 — GaitPart

GaitPart is a deep-learning-based gait recognition model that learns spatial and temporal features from silhouette sequences.

The approach extracts part-level representations to capture information from different body regions and their movement over time.

The implementation uses the OpenGait framework with triplet-loss training.

GaitPart produces learned feature embeddings that are compared using Euclidean distance.

The evaluated model was trained for 30,000 iterations using CASIA-B subjects 001–074.

## Matched Evaluation Protocol

To ensure a fair comparison, both methods were evaluated using the same identification task.

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
| GaitPart training subjects | 001–074 |

The methods retain their original preprocessing and feature-extraction procedures.

GEI uses a nonlearned representation, while GaitPart learns identity-discriminative features from a separate training partition.

Both methods use the same gallery and probe sequence definitions for the matched comparison.

## GEI Baseline Results

The original Project 1 GEI method was evaluated again using the held-out CASIA-B subjects from Project 2.

The experiment was implemented in:

`scripts/evaluate_gei_matched.py`

The evaluation produced:

- Subjects evaluated: 50
- Subjects excluded: 0
- Correct predictions: 95
- Total probes: 100
- Rank-1 identification accuracy: 95.00%

Results are saved under:

`results/tables/gei_matched_predictions.csv`

`results/tables/gei_matched_summary.json`

## GaitPart Matched Results

The GaitPart model was evaluated after 30,000 training iterations using the same controlled 90-degree normal-walking identification protocol.

The OpenGait evaluator calculates a matrix of Rank-1 identification accuracy for each probe-view and gallery-view combination.

For the 90° → 90° comparison, the relevant matrix entry is:

`acc["NM"][5, 5, 0]`

This value corresponds to:

- Probe viewpoint: 90°
- Gallery viewpoint: 90°
- Probe sequences: nm-05 and nm-06
- Gallery sequences: nm-01 through nm-04

The evaluator modification used to report this result is stored in:

`patches/gaitpart_matched_90.patch`

### Matched Identification Results

| Method | Rank-1 Accuracy |
|---|---:|
| Project 1 — GEI Baseline | 95.00% |
| Project 2 — GaitPart (30,000 iterations) | 100.00% |
| Difference | +5.00 percentage points |

The GEI baseline correctly identified 95 of 100 probe sequences.

GaitPart achieved 100.00% Rank-1 accuracy for the matched 90-degree identification experiment.

**Dataset coverage verification:** The GaitPart evaluation succeeded on the held-out partition, but an independent check confirming the presence of all 300 intended 90-degree gallery and probe sequences is still pending.

## Additional GaitPart Results

The 30,000-iteration GaitPart model was also evaluated across the eleven CASIA-B camera viewpoints.

The standard OpenGait evaluation excludes identical-view comparisons when calculating its reported cross-view averages.

### Cross-View Rank-1 Accuracy

| Walking Condition | Rank-1 Accuracy |
|---|---:|
| Normal Walking (NM) | 94.20% |
| Carrying a Bag (BG) | 87.19% |
| Clothing Variation (CL) | 73.03% |

These results show that GaitPart performs best under normal walking conditions.

Carrying a bag reduces recognition accuracy, while clothing variation produces the lowest accuracy of the three conditions.

These cross-view results should not be directly compared with the GEI baseline's single-view 95.00% accuracy because the evaluation conditions differ.

## Investigation: Effect of Training Duration

GaitPart was evaluated at multiple training stages.

| Training Iterations | NM Rank-1 | BG Rank-1 | CL Rank-1 |
|---|---:|---:|---:|
| 500 | 48.49% | 37.23% | 14.07% |
| 10,000 | 91.25% | 82.99% | 67.23% |
| 30,000 | 94.20% | 87.19% | 73.03% |

Identification accuracy improved substantially between the preliminary 500-iteration checkpoint and the 30,000-iteration model.

Between 10,000 and 30,000 iterations, accuracy improved by:

- Normal walking: 2.95 percentage points
- Bag carrying: 4.20 percentage points
- Clothing variation: 5.80 percentage points

The 10,000- and 30,000-iteration results come from the same continuous training experiment with batch composition [4, 8].

The 500-iteration benchmark used a smaller batch composition [2, 2] and was trained independently. Therefore, its differences cannot be attributed exclusively to training duration.

## Interpretation

Under the matched 90-degree normal-walking identification protocol, GaitPart achieved 100.00% Rank-1 accuracy, compared with 95.00% for the GEI baseline.

This represents an improvement of 5 percentage points in favor of GaitPart.

The result demonstrates that the trained GaitPart implementation can outperform the original GEI baseline under the tested conditions.

One possible explanation is that GaitPart learns discriminative spatial and temporal representations, whereas GEI compresses walking motion into a single averaged image.

However, the observed improvement alone does not establish that GaitPart's temporal components caused the difference. A controlled architectural ablation would be needed to isolate their contribution.

The broader GaitPart results also show differences in robustness across walking conditions and viewpoints.

Normal walking produced the highest recognition accuracy, while clothing variation remained the most challenging condition.

## Limitations

- GEI and GaitPart use different feature representations and preprocessing procedures.
- GaitPart learns representations from subjects 001–074, while GEI uses a nonlearned feature representation.
- The matched comparison evaluates only normal walking at a single 90-degree camera viewpoint.
- GaitPart's broader cross-view results cannot be directly compared with the GEI single-view baseline.
- The GaitPart model has completed 30,000 of the reference configuration's 120,000 training iterations.
- Complete availability of the 300 intended GaitPart gallery and probe sequences remains to be independently verified.
- The matched comparison uses one trained GaitPart model; variability across training seeds has not been measured.
- The 100.00% result applies to this particular identification protocol and does not establish universal superiority.
- A full architectural ablation of GaitPart has not yet been performed.

## Conclusion

The matched evaluation demonstrates that the reproduced GaitPart model achieved higher Rank-1 identification accuracy than the GEI baseline under controlled 90-degree normal-walking conditions.

GaitPart achieved 100.00% accuracy, while the GEI baseline achieved 95.00%.

Additional GaitPart evaluations demonstrated strong cross-view recognition performance under normal walking, bag carrying, and clothing variation.

These findings support the usefulness of learned gait representations, while also showing that recognition performance depends on walking conditions and camera viewpoints.

Further investigation of temporal sequence length will help characterize how the amount of available walking information affects GaitPart recognition performance.

## Reproducibility

The relevant project files are:

- `scripts/evaluate_gei_matched.py` — Reproduces the GEI baseline under the held-out 90-degree protocol.
- `patches/gaitpart_matched_90.patch` — Adds matched-view accuracy reporting to the pinned OpenGait evaluator.
- `configs/gaitpart_casiab_eval_30000.yaml` — Evaluation configuration for the 30,000-iteration checkpoint.
- `experiments/experiment_log.md` — Chronological record of experiments and results.
- `docs/reproduction_plan.md` — Reproduction environment and execution instructions.

The original GEI implementation remains in the Project 1 repository, while the GaitPart implementation uses the pinned OpenGait framework.
