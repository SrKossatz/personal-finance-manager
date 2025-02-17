from models import Account, History, Types, Banks
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
        valid_banks = {bank.value.lower(): bank for bank in Banks}  # Mapeia os valores para checagem
        for bank in Banks:
            print(f'---{bank.value}---')

        # Validação do banco
        while True:
            bank_input = input("Enter the bank name exactly as shown above: ").strip().lower()  # Normaliza entrada
            if bank_input in valid_banks:
                bank = valid_banks[bank_input]  # Obtém o Enum correto
                break
            else:
                print("❌ Invalid bank name. Please enter one of the listed banks.")

        # Validação do saldo inicial
        while True:
            try:
                value = float(input("Enter the initial balance (must be a positive number): "))
                if value < 0:
                    print("❌ Balance cannot be negative. Try again.")
                else:
                    break
            except ValueError:
                print("❌ Invalid input. Please enter a valid number.")

        # Criar conta após validações
        account = Account(bank=bank, value=value)
        success = create_account(account)  # Supondo que retorna True se for bem-sucedido

        if success:
            print("✅ Account successfully created!")
        else:
            print("❌ Failed to create account. It may already exist or there was an error.")

    def _deactivate_account(self):
        print('Select the account you want to deactivate.')
        for i in account_list():
            if i.value == 0:
                print(f'{i.id} -> {i.bank.value} -> ${i.value}')

        account_id = int(input())

        try:
            desactivate_account(account_id)
            print('✅ Account successfully deactivated.')
        except ValueError:
            print('❌ This account still has a balance, transfer the funds first.')

    def _transfer_money(self):
        accounts = account_list()  # Obtém a lista de contas disponíveis

        if not accounts:
            print("❌ No accounts available for transfer.")
            return

        print('Select the account to withdraw from.')
        account_dict = {acc.id: acc for acc in accounts}  # Mapeia IDs para contas
        for acc in accounts:
            print(f'{acc.id} -> {acc.bank.value} -> ${acc.value:.2f}')

        # Validação da conta de origem
        while True:
            try:
                from_account_id = int(input("Enter the account ID to withdraw from: "))
                if from_account_id in account_dict:
                    from_account = account_dict[from_account_id]
                    break
                else:
                    print("❌ Invalid account ID. Please enter a valid ID from the list.")
            except ValueError:
                print("❌ Invalid input. Please enter a numeric account ID.")

        print('Select the account to transfer to.')
        for acc in accounts:
            if acc.id != from_account_id:  # Impede seleção da mesma conta
                print(f'{acc.id} -> {acc.bank.value} -> ${acc.value:.2f}')

        # Validação da conta de destino
        while True:
            try:
                to_account_id = int(input("Enter the account ID to transfer to: "))
                if to_account_id in account_dict and to_account_id != from_account_id:
                    to_account = account_dict[to_account_id]
                    break
                else:
                    print("❌ Invalid account ID. Please enter a valid ID from the list (cannot be the same as the source account).")
            except ValueError:
                print("❌ Invalid input. Please enter a numeric account ID.")

        # Validação do valor da transferência
        while True:
            try:
                amount = float(input("Enter the transfer amount: "))
                if amount <= 0:
                    print("❌ Amount must be greater than zero.")
                elif amount > from_account.value:
                    print(f"❌ Insufficient funds. Your balance is ${from_account.value:.2f}.")
                else:
                    break
            except ValueError:
                print("❌ Invalid input. Please enter a valid number.")

        # Realizar transferência e verificar se foi bem-sucedida
        try:
            success = transfer_money(from_account_id, to_account_id, amount)
            if success:
                print("✅ Transfer completed successfully!")
            else:
                print("❌ Transfer failed. Please check your account details and try again.")
        except Exception as e:
            print(f"❌ An error occurred during the transfer: {e}")

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
