#!/home/jliu/anaconda3/bin/python
# -*- coding: utf-8 -*-
# author: James Liu
# date: 2020-01-18
#

"""This script downloads .csv files for horse-racing data in Hong Kong from the user-defined URL
then processes them and writes them to a user-specified location on the local machine
as data_train.csv and data_test.csv. This script takes  the URL where the data is hosted
and the location where the user would like the data to be written to locally.

Usage: download_data.py <url> <file_path>

Arguments:
<url>        Url where the data is hosted.
<file_path>  Path where the data would be written to locally.
"""

import numpy as np
import pandas as pd
from docopt import docopt
from sklearn.model_selection import train_test_split

opt = docopt(__doc__)


def main(url, file_path):
    """
    entry point for script. take in url_path and file_path from commandline,
     and downloads/formats data for downstream use.
    Parameters
    ----------
    url
        the web link where the data is hosted. Assumes that the URL contains 5 files:
            - horse_info.csv
            - results.csv
            - trackworks.csv
            - barrier.csv
            - comments.csv
    file_path
        - the desired filepath to put the wrangled data into.

    Returns
    -------
        None if executed successfully, otherwise raises Exception.
    """
    horse_info, results, comments, track_work, barrier = download_files(url)
    complete_dataset = merge_results(
        horse_info, results, comments, track_work, barrier)
    split_and_write_data(complete_dataset, file_path)
    print(f"successfully written data to {file_path}!\n")


def download_files(url):
    """
    downloads the relevant csvs from the url specified.
    Parameters
    ----------
    url
        the url where the csv files live at.

    Returns
        five Pandas DataFrames
            - horse_info
            - results
            - comments
            - track_work
            - barrier
    -------

    """
    # the comments had a bunch of letter codes saying the horses weren't able to place for some reason; weed out here.
    list_of_invalid_entries = ['1 DH', '2 DH', '3 DH', '4 DH', '5 DH', '6 DH', 'WV',
                               '7 DH', '8 DH', 'PU', '9 DH', 'UR', 'WV-A', 'FE', 'DNF', 'WX', 'TNP', 'WX-A', 'DISQ']
    print("==========\nstarting download...\n")
    horse_info = pd.read_csv(f"{url}/horse_info.csv",
                             index_col=0)
    results = pd.read_csv(f"{url}/results.csv",
                          index_col=0,
                          dtype={"plc": np.float64},
                          na_values=list_of_invalid_entries)
    comments = pd.read_csv(f"{url}/comments.csv",
                           index_col=0,
                           dtype={"plc": np.float64},
                           na_values=list_of_invalid_entries)
    track_work = pd.read_csv(f"{url}/trackwork.csv",
                             index_col=0)
    barrier = pd.read_csv(f"{url}/barrier.csv",
                          index_col=0)
    print("==========\nsuccessfully downloaded CSV data!\n")
    return horse_info, results, comments, track_work, barrier


def merge_results(horse_info, results, comments, track_work, barrier):
    """
    returns a merged dataframe of all five .csv files.
    Parameters
    ----------
    horse_info
        dataframe holding horse info.
    results
        dataframe holding race results.
    comments
        dataframe holding comments for race.
    track_work
        dataframe holding track work information.
    barrier
        dataframe holding barrier trial results.

    Returns
    -------
        a Pandas dataframe containing all of the input dataframes.

    """
    print("==========\nstarting merge...\n")

   # Merging fixing

    results_comments = pd.merge(results, comments, how="left", on=[
                                "horseno", "date", "raceno", "plc"])

    # Rename barrier time which is the same as finish time in results
    barrier.rename(columns={'time': 'finishtime'})
    barrier_binded = pd.concat([results_comments, barrier], sort=False)

    merged_data = pd.merge(barrier_binded, horse_info,
                           how='left', on=['horse'])

# Removed the columns with _ch as this indicated Chinese.
    final_data = merged_data[merged_data.columns[~merged_data.columns.str.contains(
        '.*_ch')]]

    # Drop repeated columns and unnessary indexes
   # final_data =final_data.drop(['trainer_y','Unnamed: 0_x' ,'Unnamed: 0_y'], axis=1)
   # final_data['date']= pd.to_datetime(final_data['date'])
#     final_data


#     horse_info_results = pd.merge(results, horse_info, how="left", on=["horse"])
#     barrier_results = pd.merge(barrier, horse_info_results,
#                               how="left",
#                               on=["horse", "trainer", "jockey"])
#    barrier_horse_info_results = pd.merge(
#        barrier_results, horse_info, how="left", on=["horse"])
#    results_with_comments = pd.merge(
#        barrier_horse_info_results, comments, how="left", left_on=["date", "raceno_x", "plc_x", "horseno"],
#        right_on=["date", "raceno", "plc", "horseno"])

#     separate horse column into its name and its code
#     results_with_comments[["horse", "horse_code"]] = results_with_comments.pop(
#        'horse').str.split('(.*)\((\S*)\)', expand=True).drop(columns=[0, 3])

#     final_data = pd.merge(results_with_comments, track_work,
#                          how="left", on=["horse", "horse_code", #"date"])

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
    main(opt["<url>"], opt["<file_path>"])
