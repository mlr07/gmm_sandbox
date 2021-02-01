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
from common.output import combine_curves_prob, combine_pca_prob, export_las


# %%
# load log from data and init data dictionary
cols = ["SP", "GR", "RT90", "NPHI_COMP", "RHOB", "PE"]
data = "./logs/Lazy_D_400222042.las"
lazy = load_log(data, cols, top=2295, bot=9676)

# print info
for k,v in lazy.items():
    if not isinstance(v, str):
        print(f"{k}: {type(v)}")
    else:
        print(f"{k}: {v}")

df = lazy["base_curves"]
las = lazy["las"]

print(df.shape)
print(las.index[0])
print(las.index[-1])
print(las.index.shape)


# %%
import numpy as np
import lasio

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

