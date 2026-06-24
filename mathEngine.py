import numpy as np
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.manifold import TSNE, MDS, Isomap, SpectralEmbedding
from sklearn.metrics import pairwise_distances

try:
    import umap
    has_umap = True
except ImportError:
    has_umap = False

def reduzir_dimensionalidade(X):

    np.random.seed(42)
    epsilonData = 0.05
    noise = np.random.normal(0, epsilonData, X.shape)
    X = X + noise * (X == 1)
    X = np.clip(X, 0, 1)

    results = {}

    results["PCA"] = PCA(n_components=2).fit_transform(X)
    results["SVD"] = TruncatedSVD(n_components=2).fit_transform(X)
    results["t-SNE"] = TSNE(n_components=2, metric='hamming', random_state=42, perplexity=5).fit_transform(X)
    
    D = pairwise_distances(X, metric='hamming')
    results["MDS"] = MDS(n_components=2, dissimilarity='precomputed', random_state=42).fit_transform(D)
    
    results["Isomap"] = Isomap(n_components=2, metric='hamming', n_neighbors=4).fit_transform(X)
    results["Spectral"] = SpectralEmbedding(n_components=2).fit_transform(X)

    if has_umap:
        results["UMAP"] = umap.UMAP(n_components=2, metric='hamming', random_state=42, n_neighbors=4).fit_transform(X)

    return results