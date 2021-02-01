import pandas as pd
import numpy as np
import lasio as ls
import os

from common.load import cd

# TODO: determine dtype and shape for probability
# TODO: confirm that cluster array column is correct
# TODO: revert to col per cluster and test


def combine_curves_prob(log_data):
    curves = log_data["base_curves"]

    soft_series = pd.Series(log_data["soft_clusters"].tolist())
    soft_df = soft_series.to_frame(name="soft_clusters").set_index(curves.index)
    
    hard_series = pd.Series(log_data["hard_clusters"].tolist())
    hard_df = hard_series.to_frame(name="hard_clusters").set_index(curves.index)
    
    log_data["merged_curves"] = curves.join([soft_df, hard_df])

    print("LOGS AND  HARD/SOFT CLUSTERS MERGED")

    return log_data 


def combine_pca_prob(log_data):
    # get data
    pca = log_data["pca_curves"]
    hard = log_data["hard_clusters"].reshape((-1,1))
    depth = log_data["base_curves"].index.values.reshape((-1,1))
    
    # merge arrays into df
    merge = np.hstack((pca, hard, depth))
    merged_df = pd.DataFrame(merge)
    
    # set column names
    pca_cols = merged_df.columns.values.tolist()[:-2]
    pca_cols = [f"PC_{p}" for p in pca_cols]
    other_cols = ["hard_cluster", "dept"]
    merged_df.columns = pca_cols + other_cols

    log_data["merged_pca"] = merged_df
    print("PCA AND HARD CLUSTERS MERGED")

    return log_data


def export_las(log_data:dict, prefix:str):
    # get data
    hard_clusters = log_data["hard_clusters"].astype(int)
    las = log_data["las"]
    name = log_data["well_name"]
    
    # get start and stop MDs from user interval and las
    interval_start = float(log_data["interval_top"])
    interval_stop = float(log_data["interval_bot"])
    las_start = las.index[0]
    las_stop = las.index[-1]

    # extract idx from interval and las stop, las start idx is 0
    interval_start_idx = np.where(las.index == interval_start)[0][0]
    interval_stop_idx = np.where(las.index == interval_stop)[0][0]
    las_stop_idx = np.where(las.index == las_stop)[0][0]


    # TODO: figure out how to implement smooth concat of clusters and nan arrays

    # identify location of cluster interval relative to las start and stop
    if interval_start > las_start and interval_stop < las_stop:
        print("interval in middle case --> normal")
        print(f"{las_start} < {interval_start} < {interval_stop} < {las_stop}")

        nan_upper = np.full((interval_start_idx), np.nan)
        nan_lower = np.full((las_stop_idx - interval_stop_idx), np.nan)
        merged = np.concatenate((nan_upper, hard_clusters, nan_lower))
    
    elif interval_start == las_start and interval_stop < las_stop:
        print("interval start equal to las start --> no upper_nan")
        print(f"{las_start} = {interval_start} < {interval_stop} < {las_stop}")

        nan_lower = np.full((las_stop_idx - interval_stop_idx), np.nan)
        merged = np.concatenate((hard_clusters, nan_lower))

    elif interval_start > las_start and interval_stop == las_stop:
        print("interval stop = las stop --> no lower_nan")
        print(f"{las_start} < {interval_start} < {interval_stop} = {las_stop}")
        
        nan_upper = np.full((interval_start_idx), np.nan)
        merged = np.concatenate((nan_upper, hard_clusters))

    elif interval_start == las_start and interval_stop == las_stop:
        print("interval start and stop == las start and stop --> no nan, full log")
        print(f"{las_start} = {interval_start} < {interval_stop} = {las_stop}")
        
        merged = hard_clusters

    else:
        print("unknown case --> error")
        print(f"else case")
        print(f"{interval_start}, {interval_stop}")
        print(f"{las_start}, {las_stop}")

    print(f"shape of merged: {merged.shape}")
    print(f"shape of LAS: {las.index.shape}")

    try:
        with cd(os.path.join(os.getcwd(),"logs")):
            print(os.getcwd())
            las_copy = las
            las_copy.add_curve("ZONE_CLSTR", merged, unit="float", descr="zone clusters")
            las_copy.write(f"{prefix}_{name}.las")
    except Exception as e:
        print(e)


# TODO: name clusters based on user input
def name_clusters():
    pass

# TODO: implement func to export cluster tops
def output_tops():
    pass

# TODO: implement func to export curves and clusters
def output_las():
    pass

# TODO: merge probability curve to las --> add hard cluster array to las object
def add_prob_las(log_data):
    pass

