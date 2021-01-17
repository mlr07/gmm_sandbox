import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import numpy as np

# TODO: subplot pca and rank
# TODO: think about gmm mixture density plot

# TODO:
# PCA 2D/3D --> convert from px to go
    # G10 colors for clusters
    # Add depth to pca frame
    # Set hover template
    # Cluster and depth
    # Axis label component and variance %
    # Legend title 
    # Title well, pca, and total variance
    # Config tools

# Explained variance --> Plotly PCA exampls

# Make PCA subplot --> 2D/3D PCA, feature rank, and cumvar


# TODO: convert to plotly
def plot_bic_aic(n_components, bic, aic):
    plt.plot(n_components, bic, label="BIC")
    plt.plot(n_components, aic, label="AIC")
    plt.legend(loc='best')
    plt.xlabel('n_components')
    plt.show()


# TODO: link to depth in merged dataframe, fix legend, plot parameters in title
def plot_pca_2D(log_data, key="merged_pca"):
    # prepare data
    data = log_data[key]

    fig = go.Figure()

    trace = go.Scatter(x=data["PC_0"],
                       y=data["PC_1"],
                       mode="markers",
                       marker_color=data["hard_cluster"]


    )

    fig.add_trace(trace)

    fig.show()
                    

# TODO: link to depth in merged dataframe
def plot_pca_3D(log_data, key="merged_pca"):
    data = log_data[key]
    cluster_col = data.columns.values.tolist()[-1]
    data[cluster_col] = data[cluster_col].astype(str)
    labels = {"x":"component 1", "y":"component 2", "z":" component 3"}
    title = f"{log_data['well_name']}: 3D PCA"

    fig = px.scatter_3d(data, 
                        x=0, 
                        y=1, 
                        z=2, 
                        color=cluster_col, 
                        labels=labels, 
                        title=title, 
                        size_max=10, 
                        opacity=0.5
    )
    fig.show()


def plot_pca_rank(log_data, key="pca_rank"):
    data = log_data[key]
    well = log_data["well_name"]
    
    fig = px.imshow(data, color_continuous_scale='Blues')
    fig.update_layout(title=f"{well}: PCA Feature Rank")
    fig.update_xaxes(showticklabels=True)
    fig.update_yaxes(showticklabels=True)
    fig.show()


def plot_curves_prob(log_data, key="merged_curves"):
    curves = log_data[key]
    depth = curves.index.values
    cols = curves.columns.values.tolist()
    well = log_data["well_name"]
    n = log_data["cluster_n"]
    top = log_data["interval_top"]
    bot = log_data["interval_bot"]
    interval = abs(top-bot)

    fig = make_subplots(rows=1, 
                        cols=len(cols), 
                        shared_yaxes=True, 
                        subplot_titles=cols,
                        horizontal_spacing=0.01
    )

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
                               hovertemplate="MD: %{y}<br>CLST: %{x}<br>PROB: %{z:.4f}"+"<extra></extra>",
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
            unique_clusters = np.unique(data_1D_array)
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


# TODO: quick look at distribution of data in log
def summary_stats():
    # histograms plotted on them selves and colored by curve
    # mean and variance
    # scatter plot matrix (splom) --> maybe not
    pass


    # labels = {"x":"component 1", "y":"component 2"}
    # cluster_col = data.columns.values.tolist()[-1]
    # data[cluster_col] = data[cluster_col].astype(str)
    # title = f"{log_data['well_name']}: 2D PCA"

    # #  make the trace
    # fig = px.scatter(data, 
    #                  x=0, 
    #                  y=1, 
    #                  color=cluster_col,
    #                  labels=labels, 
    #                  title=title
    # )
    
    # # show or return...
    # fig.show()