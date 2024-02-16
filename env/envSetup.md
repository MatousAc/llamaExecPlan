# Environment Setup
## Recreate
This directory includes several complex environments. You should be able to use the various `.yml` files to create new conda environments. You need to [install conda from here](https://docs.anaconda.com/free/miniconda/) first.
```
conda create --name <envName> --file <envName>.yml
```
The two environments available in this folder are for the SoC GPUs and for a local (conda) python installation. The `cuda` version is for the SoC.

Here is an explanation of each saved environment:
### Current envs
* [qagHfCuda.yml](qagHfCuda.yml) - main environment to use for this repository and thesis. use this for training LLaMA 2 with the trainer, data formatter, data processor, and other scripts in the `src/` directory.
* [qagHf.yml](qagHf.yml) - the non-cuda, local version of the environment. should allow for data processing and inference based on the final model

## DB Setup
Use [sauAttendance.yml](sauAttendance.yml) to pull up a docker container of SQL Server locally. Instructions for running are in [sauAttendance.yml](sauAttendance.yml).

## Start from scratch
Otherwise start a conda environment from scratch with:

```
conda create -n aqg
conda activate aqg
conda install python=3.11.5
```

Install the python packages that you need.

For optimum and t5:
```
pip install datasets evaluate fastt5 huggingface kaggle pandas numpy onnx onnxruntime optimum tokenizers torch transformers nltk
```

For LLaMA 2 training:
```
pip install datasets evaluate huggingface numpy pandas transformers tokenizers torch
```

