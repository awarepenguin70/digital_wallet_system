# Digital Wallet System with Fraud Detection 

A secure peer-to-peer digital payment platform with real-time fraud detection, cash management, and comprehensive administrative oversight. Built with Flask and designed with financial security best practices.

## Overview

The Digital Wallet System simulates a modern fintech application that enables users to:
- Create secure digital wallets
- Transfer money between users instantly
- Monitor transaction history
- Detect and prevent fraudulent activities
- Manage accounts through an admin dashboard

This system follows MVC architecture principles with modular blueprints and implements industry-standard security measures for financial applications.

## Features

### User Features

#### Authentication & Security
- **Secure Registration**: Password hashing using bcrypt
- **Session Management**: Server-side sessions with Flask-Session
- **Login/Logout**: Protected authentication flow
- **CSRF Protection**: Built-in form security

#### Wallet Operations
- **Balance Viewing**: Real-time wallet balance display
- **Peer-to-Peer Transfers**: Send money to other users instantly
- **Wallet Top-up**: Add funds to your wallet
- **Transaction History**: Complete record with timestamps and status

### Admin Features

#### Dashboard Overview
- System-wide transaction volume metrics
- Flagged transaction summary
- Suspicious activity alerts
- User activity monitoring

#### User Management
- View all registered users
- Top users by transaction volume
- User wallet balances
- Account status tracking

#### Fraud Monitoring
- Review all flagged transactions
- Analyze transaction patterns
- System health metrics
- Audit log access

### Security & Fraud Detection

#### Real-Time Fraud Detection
- **Large Transaction Monitoring**: Flags transactions above threshold (₹10,000)
- **Frequency Analysis**: Detects rapid successive transactions
- **Withdrawal Alerts**: Monitors percentage-based large withdrawals
- **Pattern Recognition**: Identifies suspicious transaction patterns

#### Security Measures
- Bcrypt password hashing (12 rounds)
- Server-side session management
- CSRF token validation
- Role-based access control (RBAC)
- Complete audit trail
- Input validation and sanitization

## Tech Stack

### Backend
- **Python 3.8+**: Core programming language
- **Flask 2.0+**: Web framework
- **bcrypt**: Password hashing
- **Flask-Session**: Session management

### Data Storage
- **JSON**: Lightweight file-based storage
  - `users.json`: User credentials and profiles
  - `transactions.json`: Transaction records
  - `audit_log.json`: System activity logs

### Frontend
- **HTML5/CSS3**: UI templates
- **Jinja2**: Template engine
- **Bootstrap** (optional): Responsive design

### Development
- **PyCharm**: IDE
- **Git/GitHub**: Version control
- **venv**: Virtual environment

## Project Structure

```
digital_wallet_system/
├── application/                    # Core application package
│   ├── __init__.py                # Application factory
│   ├── config.py                  # Configuration settings
│   │
│   ├── models/                    # Data models
│   │   ├── __init__.py           # Model exports
│   │   ├── user.py               # User model & operations
│   │   └── transaction.py        # Transaction model & operations
│   │
│   ├── utils/                     # Utility modules
│   │   ├── __init__.py           # Utility exports
│   │   ├── decorators.py         # Auth decorators
│   │   ├── helpers.py            # Helper functions
│   │   └── fraud_detection.py    # Fraud detection engine
│   │
│   └── blueprints/                # Route handlers
│       ├── __init__.py           # Blueprint exports
│       ├── auth.py               # Authentication routes
│       ├── transactions.py       # Transaction routes
│       └── admin.py              # Admin routes
│
├── templates/                     # HTML templates
│   ├── admin.html                # Admin dashboard
│   ├── dashboard.html            # User dashboard
│   ├── login.html                # Login page
│   ├── register.html             # Registration page
│   └── send.html                 # Money transfer page
│
├── static/                        # Static assets
│   ├── css/                      # Stylesheets
│   ├── js/                       # JavaScript files
│   └── images/                   # Images
│
├── app.py                        # Application entry point
├── requirements.txt              # Python dependencies
├── users.json                    # User data (created on run)
├── transactions.json             # Transaction records
├── audit_log.json               # System audit log
└── README.md                    # This file
```

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Git (for version control)

### Step-by-Step Installation

1. **Clone the repository**:

```bash
git clone https://github.com/awarepenguin70/digital_wallet_system.git
cd digital_wallet_system
```

2. **Create and activate virtual environment**:

```bash
# On Windows
python -m venv venv
.\venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

The `requirements.txt` should contain:

```
Flask>=2.0.0
Flask-Session>=0.4.0
bcrypt>=3.2.0
```

4. **Initialize data files**:

```bash
# On Windows
type nul > users.json
type nul > transactions.json
type nul > audit_log.json

# On macOS/Linux
touch users.json transactions.json audit_log.json
```

Then populate with initial structure:

```bash
# On Windows (PowerShell)
echo '{}' | Out-File -Encoding ASCII users.json
echo '[]' | Out-File -Encoding ASCII transactions.json
echo '[]' | Out-File -Encoding ASCII audit_log.json

