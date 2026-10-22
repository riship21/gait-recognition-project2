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

## Experiment 2 - OpenGait CASIA-B Preprocessing

### Goal

Convert the raw CASIA-B silhouette sequences into the processed format
required by OpenGait and verify which sequences survive preprocessing.

### Input

Raw CASIA-B silhouettes from Project 1:

`../biometrics-project1-gait-recognition/data/raw/CASIA-B/GaitDatasetB-silh`

### Method

The pinned OpenGait preprocessing script was used:

`datasets/pretreatment.py`

Important settings:

- image size: 64
- dataset: CASIAB
- workers: 4
- output format: pickle (`.pkl`)

Command:

```powershell
python .\third_party\OpenGait\datasets\pretreatment.py --input_path "..\biometrics-project1-gait-recognition\data\raw\CASIA-B\GaitDatasetB-silh" --output_path ".\data\processed\CASIA-B-pkl" --n_workers 4 --img_size 64 --dataset CASIAB --log_file ".\results\raw\opengait_pretreatment.log"
```

### Results

The preprocessing produced 13,592 pickle sequence files from the available CASIA-B silhouettes.

The processed sequences were subsequently transferred to the MSI WSL environment for training.

## Experiment 3 - MSI GPU Environment and Smoke-Test Preparation

### Goal

Prepare the GPU environment required to run GaitPart and verify that the
processed CASIA-B dataset is available on the training machine.

### Environment

- MSI GS66
- NVIDIA GeForce RTX 3060 Laptop GPU
- 6 GB VRAM
- WSL2 / Ubuntu 22.04
- Python 3.9.25
- PyTorch 2.2.2+cu121
- CUDA runtime 12.1

### Dataset Verification

The processed CASIA-B dataset was successfully transferred into the WSL
project environment.

Verified:

- 124 subject folders
- 13,592 processed `.pkl` sequences

### Status

Environment setup completed successfully.

Subsequent smoke testing confirmed that GaitPart could initialize, train, and save checkpoints on the GPU.

## Experiment 4 - NumPy Serialization Compatibility

### Goal

Resolve the dataset-loading failure encountered when initializing GaitPart training.

### Problem

The processed CASIA-B pickle files were created using NumPy 2.x serialization internals, while the GaitPart training environment used NumPy 1.23.5.

This caused the following error:

`ModuleNotFoundError: No module named 'numpy._core'`

### Method

A separate Conda environment was created with NumPy 2.0.2 to read the original processed files.

The dataset was converted in two stages:

1. Export the original pickle arrays into `.npy` files using NumPy 2.0.2.
2. Repackage the arrays into `.pkl` files using NumPy 1.23.5.

The conversion script is located at:

`scripts/convert_casiab_numpy.py`

### Results

- Original processed files: 13,592
- Intermediate arrays exported: 13,592
- Compatible pickle files generated: 13,592
- Example sequence shape: (87, 64, 64)
- Data type: uint8
- Original files preserved

### Conclusion

The compatibility issue was resolved without upgrading the existing PyTorch/CUDA training environment.

The converted dataset was used for subsequent GaitPart experiments.

---

## Experiment 5 - GaitPart Training Smoke Test

### Goal

Verify that GaitPart could load CASIA-B data, initialize successfully on the GPU, perform backpropagation, and save a checkpoint.

### Configuration

- Model: GaitPart
- Dataset: CASIA-B
- Batch composition: [2, 2]
- Total batch size: 4 sequences
- Training iterations: 5
- Optimizer: Adam
- Learning rate: 0.0001
- Triplet-loss margin: 0.2
- Mixed precision: Enabled

Configuration file:

`configs/gaitpart_casiab_smoke.yaml`

### Results

Training completed all five iterations successfully.

Reported triplet loss:

| Iteration | Triplet Loss |
|---|---:|
| 1 | 0.1919 |
| 2 | 0.1943 |
| 3 | 0.1943 |
| 4 | 0.1947 |
| 5 | 0.1909 |

Checkpoint generated:

`GaitPart_Smoke-00005.pt`

### Conclusion

The training pipeline was functional. However, five iterations were insufficient to evaluate convergence or recognition accuracy.

---

## Experiment 6 - Training Performance Benchmark

### Goal

Measure training speed and numerical stability over a longer run before selecting a full-training configuration.

### Configuration

- Model: GaitPart
- Batch composition: [2, 2]
- Total batch size: 4 sequences
- Training iterations: 500
- Logging interval: 50
- Mixed precision: Enabled

Configuration:

`configs/gaitpart_casiab_benchmark.yaml`

### Results

The 500-iteration run completed successfully.

- Model parameters: Approximately 1.204 million
- Steady-state training speed: Approximately 0.043 seconds per iteration
- Final reported triplet loss: 0.1835
- Checkpoint: `GaitPart_Benchmark-00500.pt`

### Conclusion

Training remained numerically stable during the benchmark.

The small batch provided fast iterations, but the limited number of identities and sequences could affect triplet-loss learning.

