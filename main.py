from database import extrair_matriz_binaria
from database import extrair_artigos

from mathEngine import reduzir_dimensionalidade
from plotEngine import gerar_graficos_dispersao
from apiGemini import obter_matriz_similaridade

def executar_pipeline_visualizacao():
    print("1. Conectando ao banco e extraindo dados binários...")
    X, y = extrair_matriz_binaria('biblioteca_completa.db')

    print(f'x: {X} \n y: {y}')
    
    print("2. Calculando reduções de dimensionalidade (t-SNE, MDS, umap)...")
    resultados_2d = reduzir_dimensionalidade(X)

    print(f'resultados2d: {resultados_2d}')


    artigos = extrair_artigos()

    matrizSimilaridade = obter_matriz_similaridade(artigos)

    # matrizSimilaridade = [
    #     [100, 30, 20, 10, 35, 5, 5, 5, 5, 5, 10, 5, 15, 10, 5],
    #     [30, 100, 50, 40, 45, 5, 5, 5, 5, 5, 10, 5, 20, 10, 5],
    #     [20, 50, 100, 60, 40, 5, 5, 5, 5, 5, 10, 5, 15, 5, 5],
    #     [10, 40, 60, 100, 30, 5, 5, 5, 5, 5, 5, 5, 10, 5, 5], 
    #     [35, 45, 40, 30, 100, 5, 5, 5, 5, 5, 5, 5, 10, 5, 5],
    #     [5, 5, 5, 5, 5, 100, 70, 85, 60, 70, 2, 2, 2, 2, 2],
    #     [5, 5, 5, 5, 5, 70, 100, 65, 40, 60, 2, 2, 2, 2, 2],
    #     [5, 5, 5, 5, 5, 85, 65, 100, 30, 85, 2, 2, 2, 2, 2],
    #     [5, 5, 5, 5, 5, 60, 40, 30, 100, 30, 2, 2, 2, 2, 2],
    #     [5, 5, 5, 5, 5, 70, 60, 85, 30, 100, 2, 2, 2, 2, 2],
    #     [10, 10, 10, 5, 5, 2, 2, 2, 2, 2, 100, 35, 45, 55, 20],
    #     [5, 5, 5, 5, 5, 2, 2, 2, 2, 2, 35, 100, 30, 25, 85],
    #     [15, 20, 15, 10, 10, 2, 2, 2, 2, 2, 45, 30, 100, 40, 15],
    #     [10, 10, 5, 5, 5, 2, 2, 2, 2, 2, 55, 25, 40, 100, 20],
    #     [5, 5, 5, 5, 5, 2, 2, 2, 2, 2, 20, 85, 15, 20, 100]
    # ]

    for x in matrizSimilaridade:
        print (x)
    #print(matrizSimilaridade)
    
    print("3. Renderizando os gráficos...")
    gerar_graficos_dispersao(resultados_2d, y, matrizSimilaridade = matrizSimilaridade)
    
    print("Pipeline concluído com sucesso!")

if __name__ == "__main__":
    executar_pipeline_visualizacao()