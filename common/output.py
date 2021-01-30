import pandas as pd
import numpy as np

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

    print("LOGS AND CLUSTERS MERGED")

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
    print("PCA AND CLUSTERS MERGED")

    return log_data


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


    # pca = pd.DataFrame(log_data["pca_curves"])
    # pca.columns = [f"PCA_{i}" for i in df_pca.columns.values.tolist()]
    # # get hard clusters
    # hard = pd.DataFrame(log_data["hard_clusters"].reshape((-1,1)), columns="hard_clusters")
    # # get depth 
    # depth = pd.DataFrame(log_data["base_curves"].index.values.reshape((-1,1)), columns="depth")
    # # merge dataframes on vertical axis
    # merged_df = pd.DataFrame() 
    # log_data["merged_pca"] = merged_df
    # print("PCA AND CLUSTERS MERGED")