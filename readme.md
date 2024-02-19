# Environment Setup
## Recreate
This directory includes several complex environments. You should be able to use the various `.yml` files to create new conda environments. You need to [install conda from here](https://docs.anaconda.com/free/miniconda/) first.
```
conda create --name <envName> --file <envName>.yml
```
The two environments available in this folder are for the SoC GPUs and for a local (conda) python installation. The `cuda` version is for the SoC.

Here is an explanation of each saved environment:
### Current envs
* [llamaInferenceCuda.yml](env/llamaInferenceCuda.yml) - main environment to use for this repository and thesis. use this for training LLaMA 2 with the trainer, data formatter, data processor, and other scripts in the `src/` directory.
* [llamaInference.yml](env/llamaInference.yml) - the non-cuda, local version of the environment. should allow for data processing and inference based on the final model

## Start from scratch
Try not to choose this option, it has not been updated in a while.
Otherwise start a conda environment from scratch with:

```
conda create -n llamaInference
conda activate llamaInference
conda install python=3.11.5
```

Install the python packages that you need.

For LLaMA 2 training:
```
pip install datasets evaluate huggingface numpy pandas transformers tokenizers torch
```

# Running inference
To run the model just interpret [inferer.py](src/inferer.py). You will be in an inference loop.

The configuration for the project is in [config.ini](src/config.ini), and the data will be kept in the [data](data/) folder.

# DB Setup
* Use [sauAttendance.yml](env/sauAttendance.yml) to pull up a docker container of SQL Server locally. Instructions for running are in [sauAttendance.yml](sauAttendance.yml).
* 

# Report
The latex for the report is located in the [report](report/) folder, and all supporting articles and research lives in the [research](research/) folder. [resources](resources/) is for miscellaneous project resources.
