import os

from common.input import load_log
from common.model import interval, scale, pca, gmm
from common.plot import plot_pca_2D, plot_pca_3D, plot_curves_prob
from common.output import combine_curves_prob, combine_pca_prob


if __name__ == "__main__":
    print(f"main dir: {os.getcwd()}")

    # TODO: handle log path with pathlib, ROOTDIR HOML example
    lazy = load_log("./logs/Lazy_D_400222042.las")
    lazy = interval(lazy, top=2500, bot=9500)
    lazy = scale(lazy)
    lazy = pca(lazy, n=3)
    lazy = gmm(lazy, n=4, key="pca_curves")
    lazy = combine_curves_prob(lazy)
    lazy = combine_pca_prob(lazy)

    plot_pca_2D(lazy, key="merged_pca")
    plot_pca_3D(lazy, key="merged_pca")
    # FIXME: adjust curve names in plot
    plot_curves_prob(lazy)

    for k,v in lazy.items():
        if not isinstance(v, str):
            print(k,type(v))
        else:
            print(k,v)

    print(f"base df: {lazy['base_curves'].shape}")
    print(f"merged df: {lazy['merged_curves'].shape}")
    print(f"soft arr: {lazy['soft_clusters'].shape}")
    print(f"hard arr: {lazy['hard_clusters'].shape}")
    print(f"pca arr: {lazy['pca_curves'].shape}")
    print(f"merged pca: {lazy['merged_pca'].shape}")




    
