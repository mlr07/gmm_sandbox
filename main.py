import os

from common.input import load_log
from common.model import interval, scale, pca, pca_rank, gmm
from common.plot import plot_pca_2D, plot_pca_3D, plot_pca_rank, plot_curves_prob
from common.output import combine_curves_prob, combine_pca_prob


if __name__ == "__main__":
    print(f"main dir: {os.getcwd()}")

    # TODO: put in pipeline
    # FIXME: handle log path with pathlib
    # NOTE: Nb top at 8650'MD, Psh on top, PCA returns 8680'MD-8682'MD

    cols = ["GR", "RT90", "NPHI_COMP", "RHOB"]
    data = "./logs/Lazy_D_400222042.las"
    lazy = load_log(data, cols)
    lazy = interval(lazy, top=8500, bot=8800)
    lazy = scale(lazy)
    lazy = pca(lazy, verbose=1)
    lazy = pca_rank(lazy)
    lazy = gmm(lazy, n=5)
    lazy = combine_curves_prob(lazy)
    lazy = combine_pca_prob(lazy)

    # plot_pca_2D(lazy)
    # plot_pca_3D(lazy)
    # plot_pca_rank(lazy)
    # FIXME: fix curve names
    plot_curves_prob(lazy)

    print(lazy["merged_curves"].info())

    for k,v in lazy.items():
        if not isinstance(v, str):
            print(f"{k}: {type(v)}")
        else:
            print(f"{k}: {v}")

    print("-"*50)

    # TODO: work into loop above
    print(f"base df: {lazy['base_curves'].shape}")
    print(f"soft arr: {lazy['soft_clusters'].shape}")
    print(f"hard arr: {lazy['hard_clusters'].shape}")
    print(f"pca arr: {lazy['pca_curves'].shape}")
    print(f"pca expvar: {lazy['pca_curves'].shape}")
    print(f"pca rank: {lazy['pca_rank'].shape}")
    print(f"merged df: {lazy['merged_curves'].shape}")
    print(f"merged pca: {lazy['merged_pca'].shape}")
