from flask import Blueprint, render_template, flash, redirect, url_for, session
from ..models.user import User
from ..models.transaction import Transaction
from ..utils.decorators import admin_required
from ..utils.helpers import Logger

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
@admin_required
def admin_dashboard():
    flagged_txns = Transaction.get_flagged_transactions()
    users = User.load_users()

    suspicious_users = {email: user for email, user in users.items()
                        if user['flagged'] or any(t['sender'] == email and 'FRAUD' in t['status']
                                                  for t in Transaction.load_transactions())}

    total_balance = sum(user['balance'] for user in users.values())
    top_users = sorted(users.items(), key=lambda item: item[1]['balance'], reverse=True)[:5]

    return render_template('admin.html',
                           flagged_txns=flagged_txns,
                           total_balance=total_balance,
                           top_users=top_users,
                           suspicious_users=suspicious_users)

@admin_bp.route('/report_fraud/<user_email>')
@admin_required
def report_fraud(user_email):
    if User.flag_user(user_email):
        Logger.log_event(session['user'], "REPORT_FRAUD", f"Flagged {user_email}")
        flash(f"{user_email} marked as fraud.")
    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/clear_flag/<user_email>')
@admin_required
def clear_flag(user_email):
    if User.flag_user(user_email, False):
        Logger.log_event(session['user'], "CLEAR_FLAG", f"Cleared flag for {user_email}")
        flash(f"{user_email} fraud flag cleared.")
    return redirect(url_for('admin.admin_dashboard'))