import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# TODO: update layout with method or property assignment
# TODO: style plot with colors and marker sizes


# TODO: convert to plotly
def plot_bic_aic(n_components, bic, aic):
    plt.plot(n_components, bic, label="BIC")
    plt.plot(n_components, aic, label="AIC")
    plt.legend(loc='best')
    plt.xlabel('n_components')
    plt.show()


# NOTE: need to pass dataframe, np array does not load smoothly
def plot_pca_2D(log_data, key="merged_pca"):
    data = log_data[key]
    labels = {"x":"component 1", "y":"component 2"}
    cluster_col = data.columns.values.tolist()[-1]
    title = f"{log_data['well_name']}: 2D PCA"
    # HACK: manual column names
    fig = px.scatter(data, x=0, y=1, color=cluster_col, labels=labels, title=title)
    fig.show()


def plot_pca_3D(log_data, key="merged_pca"):
    data = log_data[key]
    cluster_col = data.columns.values.tolist()[-1]
    labels = {"x":"component 1", "y":"component 2", "z":" component 3"}
    title = f"{log_data['well_name']}: 3D PCA"

    fig = px.scatter_3d(data, x=0, y=1, z=2, color=cluster_col, labels=labels, title=title, size_max=10, opacity=0.5)
    fig.show()


def plot_pca_rank(log_data, key="pca_rank"):
    data = log_data[key]
    well = log_data["well_name"]
    
    fig = px.imshow(data, color_continuous_scale='Blues')
    fig.update_layout(title=f"{well}: PCA Feature Rank")
    fig.update_xaxes(showticklabels=True)
    fig.update_yaxes(showticklabels=True)
    fig.show()


# FIXME: fix cluster track and figure out why plot does not always load
def plot_curves_prob(log_data, key="merged_curves"):
    curves = log_data[key]
    cols = curves.columns.values.tolist()

    fig = make_subplots(rows=1, cols=len(cols))

    # FIXME: change heatmap x and adjust curve name logic
    for i in range(len(cols)):
        col = cols[i]
        if col != "SOFT_CLUSTERS" and col != "HARD_CLUSTERS" and col != "DEPT":
            trace = go.Scatter(x=curves[col], y=curves["DEPT"], mode="lines", name=col, line_color="black")
            fig.add_trace(trace, row=1, col=i+1)
        elif col == "SOFT_CLUSTERS":
            # x = [1,2,3,4]
            y = curves["DEPT"]
            z = curves[col]

            fig.add_trace(go.Heatmap(y=y, z=z), row=1, col=i+1)
    
    fig.update_yaxes(autorange="reversed") 
    fig.show()


# TODO: plot distribution of gaussian mixtures with some sort multi-historgram
def plot_gmm_distro():
    pass
