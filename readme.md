# Environment Setup
## Recreate
This directory includes several complex environments. You should be able to use the various `.yml` files to create new conda environments. You need to [install conda from here](https://docs.anaconda.com/free/miniconda/) first.
```
conda create --name <envName> --file <envName>.yml
```
The two environments available in this folder are for the SoC GPUs and for a local (conda) python installation. The `cuda` version is for the SoC GPUs. Note that you may have to install some cuda toolkit software before the environment installs correctly.

Here is an explanation of each saved environment:
### Current envs
* [llamaInferenceCuda.yml](env/llamaInferenceCuda.yml) - main environment to use for inference. use this when you run [inferer.py](src/inferer.py)
* [llamaInference.yml](env/llamaInference.yml) - the non-cuda, local version of the environment. should allow for data processing and running of various scripts for this project

# Running inference
To run the model just interpret [inferer.py](src/inferer.py). You will be in an inference loop. If in prompt generation mode, all you have to do is press enter to prompt the model.

The configuration for the project is in [config.ini](src/config.ini). This file determines the current model source, data source, and inference prompt used. Data && logs are kept in the [data](data/) folder.

# DB Setup
* Use [sauAttendance.yml](env/sauAttendance.yml) to pull up a docker container of SQL Server locally. Instructions for running are in [sauAttendance.yml](sauAttendance.yml).
* Not sure yet what to do from here.

# Report
The latex for the report is located in the [report](report/) folder. The main files are in [report](report/) while all the report content is divided into section in the [setions](report/sections/) folder. All supporting articles and research lives in the [research](research/) folder. [resources](resources/) is for miscellaneous project resources.
