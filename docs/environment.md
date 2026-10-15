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