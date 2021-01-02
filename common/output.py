import pandas as pd

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
    print(log_data["merged_curves"].info())

    return log_data 


# TODO: merge probability curve to las
def add_prob_las():
    pass


# TODO: name clusters based on user input
def name_clusters():
    pass