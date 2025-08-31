import sys
import os

# python3 seeders/seed_david.py

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')


from seeders.clear_tables import clear_tables
from seeders.seed_categories import seed_categories
from repository.bank_account_repository import create_bank_account

from repository.user_repository import create_user
from repository.payment_repository import create_payment

def seed_start():
    clear_tables()

    seed_categories()

    user = create_user("David")

    bank_santander = create_bank_account('Santander', user.id)
    bank_binance = create_bank_account('Binance', user.id)
    bank_inter = create_bank_account('Inter', user.id)

    create_payment("Dinheiro", "Dinheiro", user.id)
    create_payment("DEBITO", "Débito", user.id, bank_santander.id)
    create_payment("Binance", "Débito", user.id, bank_binance.id)
    create_payment("Inter", "Débito", user.id, bank_inter.id)
    create_payment("Ponto Frio", "Crédito", user.id, None, due_day=12, closed_day=5)
    create_payment("Petrobras", "Crédito", user.id, None, due_day=12, closed_day=5)
    create_payment("Honda", "Crédito", user.id, None, due_day=27, closed_day=1)

if __name__ == "__main__":
    seed_start()
