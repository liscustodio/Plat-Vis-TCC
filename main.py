from database import extrair_matriz_binaria
from database import extrair_artigos

from mathEngine import reduzir_dimensionalidade
from plotEngine import gerar_graficos_dispersao
from apiGemini import obter_matriz_similaridade

def executar_pipeline_visualizacao():
    print("1. Conectando ao banco e extraindo dados binários...")
    X, y = extrair_matriz_binaria('biblioteca_completa.db')
    
    print("2. Calculando reduções de dimensionalidade (PCA, t-SNE, etc.)...")
    resultados_2d = reduzir_dimensionalidade(X)

    artigos = extrair_artigos()

    matrizSimilaridade = obter_matriz_similaridade(artigos)
    
    print("3. Renderizando os gráficos...")
    gerar_graficos_dispersao(resultados_2d, y, matrizSimilaridade = matrizSimilaridade)
    
    print("Pipeline concluído com sucesso!")

if __name__ == "__main__":
    executar_pipeline_visualizacao()