import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'supersecurekey123'
    USERS_FILE = 'users.json'
    TXNS_FILE = 'transactions.json'
    LOG_FILE = 'audit_log.json'

    # Fraud detection
    FRAUD_THRESHOLD = 1000
    FREQUENCY_THRESHOLD = 5
    TIME_WINDOW_MINUTES = 10
    LARGE_WITHDRAWAL_PERCENTAGE = 0.5