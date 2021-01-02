import glob
import os
from contextlib import contextmanager

import lasio as ls
import pandas as pd

# TODO: add type hints
# TODO: try error logs piped to file


@contextmanager
def cd(new_dir):
    prev_dir = os.getcwd()
    os.chdir(os.path.expanduser(new_dir))
    try:
        yield 
    finally:
        os.chdir(prev_dir)


# TODO: proper glob and path management, will fail if outside of root dir
def glob_data(data_dir, log_regex="/*.las"):
    try:
        with cd(data_dir):
            return glob.glob(os.getcwd()+log_regex)
    except:
        print("dir not found")


def load_log(log_path):
    log_las = ls.read(log_path, ignore_header_errors=True,  autodetect_encoding=True)
    log_output = dict()
    log_output["las"] = log_las
    log_output["well_name"] = log_las.well["WELL"]["value"]

    try:
        log_output["base_curves"] = memnomics(log_las.df().reset_index()).dropna()
        print("LOG LOADED")

    except (KeyError, Exception) as e:
        print(f"{log_path}: {e}")
        log_output["base_curves"] = None

    return log_output


# TODO: process curve names and select standard logs if present
# TODO: in app the user selects curves from a list
def memnomics(log_df):
    cols = ["DEPT", "SP", "GR", "RT90", "NPHI_COMP", "RHOB", "PE"]
    return log_df[cols]
