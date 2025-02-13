from models  import Account, Banks, Status, engine
from sqlmodel import Session, select

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



# account = Account(value=0, bank=Banks.SANTANDER)
# create_account(account)
# desactivate_account(3)

# parei em 1H20min
