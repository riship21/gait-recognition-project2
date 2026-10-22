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


## Reproduction Configuration

The project-specific GaitPart configuration is stored at:

`configs/gaitpart_casiab_reference.yaml`

OpenGait normally merges `configs/gaitpart/gaitpart.yaml` with
`configs/default.yaml` at runtime.

For reproducibility, the Project 2 configuration explicitly records the
relevant inherited settings rather than relying only on implicit defaults.

The reference configuration preserves the OpenGait GaitPart settings,
including:

- CASIA-B subjects 001-074 for training
- CASIA-B subjects 075-124 for testing
- Adam optimizer
- learning rate 0.0001
- triplet-loss margin 0.2
- 8 x 16 training batch structure
- 30 ordered training frames
- 120,000 training iterations
- Euclidean-distance matching
- 16 part-level feature regions

Hardware-specific changes, if required for the available GPU, will be
stored separately rather than modifying the reference configuration.

## Verified Reproduction Procedure

### 1. Hardware and Software

The GaitPart reproduction experiments were performed using:

- GPU: NVIDIA RTX 3060 Laptop GPU (6 GB)
- Operating system: Ubuntu 22.04 under WSL2
- Python: 3.9.25
- PyTorch: 2.2.2+cu121
- CUDA runtime: 12.1
- Training environment: `gaitpart-p2`
- Training NumPy version: 1.23.5

The implementation uses the OpenGait framework, pinned to commit:

`4d228e154ae6f7473db49e0ef33493be0c137601`

### 2. Repository Setup

Clone the project repository:

```bash
git clone https://github.com/riship21/gait-recognition-project2.git
cd gait-recognition-project2
```

Retrieve the pinned OpenGait implementation:

```bash
git clone https://github.com/ShiqiYu/OpenGait.git third_party/OpenGait
cd third_party/OpenGait
git checkout 4d228e154ae6f7473db49e0ef33493be0c137601
cd ../..
```

The OpenGait implementation is stored locally in `third_party/OpenGait` and is excluded from the project's Git repository.

The software environment and required dependencies are documented in `docs/environment.md`. A fresh machine must have a working compatible PyTorch/CUDA environment before training.

### 3. Dataset Preparation

CASIA-B contains 124 subjects recorded under different walking conditions and camera viewpoints.

The project uses:

- Training subjects: 001–074
- Testing subjects: 075–124
- Silhouette resolution: 64 × 64
- Processed sequence count: 13,592

The official OpenGait subject partition is used.

CASIA-B must be obtained separately according to its access and licensing requirements.

The processed dataset is expected under:

`data/processed/CASIA-B-pkl-compatible/`

### 4. NumPy Compatibility Conversion

The original processed pickle files referenced NumPy 2.x internals.

A separate environment with NumPy 2.0.2 was used to export the arrays:

```bash
conda activate gaitpart-convert
python scripts/convert_casiab_numpy.py --stage export
```

The intermediate `.npy` files were then repackaged with NumPy 1.23.5:

```bash
conda activate gaitpart-p2
python scripts/convert_casiab_numpy.py --stage repack
```

This procedure preserves the original dataset and creates a NumPy 1.x-compatible copy.

**Note:** The commands assume the original processed pickle files already exist at the paths specified in the conversion script. Do not repeat conversion if the destination already exists.

### 5. Training Smoke Test

From the repository root:

```bash
cd third_party/OpenGait

CUDA_VISIBLE_DEVICES=0 torchrun \
  --standalone \
  --nproc_per_node=1 \
  opengait/main.py \
  --cfgs ../../configs/gaitpart_casiab_smoke.yaml \
  --phase train \
  --log_to_file
```

Verified outcome:

- Five successful iterations
- Batch composition: [2, 2]
- Checkpoint successfully saved

### 6. Training and Checkpoints

The project uses PyTorch distributed launching with one GPU.

Training configurations are stored in the project's `configs/` directory.

OpenGait saves checkpoints under:

`third_party/OpenGait/output/CASIA-B/GaitPart/<experiment_name>/checkpoints/`

The checkpoint contains:

- Model parameters
- Optimizer state
- Scheduler state
- Iteration counter

Resuming training requires matching the checkpoint experiment name and specifying the saved iteration using `trainer_cfg.restore_hint`.

Checkpoint restoration was verified by continuing the Batch64 experiment from iteration 50 to iteration 60.

### 7. Evaluation

The preliminary recognition evaluation used the checkpoint trained for 500 iterations.

From `third_party/OpenGait`:

```bash
CUDA_VISIBLE_DEVICES=0 torchrun \
  --standalone \
  --nproc_per_node=1 \
  opengait/main.py \
  --cfgs ../../configs/gaitpart_casiab_eval_test.yaml \
  --phase test \
  --log_to_file
```

For single-GPU evaluation, the inference sampler batch size must equal 1 in the pinned OpenGait implementation.

The evaluation uses Euclidean-distance matching and excludes identical-view comparisons.

Preliminary Rank-1 results:

| Condition | Accuracy |
|---|---:|
| NM | 48.49% |
| BG | 37.23% |
| CL | 14.07% |

These results are from the 500-iteration checkpoint, not the final trained model.

### 8. Reproduction Limitations

The reproduced experiment differs from the reference configuration in several ways:

- Training uses a smaller batch composition to accommodate GPU limitations.
- Some CASIA-B sequence folders contain missing or insufficient frames.
- NumPy compatibility conversion is necessary for the supplied processed data.
- OpenGait's saved checkpoints do not include mixed-precision GradScaler state.
- Bit-for-bit determinism across environments and resumed sessions has not been established.

These differences should be considered when comparing results with the original paper.

### 9. Experiment Tracking

A chronological record of experiments, observed failures, configuration changes, and results is maintained in:

`experiments/experiment_log.md`

Further investigations and final results will be added as training progresses.
