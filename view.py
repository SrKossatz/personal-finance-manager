from models  import Account, Types, Status, engine, History
from sqlmodel import Session, select
from datetime import date, datetime, timedelta
import matplotlib.pyplot as plt

def create_account(account: Account):
  with Session(engine) as session:
    statement = select(Account).where(Account.bank == account.bank)
    result = session.exec(statement).all()

    if result:
      print("Account already exists")
      return
    
    session.add(account)
    session.commit()
    return account
    

def account_list():
  with Session(engine) as session:
    statement = select(Account)
    results = session.exec(statement).all()
  return results 

def desactivate_account(id):
  with Session(engine) as session:
    statement = select(Account).where(Account.id == id)
    account = session.exec(statement).first()

    if account is None:
        print(f"Nenhuma conta encontrada com o ID {id}.")
        return

    print(f"Conta encontrada: {account}")

    if account.value > 0:
        raise ValueError("Account has a positive balance")
    
    account.status = Status.INACTIVE
    session.commit()
    print(f"Conta {id} desativada com sucesso.")

def transfer_money(id_from, id_to, value):
  with Session(engine) as session:
    statement = select(Account).where(Account.id == id_from)
    account_from = session.exec(statement).first()
    
    if account_from.value < value:
      raise ValueError("Insufficient funds")
    
    statement = select(Account).where(Account.id == id_to)
    account_to = session.exec(statement).first()
    
    account_from.value -= value
    account_to.value += value
    session.commit()
    
def monitor_transactions(history: History):
  with Session(engine) as session:
    statement = select(Account).where(Account.id == history.account_id)
    account = session.exec(statement).first()
  
  #TODO Validar se a conta está ativa
  if history.type == Types.DEPOSIT:
    account.value += history.value
    
  else:
    if account.value < history.value:
      raise ValueError("Insufficient funds")
    account.value -= history.value
    
  session.add(history)
  session.commit()
  return history
    
   
def total_accounts_money():
  with Session(engine) as session:
    statement = select(Account)
    accounts = session.exec(statement).all()
    
    if not accounts:
        print("Nenhuma conta encontrada.")
        return 0.0  # Retorna 0 se não houver contas
    
    total = 0
    for account in accounts:
      total += account.value
    print(f"Total de todas as contas: {total}")  # Mensagem de depuração
      
    
    return float(total)

def find_history_between_dates(start_date, end_date):
  with Session(engine) as session:
    statement = select(History).where(History.date >= start_date, History.date <= end_date)
    results = session.exec(statement).all()
    return results
  
# x = find_history_between_dates(date.today() - timedelta(days=1), date.today() + timedelta(days=1))
# print(x)

def create_graph():
  with Session(engine) as session:
    statement = select(Account).where(Account.status == Status.ACTIVE)
    accounts = session.exec(statement).all()
    banks = []
    total = []

    if not accounts:
        print("Nenhuma conta encontrada.")
        return 0.0  # Retorna 0 se não houver contas

    
    for account in accounts:
      banks.append(account.bank.value)
      total.append(account.value)
    plt.bar(banks, total)
    plt.show()
      


# plt.bar(['Millenium', 'ActivoBank', 'Santander'], [100, 200, 300])
# plt.show()

# account = Account(value=0, bank=Banks.SANTANDER)
# create_account(account)
# desactivate_account(3)
# transfer_money(1, 2, 10)
# history = History(account_id=1, type=Types.WITHDRAW, value=10, date=date.today())
# monitor_transactions(history)
# total_accounts_money()
# find_history_between_dates(date.today(), date.today() + timedelta(days=1))
# create_graph()

# 2H12