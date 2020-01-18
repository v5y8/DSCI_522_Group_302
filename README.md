# DSCI 522 Group 302

## Project proposal

### Research question and description of data 

The central research question we will set out to answer during this project is:

**Given a set of features related to racing horses, can we predict the outcome of a race?**

Thus, our research question is predictive, and the data we will use to attempt to answer our question is the _Hong Kong Horse Racing Dataset for Experts_, publicly available through kaggle. In particular, we will be using the _results_ and _horse_info_ tables.

As its name suggests, the _horse_info_ dataset contains features describing the horses themselves. These features include name, country of origin, sex and age. The _results_ dataset consists of a table describing the outcome of various races. It shows the horses who participated in each race, along with several features describing both the pre-race conditions and the actual race outcomes. These include the pre-race odds, the final race times, the distance of the races, and the position of each horse thoughout the race. A more in-depth exploration of the data can be found in the EDA jupyter notebooks, located in the src directory of this repository. The main findings from the EDA are also discussed in the EDA section further down in this README.

### Analysis plan

In this project, we will be attempting to predict the order in which a set of horses will finish a race. Therefore, our labels will be ordinal, and we can produce a model which will return the class probabilities for each possible finishing position. Using these class probailities, we will be able to determine an expected finish value for each horse, which we can use to rank our racers. 

Machine learning is as much an empirical science as it is theoretical. As such, it is almost always impossible to say before hand which type of model will work best for a particular prediction task. Because of this, we plan to test several different models on our data set, including, but not limited to, generalized linear models, decision trees, random forests, naive Bayes classifiers and SVMs. We may even use ensemble methods to aggregate the predictions made by several different models. 

### Communication of results and final report

To communicate our final results, we will create tables and plots displaying our final model's predicted horse placement values, along with the actual placements from the test set. We could compare these values in a plot, along with a line representing a theoretically perfect model. This will be done by way of a Markdown report, which will make it easy to discuss and display our results, but more importantly, automate the embedding of images and plots from other scripts.

### EDA discussion
