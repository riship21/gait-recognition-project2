# GaitPart Original Experiment Logs

These files are original OpenGait training and evaluation logs generated
during the COSC 594 Project 2 experiments.

All experiments used the CASIA-B dataset and the pinned OpenGait implementation.

## Training and Evaluation

| Log File | Description |
|---|---|
| 2026-10-20-22-58-32.txt | Training from iteration 0 to 10,000 |
| 2026-10-21-17-56-37.txt | Evaluation of the 10,000-iteration checkpoint |
| 2026-10-21-18-03-55.txt | Resumed training from iteration 10,000 to 30,000 |
| 2026-10-21-20-20-48.txt | Standard evaluation of the 30,000-iteration checkpoint |
| 2026-10-21-20-30-43.txt | Matched 90-degree evaluation of the 30,000-iteration checkpoint |

## Temporal Sequence-Length Ablation

| Log File | Maximum Frames |
|---|---|
| 2026-10-22-11-43-36.txt | 15 |
| 2026-10-22-11-44-21.txt | 30 |
| 2026-10-22-11-45-09.txt | 50 |

The unlimited-frame evaluation is recorded in the standard
30,000-iteration evaluation log.

## Final Results

Cross-view Rank-1 accuracy, excluding identical-view comparisons:

| Maximum Frames | NM | BG | CL |
|---|---:|---:|---:|
| 15 | 63.99% | 54.19% | 42.32% |
| 30 | 86.25% | 76.34% | 62.16% |
| 50 | 91.77% | 84.22% | 70.13% |
| Unlimited | 94.20% | 87.19% | 73.03% |

The full-frame matched 90-degree normal-walking evaluation
achieved 100.00% Rank-1 accuracy.

See `experiments/experiment_log.md` for methodology and interpretation.

These text logs do not contain the CASIA-B image dataset or model checkpoints.
