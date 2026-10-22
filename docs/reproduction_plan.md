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


## Final Verified Experiments and Reproduction Commands

### Software Environment

The project's Conda environment is exported in:

`environment.yml`

The environment was verified with:

- Python 3.9.25
- PyTorch 2.2.2+cu121
- NumPy 1.23.5
- CUDA 12.1 runtime
- NVIDIA RTX 3060 Laptop GPU

To recreate the environment, start with:

```bash
conda env create -f environment.yml
conda activate gaitpart-p2
```

The exported environment includes CUDA-specific PyTorch wheel versions. If Conda cannot resolve those packages through the configured package sources, install the compatible PyTorch 2.2.2 and torchvision 0.17.2 CUDA 12.1 builds using the appropriate PyTorch wheel index.

The environment export documents the working package versions, but recreation on a fresh machine has not been independently verified.

### Final GaitPart Training Configuration

The main reproduction experiment used:

- Dataset: CASIA-B
- Training subjects: 001–074
- Model: GaitPart
- Batch composition: [4, 8]
- Optimizer: Adam
- Learning rate: 0.0001
- Triplet-loss margin: 0.2
- Mixed precision: Enabled
- Completed training iterations: 30,000

The experiment differs from the reference 120,000-iteration configuration because of available hardware and project constraints.

The first 10,000 iterations used:

`configs/gaitpart_casiab_full.yaml`

The remaining iterations resumed from the 10,000 checkpoint using:

`configs/gaitpart_casiab_30000.yaml`

From the OpenGait directory:

```bash
CUDA_VISIBLE_DEVICES=0 torchrun \
  --standalone \
  --nproc_per_node=1 \
  opengait/main.py \
  --cfgs ../../configs/gaitpart_casiab_30000.yaml \
  --phase train \
  --log_to_file
```

This resume command requires the existing iteration-10,000 checkpoint.

### Evaluate the 30,000-Iteration Checkpoint

From the repository root:

```bash
cd third_party/OpenGait
```

Run:

```bash
CUDA_VISIBLE_DEVICES=0 torchrun \
  --standalone \
  --nproc_per_node=1 \
  opengait/main.py \
  --cfgs ../../configs/gaitpart_casiab_eval_30000.yaml \
  --phase test \
  --log_to_file
```

Verified Rank-1 results, excluding identical-view comparisons:

| Condition | Accuracy |
|---|---:|
| Normal walking (NM) | 94.20% |
| Carrying a bag (BG) | 87.19% |
| Clothing variation (CL) | 73.03% |

### Matched GEI vs. GaitPart Evaluation

For the controlled 90-degree normal-walking comparison, both methods used CASIA-B subjects 075–124, gallery sequences `nm-01` through `nm-04`, and probe sequences `nm-05` and `nm-06`.

The GEI baseline achieved 95.00% Rank-1 accuracy.

The GaitPart model achieved 100.00% Rank-1 accuracy.

All 300 intended GaitPart gallery and probe sequences were confirmed present.

The matched-view reporting modification is provided as:

`patches/gaitpart_matched_90.patch`

To apply it to a clean checkout of the pinned OpenGait implementation, from the Project 2 root:

```bash
git -C third_party/OpenGait apply \
  ../../patches/gaitpart_matched_90.patch
```

The patch must not be applied twice. It adds reporting for the 90° → 90° Rank-1 result without changing GaitPart's identification calculations.

### Temporal Sequence-Length Ablation

The same 30,000-iteration checkpoint was evaluated under four inference-frame settings:

| Maximum frames | NM | BG | CL |
|---|---:|---:|---:|
| 15 | 63.99% | 54.19% | 42.32% |
| 30 | 86.25% | 76.34% | 62.16% |
| 50 | 91.77% | 84.22% | 70.13% |
| Unlimited | 94.20% | 87.19% | 73.03% |

To reproduce the limited-frame evaluations, run from `third_party/OpenGait`:

```bash
for frames in 15 30 50; do
    CUDA_VISIBLE_DEVICES=0 torchrun \
      --standalone \
      --nproc_per_node=1 \
      opengait/main.py \
      --cfgs ../../configs/gaitpart_casiab_ablation_${frames}frames.yaml \
      --phase test \
      --log_to_file
done
```

The ablation uses OpenGait's `frames_all_limit` setting, which selects the first N available frames from each sequence. Sequences shorter than the limit retain their available frames.

The experiment demonstrates the effect of temporal input truncation but does not isolate individual architectural components.

### Experiment Outputs

Structured experimental results are preserved in:

- `results/tables/temporal_ablation.csv`
- `results/tables/training_stage_results.csv`
- `results/tables/matched_model_comparison.csv`
- `results/tables/gei_matched_predictions.csv`
- `results/tables/gei_matched_summary.json`

The complete chronological experiment record is maintained in:

`experiments/experiment_log.md`

### Checkpoint Availability

Model checkpoints are stored locally under:

`third_party/OpenGait/output/CASIA-B/GaitPart/`

They are excluded from the Git repository due to file size.

Reproducing the checkpoint-dependent evaluations requires training the model using the documented configurations or obtaining the corresponding checkpoint separately.

### Reproduction Limitations

The final experiment used 30,000 rather than 120,000 reference iterations, a smaller training batch, and a single RTX 3060 GPU.

The environment export has not been tested on a fresh machine. Results may also vary across hardware and software environments.

The project provides the configurations, source code, experiment records, and result tables needed to inspect and reproduce the methodology.