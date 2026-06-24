import sqlite3
import numpy

def extrair_matriz_binaria(dbPath="biblioteca_completa.db"):
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()

    cursor.execute("SELECT codigo_binario FROM articles ORDER by id")
    linhas = cursor.fetchall()
    conn.close()

    dadosBinarios = []

    for linha in linhas: 
        stringBinaria = linha[0] if linha[0] else '0' * 15
        vetor = [int(bit) for bit in stringBinaria]
        dadosBinarios.append(vetor)

    X = numpy.array(dadosBinarios)

    y = numpy.array([0]*5 + [1]*5 + [2]*5)
    
    return X, y

def extrair_artigos(dbPath = "biblioteca_completa.db"):

    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()

    query = """
        SELECT a.id, a.title, a.keywords, a.abstract, GROUP_CONCAT(r.reference_text, '; ')
        FROM articles a
        LEFT JOIN article_references r ON a.id = r.article_id
        GROUP BY a.id
    """

    cursor.execute(query)
    artigos = cursor.fetchall()
    conn.close()
    
    return artigos