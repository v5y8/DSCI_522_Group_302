# author: Rob Blumberg
# date: 2020-01-25
#

"""This script runs a grid search over number of features to select using linear
regression and recursive feature elimination. It then outputs the results as a .csv
in the desired directory.

Usage: grid_search.py <training_data_file_path> <gridsearch_results_file_path>

Arguments:
<training_data_file_path>            File path where training data is stored
<gridsearch_results_file_path>       File path to save table of grid search results
"""
from docopt import docopt

import pandas as pd
import numpy as np

from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.preprocessing import OneHotEncoder, PolynomialFeatures
import re
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer

from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.feature_selection import RFE
from sklearn.linear_model import LinearRegression

import matplotlib.pyplot as plt

opt = docopt(__doc__)

def main(training_data_file_path, gridsearch_results_file_path):
    """
    Entry point for script. Takes in training_data_file_path and image_plot_file_path from commandline, 
    and runs a  gridsearch using recusrive feature elimination and linear regression.

    Arguments:
    ----------
    training_data_file_path 
        - file path where training data is located. Assumes data is a .csv file in same
        format as data/data_train.csv (output of download_data.py script)
    gridsearch_results_file_path
        - file path where image of results plot will be saved

    Returns:
    -------
        None, but saves a table to the specified file path
    """
    grid_search(training_data_file_path, gridsearch_results_file_path)

def time_parser(input_time):
    """
    Function which converts a time string of form mm.ss.SS to seconds
    
    Arguments:
    ----------
    input_time 
        (str) - input time as string of form "d.dd.dd" where d is a digit

    Returns:
    --------
    float representing input time in seconds
    """
    assert re.match("\d\.\d{2}\.\d{2}", input_time), "Only strings of format d.dd.dd can be parsed"

    parsed_time = input_time.split(".")
    mins = int(parsed_time[0])
    secs = int(parsed_time[1])
    ss = int(parsed_time[2])
    
    time_in_sec = mins*60.0 + secs + ss/100
    return time_in_sec

def load_and_parse_data(training_data_file_path):
    """
    Data loading and cleaning function. Converts finishtime column to seconds
    and drops rows where finishtime is 0. 

    Arguments:
    ----------
    training_data_file_path 
        - file path where training data is located. Assumes data is a .csv file in same
        format as data/data_train.csv (output of download_data.py script)

    Returns:
    -------
    X_train, y_train 
        (np.array) - Cleaned training set
    """

    training_data = pd.read_csv(training_data_file_path)

    assert "finishtime" in training_data.columns, "Missing column 'finishtime'"

    y_train = training_data["finishtime"]
    #fill nans with "0.00.00"
    y_train.fillna("0.00.00", inplace=True)       
    #replace anything not of format d.dd.dd to "0.00.00" with time_parser function
    y_train[~y_train.str.contains("\d\.\d{2}\.\d{2}")] = '0.00.00'
    #  apply time_parser on all values
    y_train = np.array(list(map(lambda x: time_parser(x), y_train)))
    #replace target column with converted values
    training_data["finishtime"] = y_train
    #drop all rows where finishtime is 0.0
    training_data = training_data[training_data["finishtime"] != 0.0]
    X_train = training_data.drop("finishtime", axis=1)
    y_train = training_data["finishtime"]

    return X_train, y_train

def data_preprocessing(training_data_file_path):
    """
    Data preprocessing for linear regression. Applies imputer (mean), 
    and polynomial order 5 tranformation to numeric features. Applies 
    imputer (fill with "not_specified" constant value) and one-hot encoding
    to categorical features. Uses output of load_and_parse_data() function.

    Arguments:
    ----------
    training_data_file_path 
        - file path where training data is located. Assumes data is a .csv file in same
        format as data/data_train.csv (output of download_data.py script)

    Returns
    -------
    X_train_preprocessed, y_train
        (np.array) - Preprocessed training features and targets
    """

    X_train, y_train = load_and_parse_data(training_data_file_path)

    assert all([x in X_train.columns for x in ["country", "dataset"]]), "Must have colums 'country', 'dataset'"
    assert all([x in X_train.columns for x in ["declarwt", "age", "winodds", "stake", "distance"]]), "Must have colums 'declarwt', 'age', 'winodds', 'stake', 'distance'"
    
    #define preprocessor for numeric features
    numeric_transformer = Pipeline(steps=[('imputer', SimpleImputer(strategy='mean')),
                                          ('poly', PolynomialFeatures(degree=5))
                                         ])

    #define preprocessor for categorical features
    categorical_transformer = Pipeline(steps=[('imputer', SimpleImputer(strategy='constant', fill_value="not_specified")),
                                              ('one_hot_encoder',  OneHotEncoder())
                                             ])

    #combine numeric and categorical pipelines
    categorical_features = ["country", "dataset"]
    numeric_features = ["declarwt", "age", "winodds", "stake", "distance"]

    preprocessing = ColumnTransformer(
                                 transformers=[
                                    ('num', numeric_transformer, numeric_features),
                                    ('cat', categorical_transformer, categorical_features)
                                              ])

    #combine preprocessing and model fitting steps into one pipeline 
    full_pipeline = Pipeline([
        ('data_preprocessing', preprocessing),
    ])

    X_train_preprocessed = full_pipeline.fit_transform(X_train)
    
    return X_train_preprocessed, y_train

def grid_search(training_data_file_path, gridsearch_results_file_path):
    """
    Function which performs grid search for number of features to select using RFE and linear regression.

    Arguments:
    ----------
    training_data_file_path 
        - file path where training data is located. Assumes data is a .csv file in same
        format as data/data_train.csv (output of download_data.py script)
    gridsearch_results_file_path
        - file path where image of results plot will be saved

    Returns:
    -------
        None, but saves a table to the specified file path
    """

    X_train_preprocessed, y_train = data_preprocessing(training_data_file_path)
    
    assert X_train_preprocessed.shape[0] > 30, "Training set must have at least 30 columns"

    param_grid = [{
    "n_features_to_select" : [10, 12, 15, 18, 20, 22, 25, 28, 30]
    }]

    gridsearch = GridSearchCV(RFE(LinearRegression()), param_grid=param_grid, cv=5, scoring="r2")
    gridsearch.fit(X_train_preprocessed, y_train)
    grid_search_results = pd.DataFrame({"n_features_to_select" : param_grid[0]["n_features_to_select"], 
                                        "mean_val_score (r2)" : gridsearch.cv_results_["mean_test_score"],
                                        "fit time per fold (s)" : gridsearch.cv_results_["mean_fit_time"]})
    
    grid_search_results = grid_search_results.sort_values("mean_val_score (r2)", ascending=False)

    grid_search_results.to_csv(gridsearch_results_file_path)


# script entry point
if __name__ == '__main__':
    main(opt["<training_data_file_path>"], opt["<gridsearch_results_file_path>"])