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
    pca = log_data["pca_curves"]
    # soft = log_data["soft_clusters"]
    hard = log_data["hard_clusters"].reshape((-1,1))
    
    merge = np.hstack((pca, hard))
    cols = ["comp1, comp2, comp3, hard_cluster"]
    merged_df = pd.DataFrame(merge) 
    log_data["merged_pca"] = merged_df
    print("PCA AND CLUSTERS MERGED")

    return log_data


# TODO: merge probability curve to las
def add_prob_las():
    pass


# TODO: name clusters based on user input
def name_clusters():
    pass
