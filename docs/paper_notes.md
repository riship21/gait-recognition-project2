# GaitPart Paper Notes

## Paper

Chao Fan et al.
"GaitPart: Temporal Part-Based Model for Gait Recognition"
CVPR 2020

## Main Idea

GaitPart treats different body regions separately instead of learning one
representation for the entire silhouette.

The method contains two important components:

- Focal Convolution Layer (FConv) for part-level spatial feature learning
- Micro-motion Capture Module (MCM) for short-term temporal gait features

This differs from the Project 1 GEI baseline because GEI averages the whole
walking sequence into one image, while GaitPart preserves and learns from
the silhouette sequence.

## CASIA-B Protocol

CASIA-B contains 124 subjects with 11 views and three walking conditions:

- NM: normal walking, 6 sequences
- BG: walking while carrying a bag, 2 sequences
- CL: walking while wearing a coat or jacket, 2 sequences

Training subjects:
001-074

Testing subjects:
075-124

Gallery:
NM#1-4

Probe sets:
NM#5-6
BG#1-2
CL#1-2

All 11 camera views are evaluated.

Identical-view gallery/probe cases are excluded when reporting the
cross-view average results.

## Paper Training Details

Input silhouettes:
64 x 44

Optimizer:
Adam

Learning rate:
1e-4

Triplet-loss margin:
0.2

Batch size:
(8, 16)

This means 8 identities with 16 sequences per identity.

Training iterations:
120,000

Training frame sampling:
A 30-40 frame segment is first selected and 30 ordered frames are sampled.

Sequences shorter than 15 frames are discarded.

Sequences containing 15-30 frames are repeatedly sampled.

Testing:
All available frames are provided to the model.

Matching:
Average Euclidean distance between corresponding part-level feature vectors.

## Published CASIA-B Results

Average Rank-1 accuracy excluding identical-view cases:

| Condition | GaitPart |
|---|---:|
| NM | 96.2% |
| BG | 91.5% |
| CL | 78.7% |

## Known Correction

The authors' official GitHub repository documents a clerical correction
for the 90-degree BG result.

The value should be 84.9%, not 94.9%.

The reported overall BG average of 91.5% remains correct.

## Project 2 Reproduction Target

The primary goal is to reproduce the CASIA-B GaitPart results as closely
as practical and document any differences between:

1. the original paper,
2. the reference implementation,
3. our reproduced implementation.