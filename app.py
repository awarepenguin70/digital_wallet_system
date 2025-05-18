from flask import Flask, render_template, request, redirect, session, flash, url_for
import json, os
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
app.secret_key = 'supersecurekey123'

USERS_FILE = 'users.json'
TXNS_FILE = 'transactions.json'
LOG_FILE = 'audit_log.json'
FRAUD_THRESHOLD = 1000  # Single transaction threshold
FREQUENCY_THRESHOLD = 5  # Max transactions in time window
TIME_WINDOW_MINUTES = 10  # Time window for frequency check
LARGE_WITHDRAWAL_PERCENTAGE = 0.5  # 50% of balance

# === Utility Functions ===
def load_json(filename, default):
    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        return default
    with open(filename, 'r') as f:
        return json.load(f)


def save_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def load_users():
    return load_json(USERS_FILE, {})


def save_users(users):
    save_json(USERS_FILE, users)


def load_transactions():
    return load_json(TXNS_FILE, [])


def save_transactions(txns):
    save_json(TXNS_FILE, txns)


def log_event(user, action, details=""):
    logs = load_json(LOG_FILE, [])
    logs.append({
        "user": user,
        "action": action,
        "details": details,
        "timestamp": datetime.now().isoformat()
    })
    save_json(LOG_FILE, logs)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash("Please log in first.")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def is_admin():
    return session.get('user') == 'admin@dffdp.com'


def check_fraud_patterns(sender, amount, txns):
    """Check for various fraud patterns"""
    now = datetime.now()
    time_window = now - timedelta(minutes=TIME_WINDOW_MINUTES)

    # Get recent transactions by this user
    recent_txns = [
        t for t in txns
        if t['sender'] == sender
           and datetime.fromisoformat(t['time']) >= time_window
    ]

    # Pattern 1: Multiple transfers in short period
    if len(recent_txns) >= FREQUENCY_THRESHOLD:
        return f"FREQUENCY_FRAUD - {len(recent_txns)} transactions in last {TIME_WINDOW_MINUTES} minutes"

    # Pattern 2: Large amount compared to threshold
    if amount > FRAUD_THRESHOLD:
        return f"AMOUNT_FRAUD - Exceeds ₹{FRAUD_THRESHOLD}"

    # Pattern 3: Sudden large withdrawal (percentage of balance)
    sender_balance = load_users().get(sender, {}).get('balance', 0)
    if sender_balance > 0 and amount / sender_balance > LARGE_WITHDRAWAL_PERCENTAGE:
        return f"WITHDRAWAL_FRAUD - Withdrawal of {amount/sender_balance:.0%} of total balance"

    return "OK"


# === Routes ===
@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email'].lower().strip()
        password = request.form['password']
        users = load_users()

        if email in users:
            flash("User already exists.")
            return redirect(url_for('register'))

        users[email] = {
            'password': password,
            'balance': 1000,
            'flagged': False
        }
        save_users(users)
        flash("Registered successfully!")
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].lower().strip()
        password = request.form['password']
        users = load_users()

        user = users.get(email)
        if user and user['password'] == password:
            session['user'] = email
            log_event(email, "LOGIN")

            # Redirect to admin if admin email logs in
            if email == "admin@dffdp.com":
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials.")
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    log_event(session.get('user', 'Unknown'), "LOGOUT")
    session.pop('user', None)
    flash("Logged out.")
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    users = load_users()
    txns = load_transactions()
    email = session['user']
    balance = users[email]['balance']
    history = [txn for txn in txns if txn['sender'] == email or txn['receiver'] == email]
    history = sorted(history, key=lambda x: x['time'], reverse=True)

    return render_template('dashboard.html', balance=balance, history=history, email=email, is_admin=is_admin())


