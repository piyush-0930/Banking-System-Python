import os
import hashlib
import datetime
import random

ACCOUNTS_FILE = "accounts.txt"
TRANSACTIONS_FILE = "transactions.txt"

# ----------------- Utility Functions ----------------- #
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_accounts():
    accounts = {}
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, "r") as f:
            for line in f:
                acc_no, name, pwd, balance = line.strip().split(",")
                accounts[acc_no] = {"name": name, "password": pwd, "balance": float(balance)}
    return accounts

def save_accounts(accounts):
    with open(ACCOUNTS_FILE, "w") as f:
        for acc_no, info in accounts.items():
            f.write(f"{acc_no},{info['name']},{info['password']},{info['balance']}\n")

def log_transaction(acc_no, trans_type, amount):
    date = datetime.date.today()
    with open(TRANSACTIONS_FILE, "a") as f:
        f.write(f"{acc_no},{trans_type},{amount},{date}\n")

def generate_account_number():
    return str(random.randint(100000, 999999))

# ----------------- Main Features ----------------- #
def create_account():
    accounts = load_accounts()
    name = input("Enter your name: ")
    while True:
        try:
            deposit = float(input("Enter your initial deposit: "))
            if deposit < 0:
                raise ValueError
            break
        except ValueError:
            print("Invalid input. Enter a non-negative number.")
    acc_no = generate_account_number()
    while acc_no in accounts:
        acc_no = generate_account_number()
    pwd = input("Create a password: ")
    hashed_pwd = hash_password(pwd)
    accounts[acc_no] = {"name": name, "password": hashed_pwd, "balance": deposit}
    save_accounts(accounts)
    log_transaction(acc_no, "Deposit", deposit)
    print(f"\nAccount created successfully!")
    print(f"Your account number: {acc_no} (Save this for login)\n")

def login():
    accounts = load_accounts()
    acc_no = input("Enter your account number: ")
    pwd = input("Enter your password: ")
    hashed_pwd = hash_password(pwd)
    if acc_no in accounts and accounts[acc_no]["password"] == hashed_pwd:
        print(f"\nWelcome, {accounts[acc_no]['name']}!")
        user_menu(acc_no, accounts)
    else:
        print("Invalid account number or password.\n")

def user_menu(acc_no, accounts):
    while True:
        print("\nSelect an option:")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Check Balance")
        print("4. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            try:
                amount = float(input("Enter amount to deposit: "))
                if amount <= 0:
                    raise ValueError
                accounts[acc_no]["balance"] += amount
                save_accounts(accounts)
                log_transaction(acc_no, "Deposit", amount)
                print(f"Deposit successful! New balance: ₹{accounts[acc_no]['balance']:.2f}")
            except ValueError:
                print("Invalid input. Enter a valid amount.")
        elif choice == "2":
            try:
                amount = float(input("Enter amount to withdraw: "))
                if amount <= 0:
                    raise ValueError
                if accounts[acc_no]["balance"] >= amount:
                    accounts[acc_no]["balance"] -= amount
                    save_accounts(accounts)
                    log_transaction(acc_no, "Withdrawal", amount)
                    print(f"Withdrawal successful! New balance: ₹{accounts[acc_no]['balance']:.2f}")
                else:
                    print("Insufficient balance.")
            except ValueError:
                print("Invalid input. Enter a valid amount.")
        elif choice == "3":
            print(f"Current balance: ₹{accounts[acc_no]['balance']:.2f}")
        elif choice == "4":
            print("Logged out.\n")
            break
        else:
            print("Invalid choice. Try again.")

# ----------------- Entry Point ----------------- #
def main():
    while True:
        print("\n" + "-" * 40)
        print("Welcome to the Secure Banking System")
        print("-" * 40)
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            create_account()
        elif choice == "2":
            login()
        elif choice == "3":
            print("Thank you for using the Banking System. Goodbye!\n")
            break
        else:
            print("Invalid input. Please select a valid option.")

if __name__ == "__main__":
    main()
