#!/home/dkruszew/anaconda3/bin/python
# -*- coding: utf-8 -*-
# author: Derek Kruszewski
# date: 2020-01-21
#

"""This script imports raw .csv files for horse-racing data in Hong Kong from user-defined file-path,
performs pre-preprocessing, merges the files together, and writes them to a user-specified location 
on the local machine as data_train.csv and data_test.csv. This script takes the filepath where the raw
data is saved and the location where the user would like the compiled data to be written to locally.

Usage: wrangle_data.py <file_path_in> <file_path_out>

Arguments:
<file_path_in>   Path where the raw data exists.
<file_path_out>  Path where the compiled data is to be written to locally.
"""

import numpy as np
import pandas as pd
from docopt import docopt
from sklearn.model_selection import train_test_split

opt = docopt(__doc__)


def main(file_path_in, file_path_out):
    """
    entry point for script. take in raw data file_path and output file_path from commandline,
     and warngles data for downstream use.
    Parameters
    ----------
    file_path_in
        the location where the raw data is hosted. Assumes that the folder contains 5 files:
            - horse_info.csv
            - results.csv
            - trackwork.csv
            - barrier.csv
            - comments.csv
    file_path_out
        - the desired filepath to put the wrangled data into.

    Returns
    -------
        None if executed successfully, otherwise raises Exception.
    """
    horse_info, results, comments, trackwork, barrier = import_files(file_path_in)
    complete_dataset = merge_results(horse_info, results, comments, trackwork, barrier)
    split_and_write_data(complete_dataset, file_path_out)
    print(f"successfully written data to {file_path_out}!\n")


def import_files(filepath):
    """
    imports the relevant csvs from the filepath specified.
    Parameters
    ----------
    filepath
        the filepath where the raw csv files live at.

    Returns
        five Pandas DataFrames
            - horse_info
            - results
            - comments
            - trackwork
            - barrier
    -------

    """
    print("==========\nstarting import...\n")
    horse_info = pd.read_csv(f"{filepath}/horse_info.csv", index_col=0)
    results = pd.read_csv(f"{filepath}/results.csv", index_col=0)
    comments = pd.read_csv(f"{filepath}/comments.csv", index_col=0)
    trackwork = pd.read_csv(f"{filepath}/trackwork.csv", index_col=0)
    barrier = pd.read_csv(f"{filepath}/barrier.csv", index_col=0)
    print("==========\nsuccessfully imported CSV data!\n")
    return horse_info, results, comments, trackwork, barrier


def merge_results(horse_info, results, comments, trackwork, barrier):
    """
    returns a merged dataframe of relevant .csv files.
    Parameters
    ----------
    horse_info
        dataframe holding horse info.
    results
        dataframe holding race results.
    comments
        dataframe holding comments for race.
    trackwork
        dataframe holding track work information.
    barrier
        dataframe holding barrier trial results.

    Returns
    -------
        a Pandas dataframe containing relevants input dataframes.

    """
    print("==========\nstarting merge...\n")
    # Merge comments onto results
    results['dataset'] = 'results'
    results_comments = pd.merge(results, comments, how="left", on=["horseno", "date", "raceno", "plc"])
    # Rename barrier time which is the same as finish time in results
    barrier.rename(columns={'time': 'finishtime'}, inplace=True)
    barrier['dataset'] = 'barrier'
    # Merge barrier onto results_comments
    barrier_binded = pd.concat([results_comments, barrier], axis = 0, ignore_index=False, sort=False)
    # Merge horse_info onto data frame
    merged_data = pd.merge(barrier_binded, horse_info, how='left', on=['horse'])
    # Removed the columns with _ch as this indicated Chinese.
    final_data = merged_data[merged_data.columns[~merged_data.columns.str.contains('.*_ch')]]
    # Drop repeated columns and unnessary indexes
    final_data = final_data.drop(['trainer_y'], axis=1)
    final_data['date'] = pd.to_datetime(final_data['date'])
    print("==========\ncompleted merge!\n")

    return final_data


def split_and_write_data(final_data, filepath):
    """
    splits the data into a train and test sets with a 8/2 split, then writes them to the specified file path.
    Parameters
    ----------
    final_data
        the dataframe containing the merged data
    filepath
        the user-specified filepath

    Returns
    -------
        None
    """
    print("==========\nstarting to split data into test and train sets\n")
    # shuffle and split the data.
    data_train, data_test = train_test_split(final_data,
                                             random_state=1,
                                             test_size=0.2,
                                             shuffle=True)
    print("==========\ndata is split, writing to file\n")
    data_train.to_csv(f"{filepath}/data_train.csv")
    data_test.to_csv(f"{filepath}/data_test.csv")

# script entry point
if __name__ == '__main__':
    main(opt["<file_path_in>"], opt["<file_path_out>"])
