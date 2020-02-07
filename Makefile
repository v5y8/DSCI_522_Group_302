# Driver Script
# Author: James Liu / Derek Kruszewski
# Date: 2020-01-31 (Updated 2020-02-04)
# This script downloads, wrangles, data explores, feature selects, and generates a model to predict
# horse race times from a horse race data set.

all: doc/final_report.md doc/final_report.html

# Download raw data
data/raw_files/barrier.csv data/raw_files/comments.csv data/raw_files/horse_info.csv data/raw_files/results.csv data/raw_files/trackwork.csv: src/download_data.py
	python src/download_data.py https://raw.githubusercontent.com/v5y8/horse_race_data/master data/raw_files

# Create test/train data
data/data_test.csv data/data_train.csv: data/raw_files/barrier.csv data/raw_files/comments.csv data/raw_files/horse_info.csv data/raw_files/results.csv data/raw_files/trackwork.csv src/wrangle_data.py
	python src/wrangle_data.py data/raw_files data

# Create exploratory data analysis figures using python
img/age_dist.png img/correlation_plot.png img/country_dist.png img/heatmap_null.png img/weight_dist.png: data/data_train.csv src/eda.py
	python src/eda.py data img 

# Create exploratory data analysis figures using R
img/numeric_placement.png: data/data_train.csv src/plot.R
	Rscript src/plot.R data/data_train.csv img

# Select features and output grid search results
data/results_data/grid_search_results.csv: data/data_train.csv src/grid_search.py
	python src/grid_search.py data/data_train.csv data/results_data/grid_search_results.csv

# Output results figure from fitted linear model
img/results_plot.png: data/data_test.csv data/data_train.csv data/results_data/grid_search_results.csv src/linear_model.py
	python src/linear_model.py data/data_train.csv data/data_test.csv data/results_data/grid_search_results.csv img/results_plot.png

# Render final report
doc/final_report.md doc/final_report.html: img/age_dist.png img/correlation_plot.png img/country_dist.png img/heatmap_null.png img/weight_dist.png img/numeric_placement.png img/results_plot.png data/results_data/grid_search_results.csv doc/final_report.Rmd
	Rscript -e "rmarkdown::render('doc/final_report.Rmd')"

# Clean up files
clean:
	rm -f data/raw_files/*.csv
	rm -f data/*.csv
	rm -f data/results_data/grid_search_results.csv
	rm -f doc/final_report.html
	rm -f doc/final_report.md
	rm -f img/age_dist.png
	rm -f img/correlation_plot.png
	rm -f img/country_dist.png
	rm -f img/heatmap_null.png
	rm -f img/weight_dist.png
	rm -f img/numeric_placement.png
	rm -f img/results_plot.png