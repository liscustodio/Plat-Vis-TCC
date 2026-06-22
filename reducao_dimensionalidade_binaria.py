'''# Importa biblioteca para operações numéricas (vetores, matrizes, etc.)
import numpy as np

# Importa biblioteca para criação de gráficos
import matplotlib.pyplot as plt

# Importa diferentes métodos de redução de dimensionalidade
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.manifold import TSNE, MDS, Isomap, SpectralEmbedding

# -----------------------------
# Tentativa de importar UMAP
# -----------------------------
try:
    import umap
    has_umap = True
except ImportError:
    has_umap = False
    print("UMAP não está instalado. Rodando sem UMAP.")

# -----------------------------
# Geração de dados binários em R^15
# -----------------------------
np.random.seed(42)

n_samples = 25

cluster1 = np.random.binomial(1, 0.1, (n_samples, 15))
cluster2 = np.random.binomial(1, 0.2, (n_samples, 15))
cluster3 = np.random.binomial(1, 0.3, (n_samples, 15))

X = np.vstack([cluster1, cluster2, cluster3])
y = np.array([0]*n_samples + [1]*n_samples + [2]*n_samples)

print(X)

# -----------------------------
# JITTER NOS DADOS (R^15)
# -----------------------------
epsilon_data = 0.05

noise = np.random.normal(0, epsilon_data, X.shape)
X = X + noise * (X == 1)
X = np.clip(X, 0, 1)

# -----------------------------
# Métodos
# -----------------------------
results = {}

pca = PCA(n_components=2)
results["PCA"] = pca.fit_transform(X)

svd = TruncatedSVD(n_components=2)
results["SVD"] = svd.fit_transform(X)

tsne = TSNE(n_components=2, metric='hamming', random_state=42)
results["t-SNE"] = tsne.fit_transform(X)

from sklearn.metrics import pairwise_distances
D = pairwise_distances(X, metric='hamming')

mds = MDS(n_components=2, dissimilarity='precomputed', random_state=42)
results["MDS"] = mds.fit_transform(D)

isomap = Isomap(n_components=2, metric='hamming')
results["Isomap"] = isomap.fit_transform(X)

spectral = SpectralEmbedding(n_components=2)
results["Spectral"] = spectral.fit_transform(X)

if has_umap:
    umap_model = umap.UMAP(n_components=2, metric='hamming', random_state=42)
    results["UMAP"] = umap_model.fit_transform(X)

# -----------------------------
# Plot
# -----------------------------
n_plots = len(results)
cols = 3
rows = int(np.ceil(n_plots / cols))

fig, axes = plt.subplots(rows, cols, figsize=(5*cols, 4*rows))
axes = axes.flatten()

epsilon_plot = 0.01

for i, (name, X_red) in enumerate(results.items()):
    axes[i].scatter(
        X_red[:, 0] + np.random.normal(0, epsilon_plot, len(X_red)),
        X_red[:, 1] + np.random.normal(0, epsilon_plot, len(X_red)),
        c=y,
        alpha=0.7
    )
    axes[i].set_title(name)

for j in range(i+1, len(axes)):
    fig.delaxes(axes[j])

plt.tight_layout()
plt.show()'''

# Importa biblioteca para operações numéricas (vetores, matrizes, etc.)
import numpy as np

# Importa biblioteca para criação de gráficos
import matplotlib.pyplot as plt

# Importa bibliotecas para banco de dados
import sqlite3

# Importa diferentes métodos de redução de dimensionalidade
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.manifold import TSNE, MDS, Isomap, SpectralEmbedding

# -----------------------------
# Tentativa de importar UMAP
# -----------------------------
try:
    import umap
    has_umap = True
except ImportError:
    has_umap = False
    print("UMAP não está instalado. Rodando sem UMAP.")

# -----------------------------
# Extração dos dados binários do BD SQLite
# -----------------------------
conn = sqlite3.connect('biblioteca_completa.db')
cursor = conn.cursor()

# Busca o código binário ordenado pelo ID para manter a ordem dos artigos
cursor.execute("SELECT codigo_binario FROM articles ORDER BY id")
linhas = cursor.fetchall()
conn.close()

# Converte as strings binárias em arrays numéricos
dados_binarios = []
for linha in linhas:
    string_binaria = linha[0] 
    # Se por acaso alguma linha não tiver o código, preenchemos com zeros
    if not string_binaria:
        string_binaria = '0' * 15
        
    # Transforma "01001..." em [0, 1, 0, 0, 1...]
    vetor = [int(bit) for bit in string_binaria]
    dados_binarios.append(vetor)

# Matriz X com os dados do banco
X = np.array(dados_binarios)

