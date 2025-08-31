import re
import unidecode

from calendar import monthrange
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

from decimal import Decimal, InvalidOperation

from PIL import Image, ImageTk

def date_string_to_datatime(value):
  return datetime.strptime(value, '%Y-%m-%d')

def data_datatime_to_string(value):
  return value.strftime('%Y-%m-%d')

def to_string_date_br(value):
  return value.strftime("%d/%m/%Y")

def to_money(value):
  return f"R${value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def first_day_of_current_month():
  first_day_of_month = date(datetime.now().year, datetime.now().month, 1)
  return first_day_of_month

def retroactive_and_postponed_date(data_str, postponed):
  date = datetime.strptime(data_str, '%d/%m/%Y')

  if postponed:
    new_date = date + relativedelta(months=1)
  else:
    new_date = date - relativedelta(months=1)
  
  first_date = new_date.replace(day=1)
  last_date = (first_date + relativedelta(day=31))
  return { "first_date": first_date, "last_date": last_date }

def postponed_date(data_str):
  return retroactive_and_postponed_date(data_str, True)

def retroactive_date(data_str):
  return retroactive_and_postponed_date(data_str, False)

def last_day_of_current_month():
  year = datetime.now().year
  month = datetime.now().month
  last_day_of_month = date(year, month, monthrange(year, month)[1])
  return last_day_of_month

def set_image(image, x, y):
  image = Image.open(image)
  image = image.resize((x, y))
  image = ImageTk.PhotoImage(image)
  return image

def is_decimal(value):
  if value == "" or value.isdigit() or value.replace('.', '', 1).isdigit():
    return True
  return False

def is_valid_day(value):
  if value.isdigit():
    if 0 < int(value) < 32:
      return True
  return False

def is_valid_total_installments(value):
  if value.isdigit():
    if 0 < int(value) < 240:
      return True
  return False

def real_coin_to_decimal(value):
  try:
    value = value.replace('R$', '').strip().replace('.', '').replace(',', '.')
    return float(Decimal(value))
  except InvalidOperation as e:
    raise ValueError("O campo 'Valor' deve possuir valor decimal")

def formatar_text(value):
    value = unidecode.unidecode(value)
    value = re.sub(r'[\W_]', '', value)
    return value.lower()

def compare_texts(value1, value2):
  text1 = formatar_text(value1)
  text2 = formatar_text(value2)
  return text1 == text2
