# author: James Liu
# date: 2020-01-18
#This script downloads .csv files for horse-racing data in Hong Kong from the user-defined URL
#then processes them and writes them to a user-specified location on the local machine
#as data_train.csv and data_test.csv. This script takes  the URL where the data is hosted
#and the location where the user would like the data to be written to locally.
data/raw_files/barrier.csv data/raw_files/comments.csv data/raw_files/horse_info.csv data/raw_files/results.csv data/raw_files/trackwork.csv:
	python src/download_data.py https://raw.githubusercontent.com/v5y8/horse_race_data/master data/raw_files


# author: Derek Kruszewski
# date: 2020-01-21
#This script imports raw .csv files for horse-racing data in Hong Kong from user-defined file-path,
#performs pre-preprocessing, merges the files together, and writes them to a user-specified location 
#on the local machine as data_train.csv and data_test.csv. This script takes the filepath where the raw
#data is saved and the location where the user would like the compiled data to be written to locally.
data/data_test.csv data/data_train.csv: data/raw_files/barrier.csv data/raw_files/comments.csv data/raw_files/horse_info.csv data/raw_files/results.csv data/raw_files/trackwork.csv
	python src/wrangle_data.py data/raw_files data


# author: Carlina Kim
# date: 2020-01-23
#This script creates exploratory data visualiztions and tables that help readers understand the Hong Kong horse racing data. 
img/age_dist.png img/correlation_plot.png img/country_dist.png img/heatmap_null.png img/weight_dist.png img/results_plot.png: data/data_test.csv data/data_train.csv
	python src/eda.py data img && Rscript src/plot.R data/data_train.csv img


# author: Rob Blumberg
# date: 2020-01-29
#This script runs a grid search over number of features to select using linear
#regression and recursive feature elimination. It then outputs the results as a .csv
#in the desired directory
data/results_data/grid_search_results.csv: data/data_train.csv
	python src/grid_search.py data/data_train.csv data/results_data/grid_search_results.csv


# author: Rob Blumberg
# date: 2020-01-25
#This script runs a pre-optimized linear regression model on training and test data.
#The linear regression model is trained with the training data, and then makes predictions
#on the test set. It then outputs as a .png plot in the desired directory showing predicted
#vs actual results.
img/results_plot.png: data/data_test.csv data/data_train.csv data/results_data/grid_search_results.csv
	python src/linear_model.py data/data_train.csv data/data_test.csv data/results_data/grid_search_results.csv img/results_plot.png



all: img/age_dist.png img/correlation_plot.png img/country_dist.png img/heatmap_null.png img/weight_dist.png img/results_plot.png data/data_train.csv data/data_test.csv
	Rscript -e "rmarkdown::render('doc/final_report.Rmd')"

clean:
	rm -f data/raw_files/*.csv
	rm -f data/*.csv
	rm -f doc/final_report.html
	rm -f doc/final_report.md
	rm -f data/results_data/grid_search_results.csv
