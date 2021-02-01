import os

from common.load import load_log
from common.model import scale, pca, pca_rank, gmm
# from common.plot import plot_pca_2D, plot_pca_3D, plot_pca_rank, plot_curves_prob
from common.output import combine_curves_prob, combine_pca_prob, export_las

# TODO: put in pipeline
# FIXME: handle log path with pathlib
# NOTE: NBBR top at 8650'MD (core) or 8683' (COGCC reg) --> litho and chrono picks
# NOTE: 2 cluster PCA returns 8680'MD-8682'MD

# check dir
print(f"main dir: {os.getcwd()}")

# user inputs
cols = ["GR", "RT90", "NPHI_COMP", "RHOB"]
data = "./logs/Lazy_D_400222042.las"
top = 8000
bot = 9000

top = 2295
bot = 9676

test_depths = [[2295, 9676, "MOD_FULL"], [8000,9000, "MOD_NORMAL"], [2295, 8000, "MOD_NO_UPPER"], [8000, 9676, "MOD_NO_LOWER"]]

for depth in test_depths:

    top = depth[0]
    bot = depth[1]
    prefix = depth[2]

    # run gmm and pca --> this needs to be cached
    lazy = load_log(data, cols, top=top, bot=bot)
    lazy = scale(lazy)
    lazy = pca(lazy, verbose=0)
    lazy = pca_rank(lazy)
    lazy = gmm(lazy, n=2, verbose=0)
    lazy = combine_curves_prob(lazy)
    lazy = combine_pca_prob(lazy)

    export_las(lazy, prefix=prefix)

# make plots
# fig_pca_2D = plot_pca_2D(lazy)

# plot_pca_3D(lazy)
# fig_pca_rank = fig_pca_rank = plot_pca_rank(lazy)
# fig_log_plot = plot_curves_prob(lazy)

# print info
# for k,v in lazy.items():
#     if not isinstance(v, str):
#         print(f"{k}: {type(v)}")
#     else:
#         print(f"{k}: {v}")

# print("-"*50)

# # TODO: work into loop above
# print(f"base df: {lazy['base_curves'].shape}")
# print(f"scaled curves:{lazy['scaled_curves'].shape}")
# print(f"pca arr: {lazy['pca_curves'].shape}")
# print(f"pca expvar: {lazy['pca_curves'].shape}")
# print(f"pca rank: {lazy['pca_rank'].shape}")

# print(f"soft arr: {lazy['soft_clusters'].shape}")
# print(f"hard arr: {lazy['hard_clusters'].shape}")
# print(f"merged df: {lazy['merged_curves'].shape}")
# print(f"merged pca: {lazy['merged_pca'].shape}")


