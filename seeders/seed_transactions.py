from repository.category_repository import list_categories
from repository.payment_repository import list_payments_by_user_id
from repository.transaction_repository import list_transactions
from services.transaction_service import create_transaction_serv

def seed_transactions(user_id):
  categories_expense = list_categories(True)

  ce_mercado = next((category for category in categories_expense if category.name == 'Mercado'), None)
  ce_padaria = next((category for category in categories_expense if category.name == 'Padaria'), None)
  ce_verdureira = next((category for category in categories_expense if category.name == 'Verdureira'), None)
  ce_vestuario = next((category for category in categories_expense if category.name == 'Vestuário'), None)
  ce_diversos = next((category for category in categories_expense if category.name == 'Diversos'), None)
  ce_lanches = next((category for category in categories_expense if category.name == 'Lanches'), None)
  ce_farmacia = next((category for category in categories_expense if category.name == 'Farmácia'), None)

  categories_income = list_categories(False)

  ci_pagamento = next((category for category in categories_income if category.name == 'Pagamento'), None)
  ci_decimo = next((category for category in categories_income if category.name == 'Décimo'), None)
  ci_bonus = next((category for category in categories_income if category.name == 'Bonus'), None)

  payments = list_payments_by_user_id(user_id)

  p_dinheiro = next((payment for payment in payments if payment.type == 'Dinheiro'), None)
  p_debito = next((payment for payment in payments if payment.type == 'Débito'), None)
  p_credito = next((payment for payment in payments if payment.type == 'Crédito'), None)

  create_transaction_serv("Pagamento", 3500, '2024-10-01', user_id, ci_pagamento.id, p_debito.id)
  create_transaction_serv("Sol", 1250, '2024-10-02', user_id, ce_mercado.id, p_debito.id)
  create_transaction_serv("Roupas", 600, '2024-10-04', user_id, ce_vestuario.id, p_credito.id, 3)
  create_transaction_serv("Hamburger e Refrigerante", 40, '2024-10-08', user_id, ce_lanches.id, p_debito.id)
  create_transaction_serv("Giassi", 350, '2024-10-14', user_id, ce_mercado.id, p_debito.id)
  create_transaction_serv("Bolo e Salgadinhos", 90, '2024-10-20', user_id, ce_padaria.id, p_debito.id)

  create_transaction_serv("Pagamento", 3500, '2024-11-01', user_id, ci_pagamento.id, p_debito.id)
  create_transaction_serv("Koach", 980, '2024-11-03', user_id, ce_mercado.id, p_debito.id)
  create_transaction_serv("Bolo e Salgadinhos", 105, '2024-11-09', user_id, ce_padaria.id, p_debito.id)
  create_transaction_serv("Fio dental", 30, '2024-11-12', user_id, ce_farmacia.id, p_debito.id)
  create_transaction_serv("Koach", 1050, '2024-11-20', user_id, ce_mercado.id, p_debito.id)
  create_transaction_serv("Pizza", 75, '2024-11-25', user_id, ce_lanches.id, p_credito.id, 1)

  create_transaction_serv("Pagamento", 3500, '2024-12-01', user_id, ci_pagamento.id, p_debito.id)
  create_transaction_serv("Décimo Primeira Parte", 2000, '2024-12-01', user_id, ci_decimo.id, p_debito.id)
  create_transaction_serv("Compre Forte", 1500, '2024-12-02', user_id, ce_mercado.id, p_debito.id)
  create_transaction_serv("Sabonete Acepxia", 45, '2024-12-04', user_id, ce_farmacia.id, p_debito.id)
  create_transaction_serv("Frutas e verduras", 85, '2024-12-06', user_id, ce_verdureira.id, p_debito.id)
  create_transaction_serv("TV Led 55", 3500, '2024-12-11', user_id, ce_diversos.id, p_credito.id, 10)
  create_transaction_serv("Hamburger e Refrigerante", 40, '2024-12-18', user_id, ce_lanches.id, p_debito.id)
  create_transaction_serv("Décimo Segunda Parte", 1500, '2024-12-20', user_id, ci_decimo.id, p_debito.id)
  create_transaction_serv("Xarope", 45, '2024-12-22', user_id, ce_farmacia.id, p_debito.id)
