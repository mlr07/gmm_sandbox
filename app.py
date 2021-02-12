import os

from common.load import load_log
from common.model import scale, pca, pca_rank, gmm
from common.plot import plot_pca_2D, plot_pca_3D, plot_pca_rank, plot_curves_prob
from common.output import combine_curves_prob, combine_pca_prob, export_las
from common.utils import verbose_info

import dash
import dash_core_components as dcc
import dash_html_components as html

# check dir
print(f"main dir: {os.getcwd()}")

# user inputs
cols = ["GR", "RT90", "NPHI_COMP", "RHOB"]
data = "./logs/Lazy_D_400222042.las"
top = 8000
bot = 9000

# run gmm and pca --> this needs to be cached
lazy = load_log(data, cols, top=8500, bot=8800)
lazy = scale(lazy)
lazy = pca(lazy)
lazy = pca_rank(lazy)
lazy = gmm(lazy, n=4)
lazy = combine_curves_prob(lazy)
lazy = combine_pca_prob(lazy)

# make plots
fig_pca_2D = plot_pca_2D(lazy)
fig_pca_rank = fig_pca_rank = plot_pca_rank(lazy)
fig_log_plot = plot_curves_prob(lazy)

# dash recommended style sheet
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# construct app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# style to align center and justify figures
style = {
    "width": "100%",
    "display": "flex",
    "align-items": "center",
    "justify-content": "center"
}

app.layout = html.Div([
    html.Div([
        dcc.Graph(
            id="graph1",
            figure=fig_log_plot
        ),  
    ], className="row", style=style),

    html.Div([
        dcc.Graph(
            id="graph2",
            figure=fig_pca_2D
        )
    ], className="row", style=style),

    html.Div([
        dcc.Graph(
            id="graph3",
            figure=fig_pca_rank
        )
    ], className="row", style=style)
])


if __name__ == '__main__':
    app.run_server(debug=True)