from database import session
from sqlalchemy.orm import aliased
from sqlalchemy import select, join, asc
from sqlalchemy.orm import joinedload

from models.bank_account import BankAccount
from models.user import User

def create_bank_account(name, user_id):
    bank_account = BankAccount(name=name, user_id=user_id)
    session.add(bank_account)
    session.commit()
    return bank_account

def list_bank_accounts(user_id):
    return session.query(BankAccount).filter_by(user_id=user_id).order_by(BankAccount.name.asc()).all()

def list_banks_and_users(user_ids=None):
    UserAlias = aliased(User)

    stmt = (
      select(
        BankAccount.id.label("id"),
        BankAccount.name.label("name"),
        BankAccount.current_value.label("current_value"),
        UserAlias.id.label("user_id"),
        UserAlias.name.label("user_name"),
      )
      .join(UserAlias, UserAlias.id == BankAccount.user_id, isouter=True)
      .order_by(UserAlias.name, BankAccount.name)
    )

    if user_ids:
      stmt = stmt.filter(BankAccount.user_id.in_(user_ids))

    results = session.execute(stmt).fetchall()
    return results

def find_bank_id(id):
    return session.query(BankAccount).filter_by(id=id).first()

def update_bank(id, new_name):
    bank = find_bank_id(id)
    bank.name = new_name
    session.commit()

def delete_bank(id):
    bank = find_bank_id(id)
    session.delete(bank)
    session.commit()
