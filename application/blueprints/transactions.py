from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from ..models.user import User
from ..models.transaction import Transaction
from ..utils.decorators import login_required
from ..utils.helpers import Logger
from ..utils.fraud_detection import FraudDetector

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/dashboard')
@login_required
def dashboard():
    email = session['user']
    user = User.get_user(email)
    txns = Transaction.get_user_transactions(email)
    txns = sorted(txns, key=lambda x: x['time'], reverse=True)

    return render_template('dashboard.html',
                           balance=user['balance'],
                           history=txns,
                           email=email,
                           is_admin=(email == 'admin@dffdp.com'))

@transactions_bp.route('/add_money', methods=['POST'])
@login_required
def add_money():
    try:
        amount = float(request.form['amount'])
    except ValueError:
        flash("Enter a valid amount.")
        return redirect(url_for('transactions.dashboard'))

    if amount <= 0:
        flash("Invalid amount.")
        return redirect(url_for('transactions.dashboard'))

    email = session['user']
    if User.update_balance(email, amount):
        Transaction.create_transaction('SYSTEM', email, amount, 'TOP-UP')
        Logger.log_event(email, "ADD_MONEY", f"₹{amount} added")
        flash(f"₹{amount} added to wallet.")

    return redirect(url_for('transactions.dashboard'))

@transactions_bp.route('/send', methods=['GET', 'POST'])
@login_required
def send():
    email = session['user']
    users = User.load_users()
    other_users = [u for u in users if u != email]

    if request.method == 'POST':
        receiver = request.form['receiver'].lower().strip()
        try:
            amount = float(request.form['amount'])
        except ValueError:
            flash("Enter a valid amount.")
            return redirect(url_for('transactions.send'))

        if receiver not in users:
            flash("Recipient does not exist.")
            return redirect(url_for('transactions.send'))
        if receiver == email:
            flash("Cannot send money to yourself.")
            return redirect(url_for('transactions.send'))
        if amount <= 0:
            flash("Invalid amount.")
            return redirect(url_for('transactions.send'))

        sender_balance = User.get_user(email)['balance']
        if sender_balance < amount:
            flash("Insufficient balance.")
            return redirect(url_for('transactions.send'))

        status = FraudDetector.check_fraud_patterns(email, amount)

        User.update_balance(email, -amount)
        User.update_balance(receiver, amount)

        if "FRAUD" in status:
            User.flag_user(email, True)
            flash("Transaction flagged for review due to suspicious activity.")

        Transaction.create_transaction(email, receiver, amount, status)
        Logger.log_event(email, "SEND_MONEY", f"Sent ₹{amount} to {receiver}, Status: {status}")

        if "FRAUD" not in status:
            flash("Transaction successful.")
        return redirect(url_for('transactions.dashboard'))

    return render_template('send.html', users=other_users)