# Project 2 Experiment Log

## Experiment 0 - Reproduction Planning

### Goal

Select a competitive gait recognition method and define the scope of
Project 2.

### Selected Method

GaitPart - CVPR 2020.

### Dataset

CASIA-B.

### Reason for Selection

GaitPart addresses the same gait recognition problem as Project 1 but
uses silhouette sequences and part-level temporal features rather than
compressing an entire walking sequence into a single GEI.

This provides a meaningful progression from the Project 1 baseline.

### Current Investigation Candidates

- Normal vs. bag vs. clothing conditions
- Cross-view performance
- Sequence-length sensitivity
- Comparison with GEI baseline

### Next Step

Review the GaitPart paper and reference implementation to define the
exact reproduction protocol.

## Experiment 1 - CASIA-B Dataset Audit

### Goal

Verify the completeness and sequence quality of the local CASIA-B
silhouette dataset before preprocessing it for GaitPart.

### Dataset

CASIA-B silhouette dataset originally used in Project 1.

Expected structure:

- 124 subjects
- 10 walking sequences per subject
- 11 camera views
- 13,640 total subject/condition/view sequence folders

### Protocol Split

Training:
Subjects 001-074

Testing:
Subjects 075-124

### Results

- Expected subjects: 124
- Expected sequences: 13,640
- Missing sequence folders: 0
- Empty sequences: 47
- Non-empty sequences with fewer than 15 frames: 48
- Total sequences with fewer than 15 frames: 95
- Problematic training sequences: 62
- Problematic testing sequences: 33

The most affected subjects were:

- Subject 068: 21 sequences
- Subject 005: 19 sequences
- Subject 088: 16 sequences
- Subject 037: 10 sequences
- Subject 048: 10 sequences
- Subject 109: 10 sequences
- Subject 079: 5 sequences
- Subject 096: 2 sequences
- Subject 051: 1 sequence
- Subject 026: 1 sequence

### Observation

The dataset directory structure is complete, but several sequence folders
contain very few frames or no frames.

This is important because sequence length directly affects temporal gait
models such as GaitPart.

### OpenGait Behavior

Inspection of the pinned OpenGait implementation showed that:

- empty input folders do not produce processed pickle files
- short non-empty sequences may still be processed
- the GaitPart training sampler can repeat frames when the available
  sequence is shorter than the requested training sample
- testing uses the available sequence frames

Therefore, the practical OpenGait implementation does not simply remove
every sequence containing fewer than 15 frames.

### Decision

The original CASIA-B dataset will not be manually modified.

OpenGait's preprocessing behavior will be preserved so that the
reproduction remains faithful to the selected implementation.

The processed OpenGait dataset will be audited again after preprocessing.