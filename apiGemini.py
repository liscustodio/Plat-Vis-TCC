from google import genai
from google.genai import types
import sqlite3
import json
import numpy as np

client = genai.Client(api_key="AIzaSyCDyVyB_d8qtT0cbV7iGwGVx-zcxmMHE9A")

def obter_matriz_similaridade():

    conn = sqlite3.connect('biblioteca_completa.db')
    cursor = conn.cursor()
    
    # O comando GROUP_CONCAT junta todas as referências do artigo em uma única string
    query = """
        SELECT a.id, a.title, a.keywords, a.abstract, GROUP_CONCAT(r.reference_text, '; ')
        FROM articles a
        LEFT JOIN article_references r ON a.id = r.article_id
        GROUP BY a.id
    """
    cursor.execute(query)
    artigos = cursor.fetchall()
    conn.close()

    # 3. Preparar o contexto estruturado
    referencias_texto = ""
    for a in artigos:
        referencias_texto += f"ID {a[0]} | TÍTULO: {a[1]}\nKEYWORDS: {a[2]}\nABSTRACT: {a[3]}\nREFERÊNCIAS: {a[4]}\n---\n"

    prompt = f"""
    Você é um especialista analisando uma base de dados local de artigos.
    Compare os artigos abaixo utilizando título, palavras-chaves, resumo e referências.
    Ou os equivalentes caso o artigo esteja em inglês.
    
    Calcule o percentual de proximidade relativa (de 0 a 100) entre todos eles. 
    Entenda como proximidade relativa: as relações entre as áreas, os problemas abordados e a metodologia envolvida nas soluções propostas em artigo.  
    
    REGRA CRÍTICA DE SAÍDA: 
    Retorne APENAS um array JSON 2D válido representando a matriz de adjacência.
    Não adicione formatação markdown (```json), nem textos explicativos.
    Exemplo do formato exigido para 3 artigos:
    [[100, 45, 12], [45, 100, 80], [12, 80, 100]]
    
    BASE DE CONHECIMENTO:
    {referencias_texto}
    """

    # 5. Gerar conteúdo forçando o MIME Type para JSON
    response = client.models.generate_content(
        model="gemini-3-flash-preview", # ou gemini-1.5-pro para análises mais complexas
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json" # Força a IA a cuspir apenas dados puros
        )
    )

    try:
        matriz_python = json.loads(response.text)
        return matriz_python
    except json.JSONDecodeError:
        print("Erro: A IA não retornou um JSON válido.")
        print("Retorno bruto:", response.text)
        return None

# --- Como usar a variável no seu código principal ---
if __name__ == "__main__":
    print("Enviando dados para o Gemini processar a matriz...\n")
    
    # A MÁGICA ACONTECE AQUI: O retorno da função vai direto para a variável
    minha_matriz_variavel = obter_matriz_similaridade()
    
    if minha_matriz_variavel:
        print("Sucesso! A matriz foi armazenada na variável.")
        print(f"Tipo da variável: {type(minha_matriz_variavel)}") # Vai imprimir <class 'list'>
        
        # Como você curte Data Science, pode jogar direto pro Numpy!
        matriz_numpy = np.array(minha_matriz_variavel)
        
        print("\nMatriz formatada:")
        print(matriz_numpy)