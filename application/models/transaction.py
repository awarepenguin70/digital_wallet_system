import json
import os
from datetime import datetime
from ..config import Config

class Transaction:
    @staticmethod
    def load_transactions():
        if not os.path.exists(Config.TXNS_FILE) or os.path.getsize(Config.TXNS_FILE) == 0:
            return []
        with open(Config.TXNS_FILE, 'r') as f:
            return json.load(f)

    @staticmethod
    def save_transactions(txns):
        with open(Config.TXNS_FILE, 'w') as f:
            json.dump(txns, f, indent=4)

    @staticmethod
    def create_transaction(sender, receiver, amount, status):
        txns = Transaction.load_transactions()
        txns.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount,
            'status': status,
            'time': datetime.now().isoformat()
        })
        Transaction.save_transactions(txns)
        return True

    @staticmethod
    def get_user_transactions(email):
        txns = Transaction.load_transactions()
        return [txn for txn in txns if txn['sender'] == email or txn['receiver'] == email]

    @staticmethod
    def get_flagged_transactions():
        txns = Transaction.load_transactions()
        return [txn for txn in txns if 'FRAUD' in txn['status']]