@app.route('/add_money', methods=['POST'])
@login_required
def add_money():
    try:
        amount = float(request.form['amount'])
    except ValueError:
        flash("Enter a valid amount.")
        return redirect(url_for('dashboard'))

    if amount <= 0:
        flash("Invalid amount.")
        return redirect(url_for('dashboard'))

    users = load_users()
    user = session['user']
    users[user]['balance'] += amount
    save_users(users)

    txns = load_transactions()
    txns.append({
        'sender': 'SYSTEM',
        'receiver': user,
        'amount': amount,
        'status': 'TOP-UP',
        'time': datetime.now().isoformat()
    })
    save_transactions(txns)
    log_event(user, "ADD_MONEY", f"₹{amount} added")

    flash(f"₹{amount} added to wallet.")
    return redirect(url_for('dashboard'))


@app.route('/send', methods=['GET', 'POST'])
@login_required
def send():
    users = load_users()
    sender = session['user']
    other_users = [u for u in users if u != sender]

    if request.method == 'POST':
        receiver = request.form['receiver'].lower().strip()
        try:
            amount = float(request.form['amount'])
        except ValueError:
            flash("Enter a valid amount.")
            return redirect(url_for('send'))

        if receiver not in users:
            flash("Recipient does not exist.")
            return redirect(url_for('send'))
        if receiver == sender:
            flash("Cannot send money to yourself.")
            return redirect(url_for('send'))
        if amount <= 0:
            flash("Invalid amount.")
            return redirect(url_for('send'))
        if users[sender]['balance'] < amount:
            flash("Insufficient balance.")
            return redirect(url_for('send'))

        # Check for fraud patterns
        txns = load_transactions()
        status = check_fraud_patterns(sender, amount, txns)

        users[sender]['balance'] -= amount
        users[receiver]['balance'] += amount

        if "FRAUD" in status:
            users[sender]['flagged'] = True
            flash("Transaction flagged for review due to suspicious activity.")

        save_users(users)

        txns.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount,
            'status': status,
            'time': datetime.now().isoformat()
        })
        save_transactions(txns)
        log_event(sender, "SEND_MONEY", f"Sent ₹{amount} to {receiver}, Status: {status}")

        if "FRAUD" not in status:
            flash("Transaction successful.")
        return redirect(url_for('dashboard'))

    return render_template('send.html', users=other_users)


@app.route('/admin')
def admin():
    # Redirect if user is not admin
    if not is_admin():
        return redirect(url_for('login'))

    # Load transactions and users
    txns = load_transactions()
    users = load_users()

    # Get flagged transactions
    flagged_txns = [t for t in txns if 'FRAUD' in t.get('status', '')]

    # Get suspicious users
    suspicious_users = {}
    for email, user in users.items():
        if user.get('flagged'):
            suspicious_users[email] = user
        else:
            for t in txns:
                if t.get('sender') == email and 'FRAUD' in t.get('status', ''):
                    suspicious_users[email] = user
                    break

    # Calculate total system balance
    total_balance = sum(user.get('balance', 0) for user in users.values())

    # Get top 5 users by balance
    top_users = sorted(users.items(), key=lambda item: item[1].get('balance', 0), reverse=True)[:5]

    # Render the admin page
    return render_template(
        'admin.html',
        flagged_txns=flagged_txns,
        total_balance=total_balance,
        top_users=top_users,
        suspicious_users=suspicious_users
    )




@app.route('/report_fraud/<user_email>')
@login_required
def report_fraud(user_email):
    if not is_admin():
        flash("Access denied.")
        return redirect(url_for('dashboard'))

    users = load_users()
    if user_email in users:
        users[user_email]['flagged'] = True
        save_users(users)
        log_event(session['user'], "REPORT_FRAUD", f"Flagged {user_email}")

    flash(f"{user_email} marked as fraud.")
    return redirect(url_for('admin'))


@app.route('/clear_flag/<user_email>')
@login_required
def clear_flag(user_email):
    if not is_admin():
        flash("Access denied.")
        return redirect(url_for('dashboard'))

    users = load_users()
    if user_email in users:
        users[user_email]['flagged'] = False
        save_users(users)
        log_event(session['user'], "CLEAR_FLAG", f"Cleared flag for {user_email}")

    flash(f"{user_email} fraud flag cleared.")
    return redirect(url_for('admin'))


if __name__ == '__main__':
    app.run(debug=True)