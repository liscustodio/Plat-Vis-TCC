import sqlite3

def criar_e_popular_biblioteca_completa():
    # 1. Conexão com o banco de dados final
    conn = sqlite3.connect('biblioteca_completa.db')
    cursor = conn.cursor()

    # 2. Estrutura das Tabelas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        keywords TEXT,
        abstract TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS article_references (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        article_id INTEGER,
        reference_text TEXT NOT NULL,
        FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE
    )
    ''')

    # 3. Lista Consolidada (15 Artigos: Tecnologia, Extensão e Física)
    todos_artigos = [
        # --- JBCS (Tecnologia) ---
        ("OneTrack-M: A Multitask Approach for Transformer-Based MOT Models", "MOT, Transformers, Fast Tracking", "Multi-Object Tracking (MOT) is a critical problem..."),
        ("Multiclass Classification for Detection of GPS Spoofing and Jamming Attacks on UAVs", "UAV, GPS, Jamming, Machine Learning", "Unmanned Aerial Vehicles (UAVs) are increasingly..."),
        ("Enhancing Red Team Agent Learning with Kill Chain Catalyst", "Reinforcement Learning, Kill Chain", "With the advancement of technology, tasks..."),
        ("Identification of Services and Devices for Vulnerability Analysis", "Fingerprint, Shodan, Vulnerability", "The identification of services and devices is..."),
        ("Evaluation of XAI techniques in credit card fraud detection", "Machine Learning, XAI, Fraud Detection", "Artificial intelligence has been employed..."),
        
        # --- RBEU (Extensão Universitária) ---
        ("Curricularização da extensão: a percepção dos docentes", "Curricularização, Ensino Superior, Docentes", "A curricularização da extensão busca integrar..."),
        ("Educação em saúde sobre uso racional de medicamentos", "Saúde, Idoso, Extensão Universitária", "O envelhecimento populacional traz desafios..."),
        ("O papel da extensão na segurança alimentar", "Segurança Alimentar, Políticas Públicas", "Este artigo discute projetos extensionistas..."),
        ("Tecnologias assistivas e inclusão escolar", "Tecnologia Assistiva, Inclusão, Educação Especial", "O estudo descreve o desenvolvimento de recursos..."),
        ("Práticas de sustentabilidade em hortas comunitárias", "Sustentabilidade, Educação Ambiental, Hortas", "Ações de extensão voltadas à criação de hortas..."),

        # --- Brazilian Journal of Physics (Física) ---
        (
            "Quantum Discord and Entanglement in Spin-1/2 Systems",
            "Quantum Information, Spin Systems, Entanglement, Quantum Discord",
            "This work investigates the behavior of quantum discord and entanglement in Heisenberg spin chains under external magnetic fields..."
        ),
        (
            "Black Hole Thermodynamics in Modified Gravity Theories",
            "Black Holes, Thermodynamics, Modified Gravity, Hawking Radiation",
            "We analyze the thermodynamic properties of static black holes in the context of f(R) gravity, focusing on entropy and temperature relations..."
        ),
        (
            "Phase Transitions in Complex Networks: A Statistical Mechanics Approach",
            "Statistical Mechanics, Complex Networks, Phase Transitions, Percolation",
            "The study explores how connectivity patterns influence phase transitions in scale-free networks using Ising model analogies..."
        ),
        (
            "Optical Properties of Graphene-Based Nanostructures",
            "Graphene, Nanotechnology, Optics, Condensed Matter",
            "The optical absorption spectra of graphene nanoribbons are calculated using tight-binding models and Green's function methods..."
        ),
        (
            "Stellar Evolution and Nucleosynthesis in Low-Mass Stars",
            "Astrophysics, Stellar Evolution, Nucleosynthesis, Plasma Physics",
            "Recent observations of chemical abundances in globular clusters are compared with theoretical models of low-mass star evolution..."
        )
    ]

    # 4. Mapa de Referências (5 por artigo)
    referencias_map = {
        # JBCS (0-4)
        0: ["Aharon (2022)", "Bernardin (2008)", "Bewley (2016)", "Carion (2020)", "Luiten (2020)"],
        1: ["Abdulganiyu (2023)", "Aissou (2022)", "Araújo (2023)", "Davidovich (2022)", "Omolara (2023)"],
        2: ["Al-Azzawi (2024)", "Breiman (2001)", "Chen (2023)", "Holm (2022)", "Mnih (2015)"],
        3: ["Al-Alami (2017)", "Bracciale (2024)", "Durumeric (2013)", "Genge (2016)", "Sarabi (2023)"],
        4: ["Aldeia (2022)", "Alfaiz (2022)", "Bussmann (2021)", "Lundberg (2017)", "Ribeiro (2016)"],
        # RBEU (5-9)
        5: ["MEC Resolução 7 (2018)", "FORPROEX (2012)", "Freire (1977)", "Severino (2017)", "Santos (2004)"],
        6: ["OMS Guia Medicamentos", "Alvarenga (2010)", "Brasil (2006)", "Garcia (2012)", "Pontes (2015)"],
        7: ["CONSEA SAN", "Belik (2012)", "Maluf (2007)", "FAO (2023)", "Castro (1984)"],
        8: ["Bersch (2017)", "Manzini (2014)", "Rocha (2016)", "Galvão Filho (2009)", "UNESCO (1994)"],
        9: ["Milani (2015)", "Santos (2002)", "Capra (1996)", "Dias (2004)", "Sachs (2002)"],
        # Física (10-14)
        10: ["Ollivier & Zurek (2001)", "Vedral (2002)", "Nielsen & Chuang (2010)", "Heisenberg (1928)", "Wootters (1998)"],
        11: ["Hawking (1975)", "Bekenstein (1973)", "Starobinsky (1980)", "Carroll (2004)", "Wald (1994)"],
        12: ["Albert & Barabási (2002)", "Newman (2010)", "Watts & Strogatz (1998)", "Ising (1925)", "Dorogovtsev (2008)"],
        13: ["Novoselov (2004)", "Neto et al. (2009)", "Dresselhaus (2010)", "Katsnelson (2012)", "Peres (2010)"],
        14: ["Bethe (1939)", "Clayton (1983)", "Iben (1967)", "Salaris (2005)", "Asplund (2009)"]
    }

    # 5. Inserção
    for i, dados in enumerate(todos_artigos):
        cursor.execute('INSERT INTO articles (title, keywords, abstract) VALUES (?, ?, ?)', dados)
        art_id = cursor.lastrowid
        for ref in referencias_map.get(i, []):
            cursor.execute('INSERT INTO article_references (article_id, reference_text) VALUES (?, ?)', (art_id, ref))

    conn.commit()
    conn.close()
    print("Banco 'biblioteca_completa.db' criado com 15 artigos de Tecnologia, Extensão e Física!")

if __name__ == "__main__":
    criar_e_popular_biblioteca_completa()