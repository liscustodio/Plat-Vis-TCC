from database import extrair_matriz_binaria
from database import extrair_artigos
from mathEngine import reduzir_dimensionalidade
from plotEngine import gerar_graficos_dispersao
from apiGemini import obter_matriz_similaridade
from shiny import App, ui
from shinywidgets import output_widget, render_widget

def executar_pipeline_visualizacao():
    print("1. Conectando ao banco e extraindo dados binários...")
    X, y = extrair_matriz_binaria('biblioteca_completa.db')

    print(f'x: {X} \n y: {y}')
    
    print("2. Calculando reduções de dimensionalidade (t-SNE, MDS, umap)...")
    resultados_2d = reduzir_dimensionalidade(X)

    print(f'resultados2d: {resultados_2d}')


    artigos = extrair_artigos()

    matrizSimilaridade = obter_matriz_similaridade(artigos)

    for x in matrizSimilaridade:
        print (x)
    #print(matrizSimilaridade)
    
    print("3. Renderizando os gráficos...")
    gerar_graficos_dispersao(resultados_2d, y, matrizSimilaridade = matrizSimilaridade)

    print("Pipeline concluído com sucesso!")

app_ui = ui.page_fluid(
    ui.h2("Análise de Artigos"),
    output_widget("grafico")
)

def server(input, output, session):
    
    @output
    @render_widget
    def grafico():
        X, y = extrair_matriz_binaria()
        resultados_2d = reduzir_dimensionalidade(X)
        artigos = extrair_artigos()
        matrizSimilaridade = obter_matriz_similaridade(artigos)
        print("chamada bem sucedida") 

        fig = gerar_graficos_dispersao(resultados_2d, y, matrizSimilaridade = matrizSimilaridade)

        return fig

#if __name__ == "__main__":
    #executar_pipeline_visualizacao()
    
app = App(app_ui, server)