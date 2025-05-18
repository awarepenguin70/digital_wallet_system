# Digital Wallet System with Cash Management and Fraud Detection

## Table of Contents
1. [Project Definition](#project-definition)
2. [Tech Stack](#tech-stack)
3. [Features](#features)
4. [File Structure](#file-structure)
5. [Installation & Setup](#installation--setup)
6. [Running the Application](#running-the-application)
7. [Requirements](#requirements)

## Project Definition

The Digital Wallet System is a secure web application that simulates a peer-to-peer digital payment platform with cash management and advanced fraud detection capabilities:

- User authentication and authorization
- Peer-to-peer financial transactions
- Real-time fraud detection mechanisms
- Administrative dashboard for oversight
- Comprehensive audit logging

Built with Python using the Flask framework, this system follows MVC architecture principles with modular blueprints and implements security best practices for financial applications.

## Tech Stack

### Core Technologies
- **Python (v3.8+)** - Primary programming language chosen for its readability and extensive libraries
- **Flask (v2.0+)** - Lightweight web framework that provides routing, templating, and request handling
- **JSON** - Simple, lightweight data interchange format used for storage

### Security
- **bcrypt** - Industry-standard password hashing for secure credential storage
- **Flask-Session** - Server-side session management
- **CSRF protection** - Built into Flask for form security
- **Rule-based fraud detection** - Custom transaction monitoring system

### Development Tools
- **PyCharm** - Professional IDE for Python development
- **Git/GitHub** - Version control and collaboration platform
- **Virtual Environment (venv)** - Dependency isolation

## Features

### User Features
- **Registration & Authentication**
    - Secure user registration with password hashing
    - Login/logout functionality
    - Session management

- **Wallet Management**
    - Balance viewing
    - Peer-to-peer money transfers
    - Wallet top-up functionality
    - Transaction history with timestamps

### Admin Features
- **Dashboard Overview**
    - System-wide transaction volume
    - Flagged transactions
    - Suspicious activity alerts

- **User Management**
    - View all registered users
    - See top users by transaction volume

- **Fraud Monitoring**
    - Review all flagged transactions
    - Analyze transaction patterns
    - System health metrics

### Security Features
- Real-time fraud detection with:
    - Large transaction threshold monitoring
    - Frequency analysis of transactions
    - Percentage-based withdrawal alerts
- Complete audit trail of all transactions
- Role-based access control (RBAC) for admin functions

## File Structure

```
digital_wallet_system/
├── application/               # Core application package
│   ├── __init__.py           # Application factory and setup
│   ├── config.py             # Configuration settings
│   ├── models/               # Data models
│   │   ├── __init__.py       # Models exports
│   │   ├── user.py           # User model and operations
│   │   └── transaction.py    # Transaction model and operations
│   ├── utils/                # Utility classes
│   │   ├── __init__.py       # Utilities exports
│   │   ├── decorators.py     # Authentication decorators
│   │   ├── helpers.py        # Helper functions
│   │   └── fraud_detection.py # Fraud detection logic
│   └── blueprints/           # Route handlers
│       ├── __init__.py       # Blueprints exports
│       ├── auth.py           # Authentication routes
│       ├── transactions.py   # Transaction routes
│       └── admin.py          # Admin routes
├── templates/                # HTML templates
│   ├── admin.html            # Admin dashboard
│   ├── dashboard.html        # User dashboard
│   ├── login.html            # Login page
│   ├── register.html         # Registration page
│   └── send.html             # Money transfer page
├── static/                   # Static assets (CSS/JS/Images)
├── app.py                    # Application entry point
├── requirements.txt          # Dependency list
├── users.json                # User data storage
├── transactions.json         # Transaction records
└── audit_log.json            # System activity log
```

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone [repository-url]
   cd digital_wallet_system
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize data files**
   ```bash
   touch users.json transactions.json audit_log.json
   echo "{}" > users.json
   echo "[]" > transactions.json
   echo "[]" > audit_log.json
   ```

5. **Set up admin account**
    - After first run, manually add admin user to users.json:
      ```json
      "admin@dffdp.com": {
        "password": "123",
        "balance": 0,
        "is_admin": true
      }
      ```

## Running the Application

1. **Start the development server**
   ```bash
   python app.py
   ```

2. **Access the application**
    - Open browser to: `http://localhost:5000`

3. **Key Endpoints**
    - `/` - Landing page with login redirect
    - `/login` - User authentication
    - `/register` - New user registration
    - `/dashboard` - Wallet overview
    - `/send` - Peer-to-peer payment interface
    - `/admin` - Administrative console (admin-only)
