import os

from common.input import load_log
from common.model import interval, scale, pca, gmm
from common.plot import plot_pca_2D, plot_pca_3D, plot_curves_prob
from common.output import combine_curves_prob

# TODO: make log data class --> access by attributes with dot notation

if __name__ == "__main__":
    print(f"main dir: {os.getcwd()}")

    # TODO: handle log path with pathlib, ROOTDIR HOML example
    lazy = load_log("./logs/Lazy_D_400222042.las")
    lazy = interval(lazy, top=2500, bot=9500)
    lazy = scale(lazy)
    lazy = pca(lazy, n=3)
    lazy = gmm(lazy, n=6, key="scaled_curves")
    lazy = combine_curves_prob(lazy)

    plot_pca_2D(lazy)
    plot_pca_3D(lazy)
    plot_curves_prob(lazy)

    for k,v in lazy.items():
        if not isinstance(v, str):
            print(k,type(v))
        else:
            print(k,v)




    
