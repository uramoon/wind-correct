# Post-processing ECMWF Maritime Wind Forecasts around the Korean Peninsula Using SVR and PCA

This repository contains the official implementation of "Post-processing ECMWF Maritime Wind Forecasts around the Korean Peninsula Using SVR and PCA" by Seung-Hyun Moon, Do-Youn Kim, and Yong-Hyuk Kim.

If you use this code for your research please considier citing the paper: TBD

## How to run the code

### Run training
The "data" folder must contain the observations and ECMWF forecasts for the training locations. Please refer to the included sample for the correct format. The trained model is saved in the "model" folder.
```bash
python train.py STATION_NO
# e.g, python train.py 22105
```

### Run correction
The "model" folder must contain the model, and the "input" folder must contain the observations and ECMWF forecasts for the trained locations. Please refer to the included sample for the correct format.
```bash
python correct.py MODEL_FILE STATION_NO YYYYMMDD
# e.g, python correct.py 22105.p 22190 20220607
```
