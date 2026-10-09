# Introduction to accelerated python

## Summary

This tutorial covers numpy, numba and cupy as approaches for improving the performance of scientific python code. The tutorial (without cell outputs) is in the Jupyter notebook 'intro_to_accelerated_python.ipynb'.

For a pre-run notebook with outputs from MeluXina already included, see 'PRERUN_intro_to_accelerated_python.ipynb'.

## Running the notebook

### MeluXina

To follow along with the live session (9 October 2026), the preferable option is to open the notebook on MeluXina:

1. Go to [LXP OnDemand](https://portal.lxp.lu/pun/sys/dashboard)
2. Choose "Jupyter Notebook"
3. Enter the following launch options:
    - Account: p201580
    - Partition: gpu
    - Number of Nodes: 1
    - QOS: dev
    - Reservation: gpudev
    - Timelimit: 02:00:00
    - Software Stack: env/release/2025.1
    - Built-in Modules to Load: PyTorch
    - Configure Python Environment?: Yes
    - MeluXina Preset Python Environment(s): None
    - Your Python Virtual Environment Path: /project/home/p201580/venvs/accelerated-python
4. Launch Jupyter notebook and wait for it to start
5. Clone this repository into your working directory on MeluXina (if you haven't already)
6. Open intro_to_accelerated_python.ipynb

### Other machines

If you want to run this notebook on a different machine, follow these instructions. These assume you have python and [uv](https://docs.astral.sh/uv/) installed.

1. Clone the repository onto your machine
2. Change into this directory
3. Install the python environment. This will depend on your system:
    - If you are on a system with CUDA and NVIDIA GPUs, check what version of CUDA you have (CUDA must already be installed/loaded before installing the python environment). run `uv sync --extra cuda12` if you have CUDA 12, or `uv sync --extra cuda13` if you have CUDA 13.
    - If you do not have NVIDIA GPUs, simply run `uv sync`. You will not be able to run the `cupy` part of the tutorial.
4. Launch jupyter lab: `uv run jupyter lab`
5. Open intro_to_accelerated_python.ipynb
