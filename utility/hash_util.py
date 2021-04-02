import hashlib
import json


def hash_string_256(string):
    return hashlib.sha256(string).hexdigest()


def hash_block(block):
    """ Return the hashed block """
    # The .copy() ensure we don't mess with the data of the blocks
    hashable_block = block.__dict__.copy()
    hashable_block['transactions'] = [tx.to_ordered_dict() for tx in hashable_block['transactions']]
    # Avoid hash order error with sort_keys=True
    return hashlib.sha256(json.dumps(hashable_block, sort_keys=True).encode()).hexdigest()
