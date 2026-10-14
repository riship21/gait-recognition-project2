# GaitPart Reproduction Plan

## Reproduction Target

Primary paper:

Fan et al.,
"GaitPart: Temporal Part-Based Model for Gait Recognition,"
CVPR 2020.

## Biometric Problem

Closed-set gait identification using silhouette sequences.

## Dataset

CASIA-B.

The exact train/test split, gallery/probe protocol, preprocessing,
and evaluation procedure will be extracted from the paper and reference
implementation before experiments begin.

## Method

GaitPart learns spatial and short-term temporal gait information from
silhouette sequences.

Important components include:

- Focal Convolution Layer (FConv)
- Micro-motion Capture Module (MCM)
- Part-level gait features
- Triplet-loss-based training

## Reproduction Goals

1. Reproduce the CASIA-B evaluation protocol.
2. Reproduce reported GaitPart performance as closely as practical.
3. Clearly document any deviations from the paper.
4. Preserve raw training and evaluation outputs.
5. Compare reproduction results with the published results.
6. Perform at least one targeted investigation related to the method.

## Planned Evaluation

Evaluation is expected to include:

- Rank-1 identification accuracy
- Rank-5 identification accuracy
- CMC / rank curve
- NM condition
- BG condition
- CL condition
- per-view analysis where appropriate

## Reproducibility

The final repository will document:

- operating system
- Python version
- PyTorch version
- CUDA version
- GPU / hardware
- dataset access and directory structure
- preprocessing commands
- training commands
- evaluation commands
- configuration files
- model checkpoints
- raw result files
- all deviations from the original paper