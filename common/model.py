import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.mixture import GaussianMixture


# NOTE: quick scaler
def scale(log_data, key="base_curves"):
    log_data["scaled_curves"] = StandardScaler().fit_transform(log_data[key])

    return log_data


# NOTE: run PCA
def pca(log_data, key="scaled_curves"):
    pca = PCA(random_state=42)
    log_data["pca_curves"] = pca.fit_transform(log_data[key])
    log_data["pca_expvar"] = pca.explained_variance_ratio_

    return log_data


# NOTE: compute feature rank from PCA. see notebook 02 for run down on method.
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


# NOTE: run gmm
def gmm(log_data, n=5, key="scaled_curves"):
    gmm = GaussianMixture(n_components=n, covariance_type="full", n_init=10, random_state=42)
    gmm.fit(log_data[key])

    log_data["soft_clusters"] = gmm.predict_proba(log_data[key])
    log_data["hard_clusters"] = gmm.predict(log_data[key])
    log_data["cluster_n"] = n

    return log_data

