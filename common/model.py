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


def interval(log_dict, top, bot, key="base_curves"):
    log_dict[key] = log_dict[key].loc[top:bot]
    return log_dict


def pca(log_data, key="scaled_curves", verbose=0):
    pca = PCA(random_state=42)
    log_data["pca_curves"] = pca.fit_transform(log_data[key])
    log_data["pca_expvar"] = pca.explained_variance_ratio_

    if verbose == 0:
        print("PCA COMPLETE")

    elif verbose == 1:
        print("PCA COMPLETE")
        print(f"pca: {log_data['pca_curves'].shape}")
        print(f"features: {pca.n_features_}")
        print(f"samples: {pca.n_samples_}")
        print(f"explained variance ratio: {log_data['pca_expvar']}")

    return log_data


# TODO: review routine with dataframes, too many variables
# TODO: verbose print out of features and pca rank
def pca_rank(log_data):
    X = log_data["scaled_curves"]
    X_pca = log_data["pca_curves"]
    index = log_data["base_curves"].columns.values.tolist()
    expvar = log_data["pca_expvar"]

    matrix = np.dot(X.T, X_pca)

    df = pd.DataFrame(matrix)

    df.columns = [''.join(['PC', f'{i+1}']) for i in range(matrix.shape[0])]
    df.index = index

    df_norm = (df.copy()-df.mean())/df.std()
    df_norm = df_norm.sort_values(by=list(df_norm.columns), ascending=False)

    df_abs = df_norm.copy().abs()
    df_abs = df_abs.sort_values(by=list(df_abs.columns), ascending=False)

    df_expvar = df_abs.copy()*expvar
    df_expvar = df_expvar.sort_values(by=list(df_expvar.columns), ascending=False)

    log_data["pca_rank"] = df_expvar

    return log_data


def gmm(log_dict, n=5, key="scaled_curves", verbose=0):
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