import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import numpy as np


# TODO: update layout with method or property assignment
# TODO: style plot with colors and marker sizes


# TODO: convert to plotly
def plot_bic_aic(n_components, bic, aic):
    plt.plot(n_components, bic, label="BIC")
    plt.plot(n_components, aic, label="AIC")
    plt.legend(loc='best')
    plt.xlabel('n_components')
    plt.show()


# TODO: link to depth in merged dataframe
def plot_pca_2D(log_data, key="merged_pca"):
    data = log_data[key]
    labels = {"x":"component 1", "y":"component 2"}
    cluster_col = data.columns.values.tolist()[-1]
    title = f"{log_data['well_name']}: 2D PCA"
    # HACK: manual column names
    fig = px.scatter(data, 
                     x=0, 
                     y=1, 
                     color=cluster_col, 
                     color_continuous_scale="Turbo", 
                     labels=labels, 
                     title=title
    )
    fig.show()

# TODO: link to depth in merged dataframe
def plot_pca_3D(log_data, key="merged_pca"):
    data = log_data[key]
    cluster_col = data.columns.values.tolist()[-1]
    labels = {"x":"component 1", "y":"component 2", "z":" component 3"}
    title = f"{log_data['well_name']}: 3D PCA"

    fig = px.scatter_3d(data, 
                        x=0, 
                        y=1, 
                        z=2, 
                        color=cluster_col, 
                        color_continuous_scale="Turbo", 
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


# TODO: fix legend, hovertext probs/clusters, fix hard clusters, adjust background/grid
def plot_curves_prob(log_data, key="merged_curves"):
    curves = log_data[key]
    depth = curves.index.values
    cols = curves.columns.values.tolist()
    well = log_data["well_name"]

    fig = make_subplots(rows=1, 
                        cols=len(cols), 
                        shared_yaxes=True, 
                        subplot_titles=cols,
                        horizontal_spacing=0.01
    )

    for i in range(len(cols)):
        col = cols[i]
        text = col

        if col != "soft_clusters" and col != "hard_clusters":
            trace = go.Scatter(x=curves[col], 
                               y=depth, 
                               mode="lines", 
                               name=col, 
                               line_color="black",
                               line_width=2,
                               hovertemplate="MD: %{y}"+"<br>"+f"{col}"+": %{x:.2f}"+"<extra></extra>"
            )
            fig.add_trace(trace, row=1, col=i+1)
            fig.update_xaxes(tickangle=-60, row=1, col=i+1)
        
        # TODO: fix hovertemplate
        elif col == "soft_clusters":
            trace = go.Heatmap(y=depth,
                               z=curves[col],
                               showscale=False,
                               hovertemplate="MD: %{y}<br>CLST: %{x}<br>PROB: %{z:.4f}"+"<extra></extra>",
            )
            fig.add_trace(trace, row=1, col=i+1)
            fig.update_xaxes(showticklabels=False,
                             row=1, 
                             col=i+1)

        elif col == "hard_clusters":
            # convert df column to 1D vertical array for heatmap
            data_1D_array = np.array(curves[col]).reshape(-1,1).astype(str)

            trace = go.Heatmap(y=depth,
                               z=data_1D_array,
                               showscale=Fal
                               hovertemplate="MD: %{y}<br>CLST: %{z}<extra></extra>"
            )
            fig.add_trace(trace, row=1, col=i+1)
            fig.update_xaxes(showticklabels=False,
                             row=1, 
                             col=i+1)


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

    fig.update_layout(title=f"{well}: Curves and Clusters",
                      spikedistance=500,
                      hoverdistance=5
    )

    fig.show()


# TODO: plot distribution of gaussian mixtures with some sort multi-historgram
def plot_gmm_distro():
    pass