# On macOS/Linux
echo "{}" > users.json
echo "[]" > transactions.json
echo "[]" > audit_log.json
```

5. **Configure the application**:

Edit `application/config.py` if needed:

```python
class Config:
    SECRET_KEY = 'your-secret-key-here'  # Change in production
    SESSION_TYPE = 'filesystem'
    FRAUD_THRESHOLD = 10000  # Transaction amount threshold
```

## Running the Application

### Start the Development Server

```bash
python app.py
```

The application will start on `http://localhost:5000`

### Default Admin Account

After first run, create an admin account by editing `users.json`:

```json
{
  "admin@wallet.com": {
    "password": "$2b$12$hashed_password_here",
    "balance": 0,
    "is_admin": true,
    "created_at": "2025-01-01T00:00:00"
  }
}
```

Or use the registration flow and manually set `"is_admin": true` in the JSON file.

### Key Endpoints

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/` | GET | Landing page | No |
| `/register` | GET/POST | User registration | No |
| `/login` | GET/POST | User authentication | No |
| `/logout` | GET | End session | Yes |
| `/dashboard` | GET | User wallet overview | Yes |
| `/send` | GET/POST | P2P payment interface | Yes |
| `/topup` | POST | Add funds to wallet | Yes |
| `/transactions` | GET | Transaction history | Yes |
| `/admin` | GET | Admin dashboard | Admin Only |
| `/admin/users` | GET | User management | Admin Only |
| `/admin/fraud` | GET | Fraud monitoring | Admin Only |

## Usage Guide

### For Regular Users

1. **Register an Account**:
   - Navigate to `/register`
   - Provide email and password
   - Initial wallet balance: ₹0

2. **Top Up Your Wallet**:
   - Go to dashboard
   - Click "Top Up"
   - Enter amount
   - Funds added instantly

3. **Send Money**:
   - Click "Send Money"
   - Enter recipient email
   - Enter amount
   - Confirm transaction
   - Transaction logged and fraud-checked

4. **View History**:
   - Access transaction history from dashboard
   - See all incoming and outgoing transactions
   - Check transaction status and timestamps

### For Administrators

1. **Access Admin Dashboard**:
   - Log in with admin account
   - Navigate to `/admin`

2. **Monitor Transactions**:
   - View system-wide transaction volume
   - Check flagged transactions
   - Analyze user activity patterns

3. **User Management**:
   - View all registered users
   - Check user balances
   - Identify top transactors

4. **Fraud Detection**:
   - Review flagged transactions
   - Analyze suspicious patterns
   - Access detailed audit logs

## Fraud Detection Rules

The system automatically flags transactions based on:

### Rule 1: Large Transaction Amount
```python
if amount > 10000:
    flag_transaction("Large transaction amount")
```

### Rule 2: Rapid Transactions
```python
if user_made_transaction_in_last_5_minutes():
    flag_transaction("Frequent transactions detected")
```

### Rule 3: Large Withdrawal Percentage
```python
if amount > (user_balance * 0.8):
    flag_transaction("Large withdrawal percentage")
```

### Customizing Fraud Rules

Edit `application/utils/fraud_detection.py`:

```python
class FraudDetector:
    LARGE_AMOUNT_THRESHOLD = 10000  # Adjust threshold
    RAPID_TRANSACTION_WINDOW = 300   # 5 minutes in seconds
    LARGE_WITHDRAWAL_PERCENT = 0.8   # 80% of balance
```

## Data Models

### User Model (`users.json`)

```json
{
  "user@example.com": {
    "password": "$2b$12$...",
    "balance": 5000.00,
    "is_admin": false,
    "created_at": "2025-01-15T10:30:00",
    "last_login": "2025-01-20T14:45:00"
  }
}
```

### Transaction Model (`transactions.json`)

```json
[
  {
    "id": "txn_1234567890",
    "from": "sender@example.com",
    "to": "receiver@example.com",
    "amount": 1000.00,
    "timestamp": "2025-01-20T15:30:00",
    "status": "completed",
    "flagged": false,
    "flag_reason": null
  }
]
```

### Audit Log (`audit_log.json`)

```json
[
  {
    "timestamp": "2025-01-20T15:30:00",
    "user": "user@example.com",
    "action": "login",
    "ip_address": "127.0.0.1",
    "status": "success"
  }
]
```

## Security Best Practices

### Implemented Security Measures

 **Password Security**
- Bcrypt hashing with 12 rounds
- No plaintext password storage
- Strong password requirements

 **Session Security**
- Server-side session storage
- Secure session cookies
- Automatic session expiration

 **Transaction Security**
- Balance validation before transfer
- Atomic transaction operations
- Transaction rollback on failure

 **Access Control**
- Role-based permissions
- Decorator-based auth checks
- Admin-only route protection

