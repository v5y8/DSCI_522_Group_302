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

import pandas as pd
import os
from docopt import docopt

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
    list_of_data = download_files(url)

    write_data_to_file(list_of_data, file_path)
    print(f"successfully written data to {file_path}!\n")


def download_files(url):
    """
    downloads the relevant csvs from the url specified.
    Parameters
    ----------
    url
        the url where the csv files live at.

    Returns
    -------
        a dictionary containing five Pandas DataFrames
           "horse_info" - horse_info
           "results" - results
            "comments" - comments
            "trackwork" - trackwork
            "barrier" - barrier
    -------

    """
    # the comments had a bunch of letter codes saying the horses weren't able to place for some reason; weed out here.
    print("==========\nstarting download...\n")
    horse_info = pd.read_csv(f"{url}/horse_info.csv",
                             index_col=0)
    results = pd.read_csv(f"{url}/results.csv",
                          index_col=0)
    comments = pd.read_csv(f"{url}/comments.csv",
                           index_col=0)
    trackwork = pd.read_csv(f"{url}/trackwork.csv",
                            index_col=0)
    barrier = pd.read_csv(f"{url}/barrier.csv",
                          index_col=0)

    print("==========\nsuccessfully downloaded CSV data!\n")
    return {"horse_info": horse_info,
            "results": results,
            "comments": comments,
            "trackwork": trackwork,
            "barrier": barrier}


def write_data_to_file(dict_of_data, filepath):
    """
    splits the data into a train and test sets with a 8/2 split, then writes them to the specified file path.
    Parameters
    ----------
    dict_of_data
        the tuple contaiing the five dataframes
    filepath
        the user-specified filepath

    Returns
    -------
        None
    """
    print("==========\nstarting write to disk\n")
    for name, data in dict_of_data.items():
        data.to_csv(f"{filepath}/{name}.csv")
    print("==========\nfinished writing files to disk\n")


def test(url, file_path):
    """
    tests both of these things to make sure they're valid.
    Parameters
    ----------
    url: the input url from the commandline
    file_path: the filepath where the downloaded files are written

    Returns
    -------
    Exception if URL is none or file path is not valid;
     otherwise None.
    """
    if url is None:
        raise Exception("URL must be non-empty!")
    if file_path is None or not os.path.isdir(file_path):
        raise Exception("the filepath input is invalid!")


test(opt["<url>"], opt["<file_path>"])

# script entry point
if __name__ == '__main__':
    main(opt["<url>"], opt["<file_path>"])
