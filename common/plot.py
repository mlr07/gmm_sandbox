import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import numpy as np

# TODO: gmm mixture density plot
# TODO: Config tools


# TODO: convert to plotly
def plot_bic_aic(n_components, bic, aic):
    plt.plot(n_components, bic, label="BIC")
    plt.plot(n_components, aic, label="AIC")
    plt.legend(loc='best')
    plt.xlabel('n_components')
    plt.show()


def plot_pca_2D(log_data, key="merged_pca"):
    # prepare data
    data = log_data[key]
    unique_clusters = np.sort(data["hard_cluster"].unique().astype(int))
    pca_var = log_data["pca_expvar"][0:2]*100
    pca_var_sum = pca_var.sum()
    
    # get some colors
    g10 = px.colors.qualitative.G10       
    
    # build a title
    well = log_data["well_name"]
    n = log_data["cluster_n"]
    top = log_data["interval_top"]
    bot = log_data["interval_bot"]
    title = f"{well}: Total 2D PCA Variance = {pca_var_sum:.0f}%, {n} Cluster GMM, {top}-{bot}'MD"

    # make the fig
    fig = go.Figure()
    
    # make trace for each cluster  
    for cluster in unique_clusters:
        mask = data["hard_cluster"] == cluster
        mask_data = data[mask]
        mask_dept = mask_data["dept"].astype(str).tolist()
        trace = go.Scatter(x=mask_data["PC_0"],
                           y=mask_data["PC_1"],
                           mode="markers",
                           name=f"Cluster {cluster}",
                           marker_color=g10[cluster],
                           hovertemplate="MD: %{text}<extra></extra>",
                           text=mask_dept
        )
        fig.add_trace(trace)

    fig.update_layout(title=title,
                      xaxis_title=f"PC_0 variance = {pca_var[0]:.0f}%",
                      yaxis_title=f"PC_1 variance = {pca_var[1]:.0f}%",
                      legend_title="GMM Cluster"
    )

    fig.show()
                    

# TODO: set axis labels and adjust marker colors
def plot_pca_3D(log_data, key="merged_pca"):
    # prepare data
    data = log_data[key]
    unique_clusters = np.sort(data["hard_cluster"].unique().astype(int))
    pca_var = log_data["pca_expvar"][0:3]*100
    pca_var_sum = pca_var.sum()
    
    # get some colors
    g10 = px.colors.qualitative.G10       
    
    # build a title
    well = log_data["well_name"]
    n = log_data["cluster_n"]
    top = log_data["interval_top"]
    bot = log_data["interval_bot"]
    title = f"{well}: Total 3D PCA Variance = {pca_var_sum:.0f}%, {n} Cluster GMM, {top}-{bot}'MD"

    # make figure
    fig = go.Figure()

    # make trace for each cluster  
    for cluster in unique_clusters:
        mask = data["hard_cluster"] == cluster
        mask_data = data[mask]
        mask_dept = mask_data["dept"].astype(str).tolist()
        trace = go.Scatter3d(x=mask_data["PC_0"],
                             y=mask_data["PC_1"],
                             z=mask_data["PC_2"],
                             mode="markers",
                             name=f"Cluster {cluster}",
                             marker_color=g10[cluster],
                             hovertemplate="MD: %{text}<extra></extra>",
                             text=mask_dept
        )
        fig.add_trace(trace)

    fig.update_layout(title=title,
                xaxis_title=f"PC_0 variance = {pca_var[0]:.0f}%",
                yaxis_title=f"PC_1 variance = {pca_var[1]:.0f}%",
                legend_title="GMM Cluster"
    )

    fig.show()


def plot_pca_rank(log_data, key="pca_rank"):
    # get some data
    data = log_data[key]
    pca_var = log_data["pca_expvar"]*100
    cols = data.columns.tolist()
    cols_var = [f"{col} ({var:.1f}%)" for col, var in zip(cols,pca_var)]

    # make title
    well = log_data["well_name"]
    top = log_data["interval_top"]
    bot = log_data["interval_bot"]
    n = log_data["cluster_n"]
    title = f"{well}: PCA Feature Rank, {n} Cluster GMM, {top}-{bot}'MD"

    # build the figure
    fig  = go.Figure()

    trace = go.Heatmap(x=cols_var,
                       y=data.index.values,
                       z=data,
                       colorscale="Blues",
                       hovertemplate="%{z:.2f}<extra></extra>"
    )

    fig.update_layout(title=title,
                      yaxis_autorange="reversed",

    )

    fig.add_trace(trace)
    fig.show()


def plot_curves_prob(log_data, key="merged_curves"):
    # prepare data
    curves = log_data[key]
    depth = curves.index.values
    cols = curves.columns.values.tolist()
    
    # make title
    well = log_data["well_name"]
    n = log_data["cluster_n"]
    top = log_data["interval_top"]
    bot = log_data["interval_bot"]
    interval = abs(top-bot)

    # make the fig
    fig = make_subplots(rows=1, 
                        cols=len(cols), 
                        shared_yaxes=True, 
                        subplot_titles=cols,
                        horizontal_spacing=0.01
    )

    # make trace for each curve 
    for i in range(len(cols)):
        col = cols[i]

        if col != "soft_clusters" and col != "hard_clusters":
            trace = go.Scatter(x=curves[col], 
                               y=depth, 
                               mode="lines", 
                               name=col, 
                               line_color="black",
                               line_width=2,
                               hovertemplate="MD: %{y}<br>"+f"{col}"+": %{x:.2f}<extra></extra>"
            )
            fig.add_trace(trace, 
                          row=1, 
                          col=i+1
            )
            fig.update_xaxes(tickangle=60, 
                             row=1, 
                             col=i+1
            )
        
        elif col == "soft_clusters":
            trace = go.Heatmap(y=depth,
                               z=curves[col],
                               showscale=False,
                               hovertemplate="MD: %{y}<br>CLST: %{x}<br>PROB: %{z:.2f}"+"<extra></extra>",
            )
            fig.add_trace(trace, 
                          row=1, 
                          col=i+1
            )
            fig.update_xaxes(showticklabels=False,
                             row=1, 
                             col=i+1
            )

        elif col == "hard_clusters":
            # convert df column to 1D vertical array
            data_1D_array = np.array(curves[col]).reshape(-1,1)
            # get unique clusters k
            unique_clusters = np.sort(np.unique(data_1D_array))
            # grab a sequence of 10 colors
            g10 = px.colors.qualitative.G10
            # get colors for custer k
            colors = [g10[c] for c in unique_clusters]

            trace = go.Heatmap(y=depth,
                               z=data_1D_array,
                               showscale=False,
                               colorscale=colors,
                               hovertemplate="MD: %{y}<br>CLST: %{z}<extra></extra>"
            )
            fig.add_trace(trace, 
                          row=1, 
                          col=i+1
            )
            fig.update_xaxes(showticklabels=False,
                             row=1, 
                             col=i+1
            )

    # HACK for linked spikelines
    fig.update_traces(yaxis="y1",
                      showlegend=False
    )
    # set up yaxis and howvertool
    fig.update_yaxes(autorange="reversed", 
                     showspikes=True, 
                     spikemode="across+toaxis",
                     spikesnap="cursor",
                     spikedash="solid",
                     spikethickness=1,
                     spikecolor="firebrick"
    )
    fig.update_layout(title=f"{well}: {n} cluster GMM from {top}-{bot}MD' ({interval}' interval)",
                      spikedistance=500,
                      hoverdistance=5
    )
    fig.show()


# TODO: plot distribution of gaussian mixtures with some sort multi-historgram
def plot_gmm_distro():
    pass
