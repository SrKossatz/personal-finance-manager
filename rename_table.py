import sqlite3

# Conectar ao banco de dados SQLite
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Verificar se a tabela 'history' existe
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='history';")
if cursor.fetchone() is not None:
    # Executar a query para renomear a tabela
    cursor.execute("ALTER TABLE history RENAME TO History;")
    conn.commit()
    print("Tabela renomeada com sucesso!")
else:
    print("A tabela 'history' não existe.")

# Fechar conexão
conn.close()
