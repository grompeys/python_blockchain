import functools
import hashlib
import json
import pickle
from collections import OrderedDict
from hash_util import hash_block, hash_string_256

# Initializing our blockchain list
MINING_REWARD = 10

genesis_block = {
    'previous_hash': '',
    'index': 0,
    'transactions': [],
    'proof': 100
}
blockchain = [genesis_block]
open_transactions = []
owner = 'Billy'
participants = {owner}


def load_data():
    with open('blockchain.p', mode='rb') as f:
        file_content = pickle.loads(f.read())
        global blockchain
        global open_transactions
        # Escape the '\n' with [:-1]
        blockchain = file_content['chain']
        open_transactions = file_content['ot']

load_data()


def save_data():
    with open('blockchain.p', mode='wb') as f:
        save_data = {
            'chain': blockchain,
            'ot': open_transactions
        }
        f.write(pickle.dumps(save_data))


def valid_proof(transactions, last_hash, proof):
    """ Generates a new hash and check it's validity.
    Arguments:
        :transactions: The transactions that the new block will contain
        :last_hash: The hash from the previous block of the chain
        :proof: The proof number (Nonce)
    """
    guess = f'{transactions}{last_hash}{proof}'.encode()
    hashed_guess = hash_string_256(guess)
    # Set the validity condition of our PoW
    # More 0s == more difficulty
    return hashed_guess[0:2] == '00'


def proof_of_work():
    """ Return the proof of work number for the current block's hash """
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof


def get_balance(participant):
    """ Returns the sum of coins received minus the sum of coins sent (in the blockchain as well as in open transactions) for the given participant """
    tx_sender = [[tx['amount'] for tx in block['transactions']
                  if tx['sender'] == participant] for block in blockchain]
    open_tx_sender = [tx['amount']
                      for tx in open_transactions if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = functools.reduce(
        lambda tx_sum, tx_amt: tx_sum + sum(tx_amt)
        if len(tx_amt) > 0
        else tx_sum + 0, tx_sender, 0)

    tx_recipient = [[tx['amount'] for tx in block['transactions']
                     if tx['recipient'] == participant] for block in blockchain]
    amount_received = functools.reduce(
        lambda tx_sum, tx_amt: tx_sum + sum(tx_amt)
        if len(tx_amt) > 0
        else tx_sum + 0, tx_recipient, 0)
    return amount_received - amount_sent


def get_last_blockchain_value():
    """ Returns the last value of the current blockchain. """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']


# Optional parameters must always comes last
def add_transaction(recipient, sender=owner, amount=1.0):
    """ Append a new value as well as the last blockchain value to the blockchain.

    Arguments:
        :sender: The sender of the coins.
        :recipient: The recipient of the coins.
        :amount: The amount of coins sent with the transaction (default = 1.0)
    """
    # Create a Dictionary
    # transaction = {
    #     'sender': sender,
    #     'recipient': recipient,
    #     'amount': amount
    # }
    # Create an OrderedDict to avoid hash errors
    transaction = OrderedDict([
        ('sender', sender),
        ('recipient', recipient),
        ('amount', amount)
    ])
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        save_data()
        return True
    return False


def get_transaction_value():
    """ Returns the input of the user (a recipient and a new transaction amount) as a Tuple. """
    tx_recipient = input('Enter the recipient of the transaction: ')
    tx_amount = float(input('Please enter transaction amount: '))
    # Return a Tuple
    # Parenthesis are required if the Tuple contains only one value
    # return (val, )
    return tx_recipient, tx_amount


def mine_block():
    """ Add a new block to the blockchain. """
    # Get the last block of the blockchain and hash its value
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    # Calculate the PoW
    proof = proof_of_work()

    # Reward the mining
    reward_transaction = OrderedDict([
        ('sender', 'MINING'),
        ('recipient', owner),
        ('amount', MINING_REWARD)
    ])
    # Copy the values of open transaction in a new variable
    # We could specify the range selector [begining : end(not included)] if needed
    # Range selection works with lists and Tuples
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)

    # Create a new block that contains
    # A hashed version of the previous block
    # The index of the current block
    # The list of open transactions
    # The PoW number
    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': copied_transactions,
        'proof': proof
    }
    blockchain.append(block)
    return True


def print_blockchain_elements():
    """ Output the blockchain list to the console """
    for block in blockchain:
        print(block)
    else:
        print('-' * 20)


def get_user_choice():
    """ Get user input to select program action """
    user_input = input('Your choice: ')
    return user_input


def verify_chain():
    """ Verify the current blockchain and return True if it's valid, False otherwise """
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block['previous_hash'] != hash_block(blockchain[index - 1]):
            print('*' * 20)
            print('Invalid block found.')
            return False
        # block['transactions'][:-1] exludes the reward_transactions
        if not valid_proof(block['transactions'][:-1], block['previous_hash'], block['proof']):
            print('Invalid PoW!')
            return False
    return True


def verify_transactions():
    return all([verify_transaction(tx) for tx in open_transactions])


waiting_for_input = True

while waiting_for_input:
    print('Select an option')
    print('1: Add a new transaction')
    print('2: Mine a new block')
    print('3: Output the blockchain blocks')
    print('4: Output participants')
    print('5: Check transactions validity')
    print('h: Manipulate the chain...')
    print('q: Quit program')
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_data = get_transaction_value()
        # Extract tx_data to the recipient and amount variables
        recipient, amount = tx_data
        if add_transaction(recipient, amount=amount):
            print('Transaction added')
        else:
            print('Transaction failed')
        print(open_transactions)
    elif user_choice == '2':
        if mine_block():
            open_transactions = []
            save_data()
    elif user_choice == '3':
        print_blockchain_elements()
    elif user_choice == '4':
        print(participants)
    elif user_choice == '5':
        if verify_transactions():
            print('All transactions are valid')
        else:
            print('Invalid transaction found')
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = {
                'previous_hash': '',
                'index': 0,
                'transactions': [{'sender': 'Chris', 'recipient': 'Billy', 'amount': 100}]
            }
    elif user_choice == 'q':
        waiting_for_input = False
    else:
        print('!!!!!!!!!!')
        print('Input was invalid, please enter a valid option.')
        print('')
    if not verify_chain():
        print_blockchain_elements()
        break
    # print(f'Balance of {owner}: {get_balance(owner):6.2f}')
    print('Balance of {}: {:6.2f}'.format(owner, get_balance(owner)))
else:
    print('User left.')

print('Bye! ' + owner)
