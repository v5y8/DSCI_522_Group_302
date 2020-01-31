#!/usr/bin/env bash

# setup.sh
# James Liu, Jan 2020

# This script runs all of the necessary download, analysis and wrangling scripts and generates a markdown report from
# an .Rmd file.


# example usage:
# bash setup.sh


# download the data
printf "============\nstarting download script\n"
python src/download_data.py https://raw.githubusercontent.com/v5y8/horse_race_data/master data/raw_files
printf "============\nfinished download script\n"

# wrangle the data
printf "============\nstarting data wrangling\n"
python src/wrangle_data.py data/raw_files data
printf "============\nfinished data wrangling\n"

# EDA script
printf "============\nstarting EDA analysis\n"
python src/eda.py data img
Rscript src/plot.R data/data_train.csv img
printf "============\nfinished EDA analysis\n"

# train and fit model
printf "============\nstarting training model\n"
python src/linear_model.py data/data_train.csv data/data_test.csv img/results_plot.png
printf "============\nfinished training model\n"

# render R markdown
printf "============\nstarting rendering report\n"
Rscript -e "rmarkdown::render('doc/final_report.Rmd')"
printf "============\nfinished rendering report\n"

printf "============\nfinished running pipeline, exiting\n"
