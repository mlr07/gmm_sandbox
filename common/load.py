import os
from contextlib import contextmanager

import lasio as ls
import pandas as pd


# NOTE: this is used by log export in output.py
@contextmanager
def cd(new_dir):
    prev_dir = os.getcwd()
    os.chdir(os.path.expanduser(new_dir))
    try:
        yield
    finally:
        os.chdir(prev_dir)


# TODO: dash, need a place to examine curves and select depths
# NOTE: this will probably be the place the encoding error will pop up
def inspect_log():
    pass


# NOTE: make dict and load in log
def load_log(log_path:str, cols:list, top:int, bot:int):
    log_data = dict()
    log_data["interval_top"] = top
    log_data["interval_bot"] = bot

    try:
        log_data["las"] = ls.read(log_path, ignore_header_errors=True, autodetect_encoding=True)
        log_data["well_name"] = log_data["las"].well["WELL"]["value"]
        # HACK: nan is replaced with 0.0 to keep shapes consistent between las and df
        log_data["base_curves"] = log_data["las"].df().loc[top:bot][cols].fillna(0.0)

        return log_data

    except Exception as e:
        print(e)