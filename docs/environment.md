# Project 2 Environment

## Repository Environment

Project 2 uses a dedicated Conda environment rather than the system
Python installation.

Environment name:

`gaitpart-p2`

Python:

`3.9`

## Development Machines

### Current Laptop

Purpose:

- documentation
- dataset auditing
- preprocessing
- result analysis
- Git/version control

This machine does not contain an NVIDIA CUDA GPU.

### GPU Laptop

An NVIDIA-equipped MSI GS66 will be used for:

- PyTorch CUDA setup
- GaitPart training
- checkpoint evaluation
- GPU-based experiments

The exact GPU, CUDA, PyTorch, and driver versions will be documented after
the GPU environment is configured.

## OpenGait

Repository:

`https://github.com/ShiqiYu/OpenGait`

Pinned commit:

`4d228e154ae6f7473db49e0ef33493be0c137601`

The OpenGait source is cloned locally under:

`third_party/OpenGait`

The directory is excluded from this repository because it is third-party
software.

The exact commit is recorded so that the same version can be retrieved
again.

## Current CPU Dependencies

Current preprocessing dependencies include:

- Python 3.9
- NumPy
- OpenCV
- tqdm
- PyYAML

PyTorch and CUDA dependencies will be documented after configuration of
the NVIDIA GPU machine.

## MSI GPU Environment

GPU machine:

- MSI GS66
- WSL2
- Ubuntu 22.04
- NVIDIA GeForce RTX 3060 Laptop GPU
- GPU memory: 6 GB
- NVIDIA driver: 552.12
- Windows-reported CUDA support: 12.4

Project environment:

- Conda environment: `gaitpart-p2`
- Conda: 26.3.2
- Python: 3.9.25
- PyTorch: 2.2.2+cu121
- PyTorch CUDA runtime: 12.1
- CUDA available in PyTorch: Yes

The processed CASIA-B dataset was transferred to the WSL filesystem.

Verified processed dataset:

- Subjects: 124
- Pickle sequences: 13,592

The next step is a short GaitPart smoke test before full training.