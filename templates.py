from models import Account, History, Types, Status, Bancos
from view import create_account, desactivate_account, transfer_money, monitor_transactions, total_accounts_money, find_history_between_dates, create_graph, account_list
from datetime import date, datetime

class UI:
    def start(self):
        while True:
            print('''
            [1] -> Create account
            [2] -> Deactivate account
            [3] -> Transfer money
            [4] -> Monitor transactions
            [5] -> Total account balance
            [6] -> Filter transaction history
            [7] -> Generate graph
                  ''')
            
            choice = int(input('Choose an option: '))

            if choice == 1:
                self._create_account()
            elif choice == 2:
                self._deactivate_account()
            elif choice == 3:
                self._transfer_money()
            elif choice == 4:
                self._monitor_transactions()
            elif choice == 5:
                self._total_accounts()
            elif choice == 6:
                self._filter_transactions()
            elif choice == 7:
                self._generate_graph()
            else:
                break

    def _create_account(self):
        print('Enter the name of one of the banks below:')
        for bank in Bancos:
            print(f'---{bank.value}---')
        
        bank = input().title()
        value = float(input('Enter the initial balance: '))

        account = Account(bank=Bancos[bank], value=value)
        create_account(account)

    def _deactivate_account(self):
        print('Select the account you want to deactivate.')
        for i in account_list():
            if i.value == 0:
                print(f'{i.id} -> {i.bank.value} -> ${i.value}')

        account_id = int(input())

        try:
            desactivate_account(account_id)
            print('Account successfully deactivated.')
        except ValueError:
            print('This account still has a balance, transfer the funds first.')

    def _transfer_money(self):
        print('Select the account to withdraw from.')
        for i in account_list():
            print(f'{i.id} -> {i.bank.value} -> ${i.value}')

        from_account_id = int(input())

        print('Select the account to transfer to.')
        for i in account_list():
            if i.id != from_account_id:
                print(f'{i.id} -> {i.bank.value} -> ${i.value}')

        to_account_id = int(input())
        amount = float(input('Enter the transfer amount: '))
        transfer_money(from_account_id, to_account_id, amount)

    def _monitor_transactions(self):
        print('Select an account.')
        for i in account_list():
            print(f'{i.id} -> {i.bank.value} -> ${i.value}')

        account_id = int(input())
        amount = float(input('Enter the transaction amount: '))

        print('Select the transaction type:')
        for type in Types:
            print(f'---{type.value}---')
        
        type = input().title()
        history = History(account_id=account_id, type=Types[type], value=amount, date=date.today())
        monitor_transactions(history)
    
    def _total_accounts(self):
        print(f'Total balance: ${total_accounts_money()}')

    def _filter_transactions(self):
        start_date = input('Enter the start date (dd/mm/yyyy): ')
        end_date = input('Enter the end date (dd/mm/yyyy): ')

        start_date = datetime.strptime(start_date, '%d/%m/%Y').date()
        end_date = datetime.strptime(end_date, '%d/%m/%Y').date()

        for i in find_history_between_dates(start_date, end_date):
            print(f'{i.value} - {i.type.value}')

    def _generate_graph(self):
        create_graph()

UI().start()
