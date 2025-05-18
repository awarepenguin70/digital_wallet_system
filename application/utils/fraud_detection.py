from datetime import datetime, timedelta
from ..config import Config
from ..models.transaction import Transaction
from ..models.user import User

class FraudDetector:
    @staticmethod
    def check_fraud_patterns(sender, amount):
        txns = Transaction.load_transactions()
        now = datetime.now()
        time_window = now - timedelta(minutes=Config.TIME_WINDOW_MINUTES)

        recent_txns = [
            t for t in txns
            if t['sender'] == sender
               and datetime.fromisoformat(t['time']) >= time_window
        ]

        if len(recent_txns) >= Config.FREQUENCY_THRESHOLD:
            return f"FREQUENCY_FRAUD - {len(recent_txns)} transactions in last {Config.TIME_WINDOW_MINUTES} minutes"

        if amount > Config.FRAUD_THRESHOLD:
            return f"AMOUNT_FRAUD - Exceeds ₹{Config.FRAUD_THRESHOLD}"

        sender_balance = User.get_user(sender).get('balance', 0)
        if sender_balance > 0 and amount / sender_balance > Config.LARGE_WITHDRAWAL_PERCENTAGE:
            return f"WITHDRAWAL_FRAUD - Withdrawal of {amount/sender_balance:.0%} of total balance"

        return "OK"