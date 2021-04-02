from time import time
from utility.printable import Printable


class Block(Printable):
    def __init__(self, index, previous_hash, transactions, proof, timestamp=None):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.proof = proof
        self.timestamp = time() if timestamp is None else timestamp

    # def __repr__(self):
    #     return f'Index: {self.index}, Previous Hash: {self.previous_hash}, Proof: {self.proof}, Transactions: {self.transactions}'
