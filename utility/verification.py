import json

from models.wallet import Wallet

""" Provides verification helper methods. """

from utility.hash_util import hash_block, hash_string_256


class Verification:
    @staticmethod
    def valid_proof(transactions, last_hash, proof):
        """ Generates a new hash and check it's validity.
        Arguments:
            :transactions: The transactions that the new block will contain
            :last_hash: The hash from the previous block of the chain
            :proof: The proof number (Nonce)
        """
        guess = f'{[tx.to_ordered_dict() for tx in transactions]}{last_hash}{proof}'.encode()
        hashed_guess = hash_string_256(guess)
        # Set the validity condition of our PoW
        # More 0s == more difficulty
        return hashed_guess[0:2] == '00'

    @classmethod
    def verify_chain(cls, blockchain):
        """ Verify the current blockchain and return True if it's valid,
        False otherwise """
        for (index, block) in enumerate(blockchain):
            if index == 0:
                continue
            if block.previous_hash != hash_block(blockchain[index - 1]):
                print('*' * 20)
                print('Invalid block found.')
                return False
            # block['transactions'][:-1] exludes the reward_transactions
            if not cls.valid_proof(
                block.transactions[:-1],
                block.previous_hash,
                block.proof
            ):
                print('Invalid PoW!')
                return False
        return True

    @staticmethod
    def verify_transaction(transaction, get_balance, check_funds=True):
        """ Verify a transaction by checking whether the sender has sufficient coins.

        Arguments:
            :transaction: The transaction that should be verified.
            :get_balance: Reference to the get_balance function.
        """
        if check_funds:
            sender_balance = get_balance(transaction.sender)
            return sender_balance >= transaction.amount and Wallet.verify_transaction(transaction)
        else:
            return Wallet.verify_transaction(transaction)

    @classmethod
    def verify_transactions(cls, open_transactions, get_balance):
        return all([
            cls.verify_transaction(tx, get_balance, False)
            for tx in open_transactions
        ])
