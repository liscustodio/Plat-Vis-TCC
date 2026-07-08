import numpy as np
import matplotlib.pyplot as plt

def gerar_graficos_dispersao(results, y, matrizSimilaridade=None):
    n_plots = len(results)
    cols = 3
    rows = int(np.ceil(n_plots / cols))

    fig, axes = plt.subplots(rows, cols, figsize=(5*cols, 5*rows))
    axes = axes.flatten()

    epsilon_plot = 0.01

    # DICA: Vamos usar 'idx' para o iterador dos gráficos, 
    # liberando 'i' e 'j' para iterar sobre os artigos (linhas e colunas da matriz)
    for idx, (name, X_red) in enumerate(results.items()):
        
        # 1. Calcula as posições X e Y de todos os artigos
        x_plot = X_red[:, 0] + np.random.normal(0, epsilon_plot, len(X_red))
        y_plot = X_red[:, 1] + np.random.normal(0, epsilon_plot, len(X_red))

        # --- A MÁGICA DAS ARESTAS COLORIDAS COMEÇA AQUI ---
        # Só executa se uma matriz foi passada pelo main.py
        if matrizSimilaridade is not None:
            num_artigos = len(X_red)
            for i in range(num_artigos):
                for j in range(i + 1, num_artigos):
                    similaridade = matrizSimilaridade[i][j]
                    
                    # Filtro de Cores e Espessura
                    if 80 <= similaridade <= 100:
                        cor, espessura, opacidade = 'gray', 2.0, 1
                    elif 60 <= similaridade < 80:
                        cor, espessura, opacidade = 'gray', 2.0, 0.5
                    elif 40 <= similaridade < 60:
                        cor, espessura, opacidade = 'gray', 2.0, 0.1
                    else:
                        continue # Menor que 40: não desenha reta
                    
                    x_values = [x_plot[i], x_plot[j]]
                    y_values = [y_plot[i], y_plot[j]]
                    
                    # Desenha a linha no fundo (zorder=1)
                    axes[idx].plot(
                        x_values, y_values, 
                        color=cor, linewidth=espessura, alpha=opacidade, 
                        zorder=1 
                    )
        # --------------------------------------------------

        # 2. Desenha os pontos por cima das linhas (zorder=5)
        axes[idx].scatter(x_plot, y_plot, c=y, alpha=0.9, cmap='viridis', zorder=5)
        axes[idx].set_title(name)
        axes[idx].grid(True, linestyle='--', alpha=0.5)

        # 3. Ajuste Matemático da Tela (Caixas Quadradas)
        x_center = (x_plot.max() + x_plot.min()) / 2
        y_center = (y_plot.max() + y_plot.min()) / 2
        max_range = max(x_plot.max() - x_plot.min(), y_plot.max() - y_plot.min()) / 2
        margin = max_range * 0.1

        axes[idx].set_xlim(x_center - max_range - margin, x_center + max_range + margin)
        axes[idx].set_ylim(y_center - max_range - margin, y_center + max_range + margin)
        axes[idx].set_aspect('equal')

    # Limpa gráficos vazios que sobrarem no grid
    for j in range(idx + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()