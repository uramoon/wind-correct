# Post-Processing Maritime Wind Forecasts from the European Centre for Medium-Range Weather Forecasts around the Korean Peninsula Using Support Vector Regression and Principal Component Analysis

This repository contains the official implementation of "Post-Processing Maritime Wind Forecasts from the European Centre for Medium-Range Weather Forecasts around the Korean Peninsula Using Support Vector Regression and Principal Component Analysis" by Seung-Hyun Moon, Do-Youn Kim, and Yong-Hyuk Kim.

If you use this code for your research please considier citing the paper: 

    @Article{Moon2024Post-Processing,
        AUTHOR = {Moon, Seung-Hyun and Kim, Do-Youn and Kim, Yong-Hyuk},
        TITLE = {Post-Processing Maritime Wind Forecasts from the European Centre for Medium-Range Weather Forecasts around the Korean Peninsula Using Support Vector Regression and Principal Component Analysis},
        JOURNAL = {Journal of Marine Science and Engineering},
        VOLUME = {12},
        YEAR = {2024},
        NUMBER = {8},
        ARTICLE-NUMBER = {1360},
        URL = {https://www.mdpi.com/2077-1312/12/8/1360},
        ISSN = {2077-1312},
        DOI = {10.3390/jmse12081360}
    }

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
python correct.py MODEL_NO STATION_NO YYYYMMDD
# e.g, python correct.py 22105 22190 20220603
```
