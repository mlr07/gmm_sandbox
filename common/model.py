import pandas as pd
import numpy as np

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.mixture import GaussianMixture

# TODO: consider passing data dict around differently
# TODO: investigate min number of curves to cluster with
# TODO: investigate curve variance
# TODO: investigate clustering without depth


def scale(log_dict, key="base_curves"):
    log_dict["scaled_curves"] = StandardScaler().fit_transform(log_dict[key])
    return log_dict


# FIXME: slice on "dept" column to get correct interval
def interval(log_dict, top, bot, key="base_curves"):
    log_dict[key] = log_dict[key].loc[top:bot]
    return log_dict


def pca(log_data, n=3, key="scaled_curves", verbose=0):
    pca = PCA(n_components=n, random_state=42)
    log_data["pca_curves"] = pca.fit_transform(log_data[key])

    if verbose == 0:
        print("PCA COMPLETE")

    elif verbose == 1:
        print("PCA COMPLETE")
        print(f"pca: {log_data['pca_curves'].shape}")
        print(f"features: {pca.n_features_}")
        print(f"samples: {pca.n_samples_}")
        print(f"explained variance ratio: {pca.explained_variance_ratio_}")

    return log_data


# TODO: undo pca --> I don't think this is needed as long as index is preserved
def invert_pca():
    pass


# TODO: implement SOFT and HARD clusters
# TODO: modfify key to different curves (PCA, scaled, base, etc)
def gmm(log_dict, n=5, key=None, verbose=0):
    gmm = GaussianMixture(n_components=n, covariance_type="full", n_init=10, random_state=42)
    gmm.fit(log_dict[key])
    log_dict["soft_clusters"] = gmm.predict_proba(log_dict[key])
    log_dict["hard_clusters"] = gmm.predict(log_dict[key])


    if verbose == 0:
        print("GMM COMPLETE")

    elif verbose == 1:
        print("GMM COMPLETE")
        print(f"data: {log_dict[key].shape}")
        print(f"weights: {gmm.weights_.shape}")
        print(f"means: {gmm.means_.shape}")
        print(f"covariances: {gmm.covariances_.shape}")
        print(f"iterations: {gmm.n_iter_}")
        print(f"converged: {gmm.converged_}")

    return log_dict


def gmm_range(scaled_curves, n=25):
    
    clusters = np.arange(1, n+1)
    bic = np.zeros(clusters.shape)
    aic = np.zeros(clusters.shape)
    models = []

    for i,j in enumerate(clusters):
        gmm = GaussianMixture(n_components=j, covariance_type="full", random_state=42)
        gmm.fit(scaled_curves)
        bic[i] = gmm.bic(scaled_curves)
        aic[i] = gmm.aic(scaled_curves)
        models.append(gmm)
    
    print(n)
    print(bic)
    print(aic)
    print(models)

    return clusters, bic, aic, models


# TODO: FLow 1: trim --> scale --> gmm --> plot and save
def pipeline_1():
    pass


# TODO: Flow 2: trim --> scale --> pca --> gmm --> merge --> plot and save
def pipeline_2():
    pass