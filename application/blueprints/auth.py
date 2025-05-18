from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from ..models.user import User
from ..utils.helpers import Logger
from ..utils.decorators import login_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].lower().strip()
        password = request.form['password']
        user = User.get_user(email)

        if user and user['password'] == password:
            session['user'] = email
            Logger.log_event(email, "LOGIN")
            return redirect(url_for('transactions.dashboard'))
        else:
            flash("Invalid credentials.")
            return redirect(url_for('auth.login'))

    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email'].lower().strip()
        password = request.form['password']

        if User.create_user(email, password):
            flash("Registered successfully!")
            return redirect(url_for('auth.login'))
        else:
            flash("User already exists.")
            return redirect(url_for('auth.register'))

    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    Logger.log_event(session.get('user', 'Unknown'), "LOGOUT")
    session.pop('user', None)
    flash("Logged out.")
    return redirect(url_for('auth.login'))