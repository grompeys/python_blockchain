from uuid import uuid4

from models.blockchain import Blockchain
from models.wallet import Wallet
from utility.verification import Verification


class Node:
    def __init__(self):
        # self.wallet.public_key = str(uuid4())
        self.wallet = Wallet()
        self.blockchain = None

    def get_transaction_value(self):
        """ Returns the input of the user (a recipient and a new transaction amount) as a Tuple. """
        tx_recipient = input('Enter the recipient of the transaction: ')
        tx_amount = float(input('Please enter transaction amount: '))
        # Return a Tuple
        # Parenthesis are required if the Tuple contains only one value
        # return (val, )
        return tx_recipient, tx_amount

    def get_user_choice(self):
        """ Get user input to select program action """
        user_input = input('Your choice: ')
        return user_input

    def print_blockchain_elements(self):
        """ Output the blockchain list to the console """
        for block in self.blockchain.chain:
            print(block)
        else:
            print('-' * 20)

    def listen_for_input(self):
        waiting_for_input = True
        try:
            self.wallet.load_keys()
            self.blockchain = Blockchain(self.wallet.public_key)
        except (IOError, IndexError):
            print('Loading failed...')
        while waiting_for_input:
            if self.blockchain == None:
                print('Got no wallet. Create one? Y/n')
                user_choice = self.get_user_choice()
                if user_choice == 'y' or 'Y':
                    self.wallet.create_keys()
                    self.blockchain = Blockchain(self.wallet.public_key)
                else:
                    waiting_for_input = False
            elif not self.blockchain == None:
                print('Select an option')
                print('1: Add a new transaction')
                print('2: Mine a new block')
                print('3: Output the blockchain blocks')
                print('4: Check transactions validity')
                print('5: Create wallet')
                print('6: Load wallet')
                print('7: Save keys')
                print('q: Quit program')
                user_choice = self.get_user_choice()
                if user_choice == '1':
                    tx_data = self.get_transaction_value()
                    # Extract tx_data to the recipient and amount variables
                    recipient, amount = tx_data
                    signature = self.wallet.sign_transaction(self.wallet.public_key, recipient, amount)
                    if self.blockchain.add_transaction(recipient, self.wallet.public_key, signature, amount=amount):
                        print('Transaction added')
                    else:
                        print('Transaction failed')
                    print(self.blockchain.get_open_transactions())
                elif user_choice == '2':
                    if not self.blockchain.mine_block():
                        print('Mining failed. Got no wallet?')
                elif user_choice == '3':
                    self.print_blockchain_elements()
                elif user_choice == '4':
                    if Verification.verify_transactions(self.blockchain.get_open_transactions(), self.blockchain.get_balance):
                        print('All transactions are valid')
                    else:
                        print('Invalid transaction found')
                elif user_choice == '5':
                    self.wallet.create_keys()
                    self.blockchain = Blockchain(self.wallet.public_key)
                elif user_choice == '6':
                    self.wallet.load_keys()
                    self.blockchain = Blockchain(self.wallet.public_key)
                elif user_choice == '7':
                    self.wallet.save_keys()
                elif user_choice == 'q':
                    waiting_for_input = False
                else:
                    print('!!!!!!!!!!')
                    print('Input was invalid, please enter a valid option.')
                    print('')
                if not Verification.verify_chain(self.blockchain.chain):
                    self.print_blockchain_elements()
                    break
                # print(f'Balance of {self.wallet.public_key}: {get_balance(self.wallet.public_key):6.2f}')
                print('Balance of {}: {:6.2f}'.format(
                    self.wallet.public_key, self.blockchain.get_balance()))

        else:
            print('User left.')

        print(f'Bye! {self.wallet.public_key}')
