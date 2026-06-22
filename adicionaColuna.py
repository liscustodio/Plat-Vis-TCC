import sqlite3
import random

def adicionar_coluna_binaria():
    # Conecta ao banco de dados existente
    conn = sqlite3.connect('biblioteca_completa.db')
    cursor = conn.cursor()

    # 1. Adiciona a nova coluna c(15) se ela não existir
    try:
        cursor.execute("ALTER TABLE articles ADD COLUMN codigo_binario TEXT")
        conn.commit()
    except sqlite3.OperationalError:
        print("A coluna 'codigo_binario' já existe. Continuando com a atualização...")

    # 2. Busca todos os IDs para processar linha por linha
    cursor.execute("SELECT id FROM articles ORDER BY id")
    ids = [row[0] for row in cursor.fetchall()]

    for i, art_id in enumerate(ids):
        bits = ['0'] * 15
        
        if 0 <= i <= 4:
            start, end = 0, 4
        elif 5 <= i <= 9:
            start, end = 5, 9
        elif 10 <= i <= 14:
            start, end = 10, 14
        else:
            start, end = -1, -1

        # Aplica a probabilidade de 20% no intervalo definido
        if start != -1:
            for b in range(start, end + 1):
                if random.random() < 0.60:
                    bits[b] = '1'

        # Transforma a lista em string e atualiza o banco
        string_binaria = "".join(bits)
        cursor.execute("UPDATE articles SET codigo_binario = ? WHERE id = ?", (string_binaria, art_id))

    conn.commit()
    conn.close()
    print("Coluna 'codigo_binario' populada com sucesso!")

if __name__ == "__main__":
    adicionar_coluna_binaria()