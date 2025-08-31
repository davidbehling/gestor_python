from sqlalchemy import text
from database import session  # Supondo que você já tenha a configuração da sessão

def clear_tables():
    tables = ['users', 'categories', 'bank_accounts', 'payments', 'transactions']
    for table in tables:
        # Limpar as tabelas
        session.execute(text(f"DELETE FROM {table}"))
        
        # Verificar se a tabela sqlite_sequence existe antes de tentar deletar
        try:
            session.execute(text(f"DELETE FROM sqlite_sequence WHERE name='{table}'"))
        except Exception as e:
            print(f"Tabela sqlite_sequence não encontrada ou não necessária para {table}: {e}")

    session.commit()
