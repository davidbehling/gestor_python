import sys
import os

# python3 seeders/seed_start.py

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')


from seeders.clear_tables import clear_tables
from seeders.seed_users import seed_users
from seeders.seed_categories import seed_categories
from seeders.seed_payments import seed_payments
from seeders.seed_transactions import seed_transactions
from repository.user_repository import list_users
from repository.bank_account_repository import create_bank_account, list_bank_accounts

def seed_start():
    clear_tables()

    seed_users()
    seed_categories()

    users = list_users()
    user_id = users[0].id

    create_bank_account('Santander', user_id)

    bank_accounts = list_bank_accounts(user_id)
    bank_account_id = bank_accounts[0].id

    seed_payments(user_id, bank_account_id)

    seed_transactions(user_id)

if __name__ == "__main__":
    seed_start()
