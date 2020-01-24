# DSCI 522 Group 302

## Dependencies
Our project uses the following libraries:
- [numpy](https://numpy.org/)
- [pandas](https://pandas.pydata.org/getpandas.html)
- [pandas-profiling](https://github.com/pandas-profiling/pandas-profiling)
- [docopt](https://github.com/docopt/docopt)
- [scikit-learn](https://scikit-learn.org/stable/install.html)

Please install these packages if you do not have them for optimal usage.

## Project proposal

### Research question and data source

The central research question we will set out to answer during this project is:

**Given a set of features related to racing horses, can we predict the outcome of a race?**

Thus, our research question is predictive, and the data we will use to attempt to answer our question is the _Hong Kong Horse Racing Dataset for Experts_, publicly available through kaggle:

https://www.kaggle.com/hrosebaby/horse-racing-dataset-for-experts-hong-kong

The data has been rehosted on github:

https://raw.githubusercontent.com/v5y8/horse_race_data/master

Please use the github repository for downloading with download_data.py.

### Analysis plan

In this project, we will be attempting to predict the order in which a set of horses will finish a race. Therefore, our labels will be ordinal, and we can produce a model which will return the class probabilities for each possible finishing position. Using these class probailities, we will be able to determine an expected finish value for each horse, which we can use to rank our racers. 

Machine learning is as much an empirical science as it is theoretical. As such, it is almost always impossible to say before hand which type of model will work best for a particular prediction task. Because of this, we plan to test several different models on our data set, including, but not limited to, generalized linear models, decision trees, random forests, naive Bayes classifiers and SVMs. We may even use ensemble methods to aggregate the predictions made by several different models. 

### EDA discussion

The kaggle horse racing data set used for this project contains five sub sets (.csv files): 'results', 'barrier', 'comments', 'horse_info', and 'trackwork'. Results contains horse racing placement information from official races (race outcomes, pre-race conditions). Comments contains text on the performance of each horse during official races, and horse_info contains specifications for the horses participating in races (features include name, country of origin, sex and age).

The barrier data set includes practice runs completed by horses. Since this information is useful in predicting future track performance it was included along with results as race observations. The results race data contains all the same features as the barrier set; however the barrier practice runs are missing ~20% of the features that are in results such as "actualwt", "class", and "handicap". In order to be able study if practice runs are biased, these practice runs are labelled in the final data set so that observations are known to be either an official race or practice.

Trackwork contains warmup and exercise routines for horses throughout the time period of the data set (2015-2017). This data set was tentatively omitted because it is difficult to incorpoate into the master data set. The set contains 648,000 rows.

Merging the above mentioned tables together, an EDA was performed on the compiled "final" data set:

https://github.com/UBC-MDS/DSCI_522_Group_302/blob/master/src/EDA.ipynb

Some major notes from the EDA are as follows:
- Training and test data sets are 18744 and 4687 observations respectively
- There are 36 features: 12 numeric, and 23 categorical
- The training data set contains 1962 horses
- At first review, some features appear correlated to placement such as: class, declarewt, and country. 

### Communication of results and final report

To communicate our final results, we will create tables and plots displaying our final model's predicted horse placement values, along with the actual placements from the test set. We could compare these values in a plot, along with a line representing a theoretically perfect model. This will be done by way of a Markdown report, which will make it easy to discuss and display our results, but more importantly, automate the embedding of images and plots from other scripts.

To visualize the differences between our (one or more depending on performance) models' predicted output of placement versus their actual placements in the test data, We could plot a scatter plot, with Predicted placement being the X axis and Actual placement being the Y axis, much like excercise 4 in lab 4 of Supervised Learning I.
![screenshot of plot](https://github.com/v5y8/DSCI_522_Group_302/raw/master/data/hypothetical_pred_vs_actual_plot.png)

If applicable, We could also plot a best-fit line via linear regression with respect to some of our most important features, much like the plots we generated for excercise 1 in lab 1 of Regression II.
![screenshot of residual plot](https://github.com/v5y8/DSCI_522_Group_302/raw/master/data/hypothetical_residual_plot.png)

Finally, we can generate a table of our best/worst x number of predictions, and present them in a table.

|Horse name|predicted placement | actual placement |difference |
|-----------|------------|------------|---------------------|
|Horse 1|1|1|0|
|Horse 2|1|1|0|
|Horse 3|1|1|0|
|Horse 4|1|1|0|

...

|Horse name|predicted placement | actual placement |difference |
|-----------|------------|------------|---------------------|
|Horse 10|1|10|9|
|Horse 11|1|11|10|
|Horse 12|1|12|11|
|Horse 13|1|13|12|

## Contributions
We welcome all contributions to this project! If you notice a bug, or have a feature request, please open up an issue [here](https://github.com/UBC-MDS/DSCI_522_Group_302/issues/new). If you'd like to contribute a feature or bug fix, you can fork our repo and submit a pull request. We will review pull requests within 7 days. All contributors must abide by our [code of conduct](https://github.com/v5y8/DSCI_522_Group_302/blob/master/CODE_OF_CONDUCT.md).
