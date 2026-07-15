from google import genai
from google.genai import types
import json
import numpy as np

import os

#teste 
from database import extrair_artigos

def obter_matriz_similaridade(artigos):

    
    client = genai.Client(api_key = "")

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

    try:
        # 5. Gerar conteúdo forçando o MIME Type para JSON
        response = client.models.generate_content(
            model="gemini-3-flash-previews", # ou gemini-1.5-pro para análises mais complexas ou gemini-3-flesh-preview
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json" 
            )
        )
    except Exception as e:
        print(f"Erro na chamada: {e}")

    try:
        matriz_python = json.loads(response.text)
        return matriz_python
    except json.JSONDecodeError:
        print("Erro: A IA não retornou um JSON válido.")
        print("Retorno bruto:", response.text)
        return None
