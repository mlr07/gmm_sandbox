import pandas as pd

# TODO: determine dtype and shape for probability
# TODO: confirm that cluster array column is correct
# TODO: revert to col per cluster and test

def combine_curves_prob(log_data):
    curves = log_data["base_curves"]
    prob_series = pd.Series(log_data["cluster_probs"].tolist())
    prob_df = prob_series.to_frame(name="SOFT_CLUSTERS").set_index(curves.index)

    log_data["merged_curves"] = curves.join(prob_df)

    print(log_data["merged_curves"].info())

    return log_data 


# TODO: merge probability curve to las
def add_prob_las():
    pass