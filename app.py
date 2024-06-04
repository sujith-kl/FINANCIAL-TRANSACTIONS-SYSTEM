import sqlite3
import hashlib
import random

class Data:
    def __init__(self, name=None, password=None):
        self.user_name = name
        self.password = password
        self.balance = 0
        self.conn = sqlite3.connect('user_data.db')
        self.cursor = self.conn.cursor()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def checking(self):
        input_name = self.user_name.lower().strip()
        input_password = self.hash_password(self.password.strip())
        query = "SELECT * FROM users WHERE LOWER(name)=? AND password=?"
        self.cursor.execute(query, (input_name, input_password))
        user = self.cursor.fetchone()
        if user:
            print("Logged in successfully")
            self.balance = user[3]
            return True
        else:
            return "Invalid inputs"

    def generate_otp(self):
        return random.randint(100, 9999)

    def hash_otp(self, otp):
        return hashlib.sha256(str(otp).encode()).hexdigest()

    def otp(self):
        otp = self.generate_otp()
        hashed_otp = self.hash_otp(otp)
        print(f"OTP: {otp}")
        otpin = input("Enter OTP: ")
        if hashed_otp == self.hash_otp(otpin):
            self.otp_status = True
            return self.otp_status
        else:
            return "INVALID OTP"

    def check_balance(self):
        otp = self.otp()
        if otp == True:
            return f"Balance: Rs.{self.balance}"
        else:
            return otp

    def deposit_money(self, amount):
        self.balance += amount
        self.cursor.execute("UPDATE users SET balance = ? WHERE LOWER(name) = ?", (self.balance, self.user_name.lower()))
        self.conn.commit()
        print(f"Deposited Rs.{amount} successfully")
        print(f"New Balance: Rs.{self.balance}")

    def withdraw_money(self, amount):
        if amount > self.balance:
            print("Insufficient funds")
            return
        self.balance -= amount
        self.cursor.execute("UPDATE users SET balance = ? WHERE LOWER(name) = ?", (self.balance, self.user_name.lower()))
        self.conn.commit()
        print(f"Withdrew Rs.{amount} successfully")
        print(f"New Balance: Rs.{self.balance}")

    def add_user(self, name, password):
        hashed_password = self.hash_password(password)
        self.cursor.execute("INSERT INTO users (name, password, balance) VALUES (?, ?, 0)", (name, hashed_password))
        self.conn.commit()
        print("User added successfully")

    def start(self):
        print("""SELECT
            1. Login
            2. Add User
            3. Exit""")
        choice = input("Select: ")
        if choice == '1':
            enter_name = input("ENTER A NAME: ")
            enter_pass = input("ENTER A PASSWORD: ")
            self.user_name = enter_name
            self.password = enter_pass
            login = self.checking()
            if login == True:
                while True:
                    print("""SELECT
                        1. Balance Enquiry
                        2. Deposit Money
                        3. Withdraw Money
                        4. Exit""")
                    choice = input("Select: ")
                    if choice == '1':
                        print(self.check_balance())
                    elif choice == '2':
                        amount = int(input("Enter amount to deposit: "))
                        self.deposit_money(amount)
                    elif choice == '3':
                        amount = int(input("Enter amount to withdraw: "))
                        self.withdraw_money(amount)
                    elif choice == '4':
                        return
                    else:
                        print("Error")
            else:
                print("Login failed")
        elif choice == '2':
            new_name = input("ENTER NEW USER NAME: ")
            new_pass = input("ENTER NEW USER PASSWORD: ")
            self.add_user(new_name, new_pass)
        elif choice == '3':
            return
        else:
            print("Error")

if __name__ == "__main__":
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        password TEXT,
                        balance INTEGER DEFAULT 50000
                    )''')
    conn.commit()
    
    cursor.execute("SELECT * FROM users")
    if not cursor.fetchall():
        cursor.execute("INSERT INTO users (name, password, balance) VALUES ('user1', ?, 10000)", (hash_password('133'),))
        conn.commit()
        cursor.execute("INSERT INTO users (name, password, balance) VALUES ('test', ?, 20000)", (hash_password('123'),))
        conn.commit()
    
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    print(users) 

    run = Data()
    run.start()
