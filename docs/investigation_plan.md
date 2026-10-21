# Project 2 — GaitPart Investigation Plan

## Research Objective

Investigate how temporal sequence length, walking conditions, and camera viewpoints affect identification performance in GaitPart.

The investigations will use CASIA-B and the reproduced GaitPart model.

## Investigation 1: Temporal Sequence-Length Sensitivity

### Research Question

How does the number of silhouette frames available during inference affect Rank-1 gait identification accuracy?

### Hypothesis

Longer gait sequences may improve recognition because they provide more temporal information about an individual's walking pattern. Improvements may diminish once sufficient walking information is available.

### Independent Variable

Number of input frames:

- 15 frames
- 30 frames
- 50 frames

### Controlled Variables

- Same trained GaitPart checkpoint
- Same CASIA-B testing subjects
- Same gallery and probe definitions
- Same camera-view evaluation protocol
- Same preprocessing and silhouette resolution
- Same Euclidean-distance metric
- Same deterministic frame-selection procedure

### Dependent Variable

Rank-1 identification accuracy, reported separately for NM, BG, and CL.

### Experimental Procedure

1. Restore the selected GaitPart checkpoint.
2. Extract the prescribed number of frames from each gait sequence.
3. Apply the same frame-selection policy to gallery and probe sequences.
4. Compute GaitPart embeddings.
5. Perform identification using the existing OpenGait evaluation protocol.
6. Record per-condition and per-view accuracy.
7. Repeat with controlled sampling seeds if randomness is used.

Sequences with fewer available frames must be handled according to a documented policy, and the number of affected sequences must be reported.

### Expected Findings

Shorter sequences may provide insufficient motion information, while longer sequences may capture more discriminative gait patterns.

This is a hypothesis, not an established result.

## Investigation 2: Walking-Condition Robustness

### Research Question

How does recognition performance change under normal walking, bag-carrying, and clothing variation?

### Method

Using the same trained checkpoint, compare Rank-1 accuracy across:

- NM: Normal walking
- BG: Carrying a bag
- CL: Clothing variation

### Preliminary Results

| Condition | 500 iterations | 10,000 iterations |
|---|---:|---:|
| NM | 48.49% | 91.25% |
| BG | 37.23% | 82.99% |
| CL | 14.07% | 67.23% |

The two checkpoints were trained with different batch configurations, so the accuracy differences cannot be attributed exclusively to training duration.

## Investigation 3: Viewpoint Robustness

### Research Question

How does camera viewpoint affect GaitPart identification accuracy?

### Method

Analyze Rank-1 recognition accuracy across the eleven CASIA-B camera viewpoints:

0°, 18°, 36°, 54°, 72°, 90°, 108°, 126°, 144°, 162°, and 180°.

Use OpenGait's identical-view exclusion protocol.

### Analysis

Compare:

- Recognition accuracy at each viewpoint
- Differences between NM, BG, and CL
- Viewpoints with the highest and lowest identification accuracy
- Sensitivity to viewpoint changes

## Investigation 4: Project 1 Baseline Comparison

### Research Question

Does GaitPart outperform the Project 1 GEI nearest-neighbor baseline under a matched identification protocol?

### Method

Use equivalent:

- Training and testing subjects
- Gallery and probe sequences
- Camera viewpoints
- Walking conditions
- Rank-1 identification metric

### Important Limitation

Project 1 reported 95.93% Rank-1 accuracy for a controlled 90-degree normal-walking experiment.

This number cannot be directly compared with GaitPart's cross-view results without matching the experimental protocol.

A matched comparison must be implemented or the limitation explicitly documented.

## Experimental Integrity

Each investigation will record the configuration, checkpoint, dataset subset, sampling procedure, evaluation command, results, and interpretation.

The goal is to investigate the published method while clearly distinguishing reproduced behavior from modifications introduced for experimental analysis.
