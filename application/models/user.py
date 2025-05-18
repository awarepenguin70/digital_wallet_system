import json
import os
from ..config import Config

class User:
    @staticmethod
    def load_users():
        if not os.path.exists(Config.USERS_FILE) or os.path.getsize(Config.USERS_FILE) == 0:
            return {}
        with open(Config.USERS_FILE, 'r') as f:
            return json.load(f)

    @staticmethod
    def save_users(users):
        with open(Config.USERS_FILE, 'w') as f:
            json.dump(users, f, indent=4)

    @staticmethod
    def get_user(email):
        users = User.load_users()
        return users.get(email.lower().strip())

    @staticmethod
    def create_user(email, password, balance=1000, flagged=False):
        users = User.load_users()
        email = email.lower().strip()
        if email in users:
            return False
        users[email] = {
            'password': password,
            'balance': balance,
            'flagged': flagged
        }
        User.save_users(users)
        return True

    @staticmethod
    def update_balance(email, amount):
        users = User.load_users()
        email = email.lower().strip()
        if email not in users:
            return False
        users[email]['balance'] += amount
        User.save_users(users)
        return True

    @staticmethod
    def flag_user(email, flagged=True):
        users = User.load_users()
        email = email.lower().strip()
        if email not in users:
            return False
        users[email]['flagged'] = flagged
        User.save_users(users)
        return True