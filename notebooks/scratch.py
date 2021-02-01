# %%
import os
from pathlib import Path

# run cell once or path will break
print(os.getcwd())
os.chdir(Path(os.getcwd()).parent)
print(os.getcwd())


# %%
from common.load import load_log
from common.model import scale, pca, pca_rank, gmm
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

#  grab original las from dict of data
las = lazy["las"]
print(f"orginal las shape: {las.data.shape}")

# find idx for desired MDs
idx_top = np.where(las.index == 8000)[0][0]
idx_bot = np.where(las.index == 9001)[0][0]
print(f"8000MD idx: {idx_top}, 9000MD idx: {idx_bot}")# print(las.curves)
# print(las.index[0])
# print(las.index[-1])
# print(las.data.shape)

# slice data over desired MDs
las_slice = las.data[idx_top:idx_bot]

# assign sliced data to original las
las.data = las_slice
print(f"las shape: {las.data.shape}")
print(f"las depth index: {las.index.shape}")

# convert to dataframe
try:
    df = las.df()
except Exception as e:
    print(f"conversion to df failed: {e}")

# %%
