"""This script runs a pre-optimized linear regression model on training and test data.
The linear regression model is trained with the training data, and then makes predictions
on the test set. It then outputs as a .png plot in the desired directory showing predicted
vs actual results.


Usage: linear_model.py <training_data_file_path> <test_data_file_path> <image_plot_file_path>

Arguments:
<training_data_file_path>   File path where training data is stored
<test_data_file_path>       File path where test data is stored
<image_plot_file_path>      File path to save image of results plot
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



def main(training_data_file_path, test_data_file_path, image_plot_file_path):
    """
    Entry point for script. Takes in training_data_file_path, test_data_file_path
    and image_plot_file_path from commandline, and runs a pre-optimized linear regression
    model. 

    Arguments:
    ----------
    training_data_file_path 
        - file path where training data is located. Assumes data is a .csv file in same
        format as data/data_train.csv (output of download_data.py script)
    test_data_file_path 
       - file path where training data is located. Assumes data is a .csv file in same
        format as data/data_train.csv (output of download_data.py script)
    image_plot_file_path
        - file path where image of results plot will be saved

    Returns
    -------
        None, but saves a plot to the specified file path
    """
    plot_results(training_data_file_path, test_data_file_path, image_plot_file_path)

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

def load_and_parse_data(training_data_file_path, test_data_file_path):
    """
    Data loading and cleaning function. Converts finishtime column to seconds
    and drops rows where finishtime is 0. 

    Arguments:
    ----------
    training_data_file_path 
        - file path where training data is located. Assumes data is a .csv file in same
        format as data/data_train.csv (output of download_data.py script)
    test_data_file_path 
       - file path where training data is located. Assumes data is a .csv file in same
        format as data/data_train.csv (output of download_data.py script)

    Returns
    -------
    X_train, X_test, y_train, y_test 
        (np.array) - Split training/test features and targets
    """

    training_data = pd.read_csv(training_data_file_path)
    test_data = pd.read_csv(test_data_file_path)

    assert "finishtime" in training_data.columns and "finishtime" in test_data.columns, "Missing column 'finishtime'"

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


    y_test = test_data["finishtime"]
    #fill nans with "0.00.00"
    y_test.fillna("0.00.00", inplace=True)       
    #replace anything not of format d.dd.dd to "0.00.00" with time_parser function
    y_test[~y_test.str.contains("\d\.\d{2}\.\d{2}")] = '0.00.00'
    #  apply time_parser on all values
    y_test = np.array(list(map(lambda x: time_parser(x), y_test)))
    #replace target column with converted values
    test_data["finishtime"] = y_test
    #drop all rows where finishtime is 0.0
    test_data = test_data[test_data["finishtime"] != 0.0]
    X_test = test_data.drop("finishtime", axis=1)
    y_test = test_data["finishtime"]

    return X_train, X_test, y_train, y_test

def data_preprocessing(training_data_file_path, test_data_file_path):
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
    test_data_file_path 
       - file path where training data is located. Assumes data is a .csv file in same
        format as data/data_train.csv (output of download_data.py script)

    Returns
    -------
    X_train_preprocessed, X_test_preprocessed, y_train, y_test 
        (np.array) - Preprocessed training/test features and targets
    """

    X_train, X_test, y_train, y_test = load_and_parse_data(training_data_file_path, test_data_file_path)

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
    X_test_preprocessed = full_pipeline.transform(X_test)
    
    return X_train_preprocessed, X_test_preprocessed, y_train, y_test

def linear_model_results(training_data_file_path, test_data_file_path):
    """
    Fits pre-optimized linear regression model on training data,
    and makes predictions on test data. Uses output of 
    data_preprocessing() function.

    Arguments:
    ----------
    training_data_file_path 
        - file path where training data is located. Assumes data is a .csv file in same
        format as data/data_train.csv (output of download_data.py script)
    test_data_file_path 
       - file path where training data is located. Assumes data is a .csv file in same
        format as data/data_train.csv (output of download_data.py script)

    Returns
    -------
    test_results 
        (pd.DataFrame) - Data frame containing test set predictions and actual values
    """
    
    X_train_preprocessed, X_test_preprocessed, y_train, y_test = data_preprocessing(training_data_file_path, test_data_file_path)
    rfe = RFE(LinearRegression(), n_features_to_select=25)
    rfe.fit(X_train_preprocessed, y_train)

    lr = LinearRegression()
    lr.fit(rfe.transform(X_train_preprocessed), y_train)

    test_results = pd.DataFrame({"Actual finish time" : y_test,
                                "Predicted finish time" : lr.predict(rfe.transform(X_test_preprocessed))})
    return test_results

def plot_results(training_data_file_path, test_data_file_path, image_plot_file_path):
    """
    Plots results from linear regression on test set. Uses output of 
    linear_model_results() function. Saves plot to specified file path.

    Arguments:
    ----------
    training_data_file_path 
        - file path where training data is located. Assumes data is a .csv file in same
        format as data/data_train.csv (output of download_data.py script)
    test_data_file_path 
       - file path where training data is located. Assumes data is a .csv file in same
        format as data/data_train.csv (output of download_data.py script)
    image_plot_file_path
        - file path where image of results plot will be saved

    Returns
    -------
    None
    """
    
    test_results=linear_model_results(training_data_file_path, test_data_file_path)

    fig, ax = plt.subplots(1, 1, figsize = (8 ,8))
    ax.scatter(test_results["Predicted finish time"], test_results["Actual finish time"])
    ax.plot([min(test_results["Actual finish time"]), max(test_results["Actual finish time"])],
            [min(test_results["Actual finish time"]), max(test_results["Actual finish time"])], 
            linestyle = "--", color = "red")
    ax.set_xlabel("Predicted finish time", size=14)
    ax.set_ylabel("Actual finish time", size=14)
    ax.set_title("Actual vs predicted finish times \non test set from optimized linear model", size = 15)
    plt.savefig(image_plot_file_path)

# script entry point
if __name__ == '__main__':
    main(opt["<training_data_file_path>"], opt["<test_data_file_path>"], opt["<image_plot_file_path>"])