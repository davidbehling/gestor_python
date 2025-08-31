from repository.payment_repository import create_payment

def seed_payments(user_id, bank_account_id):
    create_payment("Dinheiro", "Dinheiro", user_id)
    create_payment("DEBITO", "Débito", user_id, bank_account_id)
    create_payment("Ponto Frio", "Crédito", user_id, None, due_day=12, closed_day=5)
    create_payment("Petrobras", "Crédito", user_id, None, due_day=12, closed_day=5)
    create_payment("Banco Honda", "Financiamento", user_id, None, due_day=12, closed_day=5)
    create_payment("Binance", "Corretora de Investimentos", user_id, None, due_day=12, closed_day=5)
    create_payment("Banco Inter", "Corretora de Investimentos", user_id, None, due_day=12, closed_day=5)