A larger-batch investigation was performed next.

---

## Experiment 7 - Training Batch-Size Investigation

### Goal

Investigate how different batch compositions affect training feasibility and performance on the RTX 3060 Laptop GPU.

### Method

Separate training experiments were performed using different numbers of identities and sequences per identity.

All experiments used the same GaitPart architecture, training dataset, optimizer, and mixed-precision setting.

### Results

| Batch composition | Total sequences | Iterations | Approx. steady-state seconds/iteration | Result |
|---|---:|---:|---:|---|
| [2, 2] | 4 | 500 | 0.043 | Successful |
| [4, 4] | 16 | 100 | 0.106 | Successful |
| [4, 8] | 32 | 100 | 0.190 | Successful |
| [8, 8] | 64 | 50 | 0.394 | Successful |

No CUDA out-of-memory errors were reported in these experiments.

### Observation

Larger batches increased iteration time but supplied more identity and sequence combinations for triplet learning.

The official reference configuration uses [8, 16], which corresponds to 128 sequences per batch.

These short experiments primarily established hardware feasibility. They did not establish which batch composition provides the best recognition accuracy.

### Decision

Batch composition [4, 8] was selected for the subsequent long-running experiment as a practical compromise between computational cost and training batch diversity.

### Limitations

The experiments used different numbers of training iterations, and peak GPU memory was not systematically recorded.

Therefore, training loss values cannot be used to make a controlled comparison of recognition quality between batch sizes.

---

## Experiment 8 - Checkpoint Restoration Test

### Goal

Verify that training could be resumed successfully from a previously saved checkpoint.

### Method

The Batch64 GaitPart checkpoint saved at iteration 50 was restored.

Training was resumed with:

- Starting iteration: 50
- Target iteration: 60
- Additional iterations: 10
- Batch composition: [8, 8]

### Results

OpenGait successfully loaded the saved model and continued training through iteration 60.

The new checkpoint contained:

- Model state
- Optimizer state
- Scheduler state
- Iteration counter

Verification results:

- Saved iteration: 60
- Optimizer state entries: 71
- Scheduler epoch: 60

### Conclusion

Checkpoint restoration and continued training were verified.

A limitation is that the OpenGait checkpoint implementation does not save the automatic mixed-precision GradScaler state, meaning resumed training may not be bit-for-bit identical to uninterrupted training.

---

## Experiment 9 - Preliminary CASIA-B Recognition Evaluation

### Goal

Verify the complete gait-recognition evaluation pipeline and measure preliminary Rank-1 identification accuracy.

### Method

The GaitPart model trained for 500 iterations was evaluated using the official CASIA-B held-out subject partition.

- Training subjects: 001–074
- Testing subjects: 075–124
- Test sequences processed: 5,485
- Distance metric: Euclidean
- Evaluation batch size: 1 GPU
- Identical-view comparisons: Excluded

### Results

| Walking condition | Rank-1 accuracy |
|---|---:|
| Normal walking (NM) | 48.49% |
| Carrying a bag (BG) | 37.23% |
| Clothing variation (CL) | 14.07% |

### Observation

Normal walking achieved the highest identification accuracy, followed by bag-carrying and clothing variation.

This suggests that changes to body appearance and walking conditions can make gait recognition more difficult.

### Conclusion

The end-to-end evaluation pipeline worked successfully, including model checkpoint restoration, feature extraction, distance-based matching, and Rank-1 evaluation.

These preliminary results reflect a model trained for only 500 iterations. They should not be interpreted as the final GaitPart reproduction performance.

---

## Experiment 10 - Extended GaitPart Training

### Goal

Train GaitPart for a substantially longer schedule to improve learned identity representations and prepare for a more meaningful recognition evaluation.

### Configuration

- Dataset: CASIA-B
- Model: GaitPart
- Batch composition: [4, 8]
- First-stage training target: 10,000 iterations
- Final completed training target: 30,000 iterations
- Reference configuration target: 120,000 iterations
- Optimizer: Adam
- Learning rate: 0.0001
- Triplet-loss margin: 0.2
- Mixed precision: Enabled
- Checkpoint interval: 2,000 iterations

Configuration files:

- `configs/gaitpart_casiab_full.yaml`
- `configs/gaitpart_casiab_30000.yaml`
- `configs/gaitpart_casiab_eval_10000.yaml`
- `configs/gaitpart_casiab_eval_30000.yaml`

### Method

The initial model was trained from iteration 0 to iteration 10,000.

Training was then resumed from the saved iteration-10,000 checkpoint and continued to iteration 30,000.

The same model architecture, batch composition, optimizer, and learning-rate scheduler were preserved across both training stages.

Recognition performance was measured using the official CASIA-B evaluation protocol, excluding identical-view comparisons.

### Status

Completed successfully on the MSI RTX 3060 Laptop GPU.

### Training Results

