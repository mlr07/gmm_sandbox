import os

from common.load import load_log
from common.model import scale, pca, pca_rank, gmm
from common.plot import plot_pca_2D, plot_pca_3D, plot_pca_rank, plot_curves_prob
from common.output import combine_curves_prob, combine_pca_prob, export_las
from common.utils import verbose_info

# NOTE: NBBR top at 8650'MD (core) or 8683' (COGCC reg) --> litho and chrono picks
# NOTE: 2 cluster PCA returns 8680'MD-8682'MD

# check dir
print(f"main dir: {os.getcwd()}")

# user inputs
cols = ["GR", "RT90", "NPHI_COMP", "RHOB"]
data = "./logs/Lazy_D_400222042.las"
nbbr_top = 8000  # NBBR start
nbbr_bot = 9000  # NBBR stop
las_top = 2295  # lazy d start
las_bot = 9676  # lazy d stop

test_depths = [[2295, 9676, "MOD_FULL"],
               [8000, 9000, "MOD_NORMAL"],
               [2295, 8000, "MOD_NO_UPPER"],
               [8000, 9676, "MOD_NO_LOWER"]]


def main(data, cols, test_depths):
    for depth in test_depths:

        top = depth[0]
        bot = dept# lazy = interval(lazy, top=top, bot=bot)le(lazy)
        lazy = pca(lazy)
        lazy = pca_rank(lazy)
        lazy = gmm(lazy, n=2)
        lazy = combine_curves_prob(lazy)
        lazy = combine_pca_prob(lazy)

        export_las(lazy, prefix=prefix)

    # make plots
    # fig_pca_2D = plot_pca_2D(lazy)
    # plot_pca_3D(lazy)
    # fig_pca_rank = fig_pca_rank = plot_pca_rank(lazy)
    # fig_log_plot = plot_curves_prob(lazy)


if __name__ == "__main__":
    main(data, cols, test_depths)