# Como sabemos que o banco tem 15 artigos divididos em 3 blocos de 5 
# (Tecnologia, Extensão e Física), configuramos os rótulos (y) para colorir os 3 clusters
n_samples = 5
y = np.array([0]*n_samples + [1]*n_samples + [2]*n_samples)

print("Matriz X extraída do banco de dados:")
print(X)

# -----------------------------
# JITTER NOS DADOS (R^15)
# -----------------------------
# Usamos o np.random.seed(42) para que a randomização do ruído (noise e jitter)
# seja sempre a mesma para os testes, garantindo gráficos reproduzíveis a cada execução.
np.random.seed(42)
epsilon_data = 0.05

noise = np.random.normal(0, epsilon_data, X.shape)
X = X + noise * (X == 1)
X = np.clip(X, 0, 1)

# -----------------------------
# Métodos
# -----------------------------
results = {}

pca = PCA(n_components=2)
results["PCA"] = pca.fit_transform(X)

svd = TruncatedSVD(n_components=2)
results["SVD"] = svd.fit_transform(X)

# Ajuste no t-SNE: perplexity reduzida pois temos apenas 15 amostras no banco
tsne = TSNE(n_components=2, metric='hamming', random_state=42, perplexity=5)
results["t-SNE"] = tsne.fit_transform(X)

from sklearn.metrics import pairwise_distances
D = pairwise_distances(X, metric='hamming')

mds = MDS(n_components=2, dissimilarity='precomputed', random_state=42)
results["MDS"] = mds.fit_transform(D)

# Ajuste no Isomap: n_neighbors reduzido pois temos apenas 15 amostras
isomap = Isomap(n_components=2, metric='hamming', n_neighbors=4)
results["Isomap"] = isomap.fit_transform(X)

spectral = SpectralEmbedding(n_components=2)
results["Spectral"] = spectral.fit_transform(X)

if has_umap:
    # Ajuste no UMAP: n_neighbors reduzido pelo tamanho do dataset
    umap_model = umap.UMAP(n_components=2, metric='hamming', random_state=42, n_neighbors=4)
    results["UMAP"] = umap_model.fit_transform(X)

# -----------------------------
# Plot
# -----------------------------
n_plots = len(results)
cols = 3
rows = int(np.ceil(n_plots / cols))

fig, axes = plt.subplots(rows, cols, figsize=(5*cols, 5*rows))
axes = axes.flatten()

epsilon_plot = 0.01

# for i, (name, X_red) in enumerate(results.items()):
#     axes[i].scatter(
#         X_red[:, 0] + np.random.normal(0, epsilon_plot, len(X_red)),
#         X_red[:, 1] + np.random.normal(0, epsilon_plot, len(X_red)),
#         c=y,
#         alpha=0.7,
#         cmap='viridis' # Adicionado um colormap para destacar melhor as 3 categorias
#     )
#     axes[i].set_title(name)

#     axes[i].set_aspect('equal', adjustable='datalim')
#     axes[i].grid(True, linestyle='--', alpha=0.5)

# for j in range(i+1, len(axes)):
#     fig.delaxes(axes[j])

# plt.tight_layout()
# plt.show()

for i, (name, X_red) in enumerate(results.items()):
    # Calculando os pontos com o jitter (para não recalcular toda hora)
    x_plot = X_red[:, 0] + np.random.normal(0, epsilon_plot, len(X_red))
    y_plot = X_red[:, 1] + np.random.normal(0, epsilon_plot, len(X_red))

    axes[i].scatter(
        x_plot, y_plot,
        c=y, alpha=0.7, cmap='viridis'
    )
    axes[i].set_title(name)
    axes[i].grid(True, linestyle='--', alpha=0.5)

    # --- O NOVO AJUSTE MATEMÁTICO ---
    
    # 1. Encontra onde é o "centro" exato daquele cluster de pontos
    x_center = (x_plot.max() + x_plot.min()) / 2
    y_center = (y_plot.max() + y_plot.min()) / 2
    
    # 2. Descobre qual é a maior distância: se os pontos estão mais espalhados na horizontal (X) ou vertical (Y)
    max_range = max(x_plot.max() - x_plot.min(), y_plot.max() - y_plot.min()) / 2
    
    # 3. Dá 10% de "respiro" (margem) para os pontos não colarem nas bordas
    margin = max_range * 0.1
    
    # 4. Força os dois eixos a desenharem uma caixa do mesmo tamanho, focada no centro dos dados
    axes[i].set_xlim(x_center - max_range - margin, x_center + max_range + margin)
    axes[i].set_ylim(y_center - max_range - margin, y_center + max_range + margin)
    
    # 5. Agora o 'equal' funciona perfeitamente sem criar espaços brancos distorcidos
    axes[i].set_aspect('equal')

for j in range(i+1, len(axes)):
    fig.delaxes(axes[j])

plt.tight_layout()
plt.show()