| Stage | Iterations | Runtime | Final Reported Triplet Loss |
|---|---|---|---:|
| Initial training | 0–10,000 | 44 minutes 35 seconds | 0.2003 |
| Resumed training | 10,000–30,000 | 1 hour 31 minutes 20 seconds | 0.2045 |

The model successfully resumed training from the iteration-10,000 checkpoint.

The final checkpoint was saved as:

`GaitPart_Full_B32-30000.pt`

Training loss remained finite but did not decrease consistently. Therefore, identification accuracy was used to assess the model's actual recognition performance.

### Rank-1 Recognition Results

| Training Iterations | Normal Walking (NM) | Carrying Bag (BG) | Clothing Variation (CL) |
|---|---:|---:|---:|
| 10,000 | 91.25% | 82.99% | 67.23% |
| 30,000 | 94.20% | 87.19% | 73.03% |
| Improvement | +2.95 pp | +4.20 pp | +5.80 pp |

Both evaluations used the held-out CASIA-B subjects 075–124.

### Observations

Identification accuracy improved across all three walking conditions between 10,000 and 30,000 iterations.

Clothing variation showed the largest improvement but remained the most challenging condition.

These results demonstrate that additional training improved recognition performance along the same training trajectory, even though the triplet loss did not decrease monotonically.

### Conclusion

The extended training and evaluation pipeline completed successfully.

The 30,000-iteration GaitPart model achieved:

- Normal walking Rank-1 accuracy: 94.20%
- Bag-carrying Rank-1 accuracy: 87.19%
- Clothing-variation Rank-1 accuracy: 73.03%

The model completed 30,000 rather than the reference configuration's 120,000 iterations. This deviation is documented as a limitation of the reproduction.

---

## Experiment 11 - Temporal Sequence-Length Ablation

### Goal

Investigate how limiting the number of silhouette frames available during inference affects GaitPart identification accuracy.

### Research Question

How does temporal input length affect Rank-1 gait identification under different walking conditions and camera viewpoints?

### Hypothesis

Longer walking sequences provide more temporal information and may improve identification performance. Improvements may diminish as the available sequence length increases.

### Experimental Setup

- Dataset: CASIA-B
- Evaluation subjects: 075–124
- Model: GaitPart
- Checkpoint: 30,000 iterations
- Batch composition during training: [4, 8]
- Evaluation metric: Rank-1 identification
- Matching metric: Euclidean distance
- Viewpoint protocol: Identical-view comparisons excluded for cross-view averages

### Independent Variable

Maximum number of inference frames:

- 15
- 30
- 50
- Unlimited

### Controlled Variables

The same trained model checkpoint, CASIA-B test partition, gallery/probe definitions, preprocessing, and matching metric were used throughout the experiments.

### Frame-Selection Policy

OpenGait's `frames_all_limit` parameter was used to cap inference sequences.

The first N available frames were selected for each limited-frame experiment.

Sequences shorter than the specified limit retained their available frames.

Consequently, the experiment evaluates maximum sequence length rather than enforcing exactly N frames for every sequence.

### Cross-View Rank-1 Results

| Frame Limit | Normal Walking | Carrying Bag | Clothing Variation |
|---|---:|---:|---:|
| 15 | 63.99% | 54.19% | 42.32% |
| 30 | 86.25% | 76.34% | 62.16% |
| 50 | 91.77% | 84.22% | 70.13% |
| Unlimited | 94.20% | 87.19% | 73.03% |

### Matched 90-Degree Normal-Walking Results

| Frame Limit | Rank-1 Accuracy |
|---|---:|
| 15 | 99.00% |
| 30 | 100.00% |
| 50 | 100.00% |
| Unlimited | 100.00% |

### Observations

Increasing the inference frame limit improved cross-view recognition accuracy across NM, BG, and CL.

The largest performance improvements occurred between 15 and 30 frames.

Further improvements were observed between 30 and 50 frames and between 50 frames and the unlimited-frame evaluation.

Clothing variation produced the lowest accuracy under every frame setting.

The 90-degree same-view identification experiment achieved high accuracy even when only the first 15 frames were available.

### Interpretation

These findings indicate that GaitPart's recognition performance is sensitive to the amount of temporal information supplied during inference, particularly in cross-view identification.

Longer sequences may expose additional gait cycles and more representative walking patterns.

However, the experiment does not isolate the contribution of GaitPart's temporal modeling modules. Such a conclusion would require an architectural ablation.

### Limitations

- The experiment uses first-N-frame truncation rather than uniformly distributed frame sampling.
- Sequences shorter than the specified limit retain their available frames.
- The effective number of input frames may vary between sequences.
- Only one trained checkpoint was evaluated.
- The study does not measure variability across training seeds.
- The experiments were conducted on the existing CASIA-B held-out test partition.

### Conclusion

Increasing the maximum number of inference frames consistently improved GaitPart Rank-1 recognition accuracy across normal walking, bag-carrying, and clothing-variation conditions.

This demonstrates the importance of sequence duration for the reproduced model's identification performance, especially in cross-view scenarios.
