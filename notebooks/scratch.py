# %%
import os
from pathlib import Path

# run cell once or path will break
print(os.getcwd())
os.chdir(Path(os.getcwd()).parent)
print(os.getcwd())


# %%
from common.load import load_log
from common.model import interval, scale, pca, pca_rank, gmm
# from common.plot import plot_pca_2D, plot_pca_3D, plot_pca_rank, plot_curves_prob
from common.output import combine_curves_prob, combine_pca_prob


# %%
# load log from data and init data dictionary
cols = ["SP", "GR", "RT90", "NPHI_COMP", "RHOB", "PE"]
data = "./logs/Lazy_D_400222042.las"
lazy = load_log(data, cols)

# grab interval of log by index
lazy = interval(lazy, bot=9000, top=8000)

# # standard scale log with defaults
lazy = scale(lazy)

# # run 3 component pca with defaults
lazy = pca(lazy)

# # run feature rank on pca
lazy = pca_rank(lazy)

# # run gmm on scaled curves
lazy = gmm(lazy, n=4)

# # merge gmm clusters to base curves 
lazy = combine_curves_prob(lazy)

# # merge gmm clusters to pca components
lazy = combine_pca_prob(lazy)


# %%
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


# %%
# need to refractor into log export

# there are two cases: depth subset and all depths. note merge_df and las object have different lengths. if i do none in interval... the idx will not match.

# if las.index is supposed to be depth track it does not make sense with 0.5 step deltas

# %%
import numpy as np
import lasio

hard_clusters = lazy["hard_clusters"].astype(int)
las = lazy["las"]
name = lazy["well_name"]

# TODO: add paramsfor interval
# get idx of top and bottom of interval
idx_top = np.where(las.index == 8000)[0][0]
idx_bot = np.where(las.index == 9000)[0][0]

# get idx of las stop
stop = np.where(las.index == las.index[-1])[0][0]

# make nan arrays above and below interval
top_nan = np.full((idx_top), np.nan)
bot_nan = np.full((stop-idx_bot), np.nan)

# merge nan above, interval, nan below
merged = np.concatenate((top_nan, hard_clusters, bot_nan))

# %%
# NOTE: this will not be needed for streamlit. anchortag thing.
from common.load import cd

try:
    with cd(os.path.join(os.getcwd(),"logs")):
        print(os.getcwd())
        las_copy = las
        las_copy.add_curve("ZONE_CLSTR", merged, unit="float", descr="zone clusters")
        las_copy.write(f"MOD2_{name}.las")
except Exception as e:
    print(e)

print(os.getcwd())

# %%
