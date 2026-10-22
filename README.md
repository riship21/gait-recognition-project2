# GaitPart Reproduction and Investigation

**Course:** COSC 594 — Biometrics  
**Project:** Project 2 — Reproduce + Investigate  
**Dataset:** CASIA-B

## Overview

This project reproduces GaitPart, a modern gait recognition approach introduced by Fan et al. at CVPR 2020, using the OpenGait framework.

The project extends the Gait Energy Image (GEI) baseline developed in Project 1.

The primary objectives are to reproduce the method, compare it against GEI under a matched identification protocol, and investigate recognition performance under different walking conditions, viewpoints, and temporal input lengths.

## Reference Paper

Fan et al. (2020). *GaitPart: Temporal Part-Based Model for Gait Recognition*. Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition.

The implementation uses a pinned revision of the OpenGait framework.

See `docs/paper_notes.md` and `docs/reproduction_plan.md` for additional details.

## Dataset

CASIA-B contains walking sequences from 124 subjects across eleven camera viewpoints.

The experiments use three walking conditions:

- NM — Normal walking
- BG — Carrying a bag
- CL — Clothing variation

The official OpenGait subject partition is used:

- Training: Subjects 001–074
- Testing: Subjects 075–124

A total of 13,592 processed sequence files were available.

The CASIA-B dataset is not redistributed in this repository.

## Methodology

The Project 1 baseline generates Gait Energy Images by averaging preprocessed silhouettes and performs Euclidean nearest-neighbor identification.

GaitPart uses part-based spatial feature extraction and temporal modeling to learn identity-discriminative gait embeddings.

The reproduced model is trained using triplet loss and evaluated with Euclidean-distance matching.

## Experimental Environment

Training was performed on an MSI laptop with:

- NVIDIA RTX 3060 Laptop GPU (6 GB)
- WSL2 / Ubuntu 22.04
- Python 3.9.25
- PyTorch 2.2.2+cu121
- CUDA 12.1 runtime

The primary Conda environment is `gaitpart-p2`.

See `docs/environment.md` for additional configuration details.

## Reproduction Results

The main GaitPart model completed 30,000 training iterations using batch composition [4, 8].

### Rank-1 Identification Accuracy

| Iterations | NM | BG | CL |
|---|---:|---:|---:|
| 500 | 48.49% | 37.23% | 14.07% |
| 10,000 | 91.25% | 82.99% | 67.23% |
| 30,000 | 94.20% | 87.19% | 73.03% |

These values use OpenGait's CASIA-B evaluation protocol with identical-view comparisons excluded.

The 500-iteration model used a different training batch configuration and is presented as a preliminary benchmark.

## Comparison with Project 1

Both methods were evaluated under a controlled 90-degree normal-walking identification protocol.

- Evaluation subjects: 075–124
- Gallery: nm-01 through nm-04
- Probe: nm-05 and nm-06
- Metric: Rank-1 identification accuracy

| Method | Rank-1 Accuracy |
|---|---:|
| GEI baseline | 95.00% |
| GaitPart (30,000 iterations) | 100.00% |

All 300 intended GaitPart gallery and probe sequences were verified as present.

The comparison indicates that GaitPart achieved higher accuracy under this specific matched protocol.

See `docs/baseline_comparison.md` for methodology, interpretation, and limitations.

## Temporal Sequence-Length Investigation

Inference was evaluated using different maximum frame counts while preserving the same trained model checkpoint.

| Maximum frames | NM | BG | CL |
|---|---:|---:|---:|
| 15 | 63.99% | 54.19% | 42.32% |
| 30 | 86.25% | 76.34% | 62.16% |
| 50 | 91.77% | 84.22% | 70.13% |
| Unlimited | 94.20% | 87.19% | 73.03% |

Limiting the number of inference frames reduced recognition performance, particularly for cross-view identification.

The experiment uses the first N available frames, rather than uniform temporal subsampling.

See `docs/investigation_plan.md` and `experiments/experiment_log.md`.

## Reproducibility

The repository contains:

- Experiment configuration files in `configs/`
- Preprocessing and evaluation scripts in `scripts/`
- Chronological experiment records in `experiments/`
- Reproduction documentation in `docs/`
- Structured result tables in `results/tables/`
- A reproducible matched-view evaluator patch in `patches/`

See `docs/reproduction_plan.md` for the environment, dataset preparation, training, checkpoint restoration, and evaluation workflow.

The OpenGait source is obtained separately at its documented pinned commit.

## Reproduction Limitations

- The principal GaitPart experiment completed 30,000 iterations rather than the reference configuration's 120,000.
- Training used a smaller batch composition to accommodate the available GPU.
- The original dataset contained missing or unusually short sequences.
- The experiments used a single main training trajectory.
- The temporal-length investigation limits the first N available frames and does not isolate individual model components.
- Additional investigation would be needed to measure variability across training seeds and isolate architectural contributions.

## Project Documentation

- `docs/reproduction_plan.md` — Reproduction procedure
- `docs/environment.md` — Software and hardware environment
- `docs/paper_notes.md` — Reference-paper analysis
- `docs/baseline_comparison.md` — Matched GEI comparison
- `docs/investigation_plan.md` — Investigation design
- `experiments/experiment_log.md` — Chronological experiments and results
- `docs/ai_log.md` — AI-assistance documentation

## Conclusion

The project successfully reproduced a working GaitPart recognition pipeline on CASIA-B and evaluated it under multiple experimental conditions.

Under the matched 90-degree normal-walking protocol, GaitPart achieved 100.00% Rank-1 accuracy compared with 95.00% for the Project 1 GEI baseline.

The temporal sequence-length investigation also showed that recognition performance depends on the amount of gait-sequence information available during inference.

Together, these experiments demonstrate reproduction, investigation, and comparison of a modern biometric identification approach.
