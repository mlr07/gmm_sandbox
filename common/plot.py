import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# TODO: convert matplotlib to plotly
# TODO: update layout with method or property assignment
# TODO: style plot with colors and marker sizes
# TODO: plot cluster ellipses


def plot_bic_aic(n_components, bic, aic):
    plt.plot(n_components, bic, label="BIC")
    plt.plot(n_components, aic, label="AIC")
    plt.legend(loc='best')
    plt.xlabel('n_components')
    plt.show()


def plot_pca_2D(log_data, key="pca_curves"):
    data = log_data[key]
    labels = {"x":"component 1", "y":"component 2"}
    title = f"{log_data['well_name']}: 2D PCA"

    fig = px.scatter(data, x=data[:,0], y=data[:,1], labels=labels, title=title)
    fig.show()


def plot_pca_3D(log_data, key="pca_curves"):
    data = log_data[key]
    labels = {"x":"component 1", "y":"component 2", "z":" component 3"}
    title = f"{log_data['well_name']}: 3D PCA"

    fig = px.scatter_3d(data, x=data[:,0], y=data[:,1], z=data[:,2], labels=labels, title=title, size_max=10, opacity=0.5)
    fig.show()


def plot_curves_prob(log_data, key="merged_curves"):
    curves = log_data[key]
    cols = curves.columns.values.tolist()

    fig = make_subplots(rows=1, cols=len(cols))

    # TODO: does this loop make sense?
    # FIXME: change heatmap x
    for i in range(len(cols)):
        col = cols[i]
        print(i, col)
        if col != "SOFT_CLUSTERS" and col != "DEPT":
            trace = go.Scatter(x=curves[col], y=curves["DEPT"], mode="lines", name=col, line_color="black")
            fig.add_trace(trace, row=1, col=i+1)
        elif col == "SOFT_CLUSTERS":
            # x = [1,2,3,4]
            y = curves["DEPT"]
            z = curves[col]

            fig.add_trace(go.Heatmap(y=y, z=z), row=1, col=i+1)
    
    fig.update_yaxes(autorange="reversed") 
    fig.show()


# TODO: plot distribution with gaussian mixtures --> distplot
def plot_gmm_distro():
    pass
