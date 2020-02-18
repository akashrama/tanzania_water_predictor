# tanzania_water_predictor
Classification model predicting the function of water pumps throughout Tanzania

# Notebooks

To explore my work, please see the /notebooks/exploratory directory where you will find one notebook for the data cleaning and egineering process, and one notebook for each ML algoritim I implmented. 

# Project Replication
If you wish to recreate my results, clone this repo and follow the following steps:

## Setup Instructions

To download the necessary data, please run the following command:

```bash
# installs necessary requirements and downloads necessary data
sh setup.sh
```

### `tanz-water` conda environment

This project relies on you using the [`environment.yml`](environment.yml) file to recreate the `tanz-water` conda environment. To do so, please run the following commands:

```bash
# create the tanz-water conda environment
# note: this make take anywhere from 10-20 minutes
conda env create -f environment.yml

# activate the tanz-water conda environment
conda activate tanz-water

# make tanz-water available to you as a kernel in jupyter
python -m ipykernel install --user --name tanz-water --display-name "Python (tanz-water)"
```
