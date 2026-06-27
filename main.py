import json
import random
import string
from pathlib import Path

class Bank:
    
    database = 'data.json' #path de diya
    data = [] #it will be having dummy data
    try:
        if Path(database).exists():
            with open (database) as fs: #by def reading phase
                data = json.loads(fs.read())
        else:
            print("There is no file to the path given")   
    except Exception as error:
        print(f"Exception occured {error}")
        
    
    @staticmethod # not for all its a decorator
    def __update():
        with open(Bank.database, "w", encoding="utf-8") as fs:
            fs.write(json.dumps(Bank.data)) #data dumping

    @classmethod
    def __accountNumGenerate(cls):
        alpha = random.choices(string.ascii_letters, k=3)
        num = random.choices(string.digits, k=3)
        spchar = random.choices("!@#$%^&*", k=1)

        account_id = alpha + num + spchar
        random.shuffle(account_id)

        return "".join(account_id)

    def __authenticate(self):
        account_number = input("Enter account number: ").strip()
        pin = input("Enter PIN: ").strip()

        for account in self.data:
            if account["account_number"] == account_number and account["pin"] == pin:
                return account

        print("Invalid account number or PIN")
        return None

    def depositMoney(self):
        userAccount = self.__authenticate()

        if userAccount is None:
            return

        amt = int(input("Enter amount you want to deposit: "))
        if amt <= 0:
            print("Deposit amount must be positive.")
            return
        userAccount["balance"] += amt

        self.__update()

        print(f"Updated Balance = {userAccount['balance']}")
        
        
    def withdrawMoney(self):
        userAccount = self.__authenticate()

        if userAccount is None:
            return

        amt = int(input("Enter amount you want to withdraw: "))
        if amt <= 0:
            print("Withdrawal amount must be positive")
            return

        if amt > userAccount["balance"]:
            print("Insufficient balance")
            return

        userAccount["balance"] -= amt

        self.__update()
        print(f"Withrawn Balance = {amt}")
        print(f"Updated Balance = {userAccount['balance']}")
    
    def accountDetails(self):
        userAccount = self.__authenticate()

        if userAccount is None:
            return

        print("\nAccount Details")
        print(f"Name: {userAccount['name']}")
        print(f"Age: {userAccount['age']}")
        print(f"Email: {userAccount['email']}")
        print(f"Account Number: {userAccount['account_number']}")
        print(f"Balance: {userAccount['balance']}")
    
    def updateAccountDetails(self):
        userAccount = self.__authenticate()

        if userAccount is None:
            return


        print("\nWhat do you want to update?")
        print("1. Name")
        print("2. Email")
        print("3. PIN")
        print("4. Age")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            new_name = input("Enter new name: ").strip()

            if not new_name:
                print("Name cannot be empty.")
                return

            userAccount["name"] = new_name

        elif choice == "2":
            new_email = input("Enter new email: ").strip()

            if not new_email:
                print("Email cannot be empty.")
                return

            userAccount["email"] = new_email

        elif choice == "3":
            new_pin = input("Enter new 4-digit PIN: ").strip()

            if len(new_pin) != 4 or not new_pin.isdigit():
                print("PIN must be exactly 4 digits.")
                return

            userAccount["pin"] = new_pin
            
        elif choice == "4":
            new_age = int(input("Enter new age :- "))

            if (new_age) < 18 :
                print("Age must be greater than equal to 18.")
                return

            userAccount["age"] = new_age

        else:
            print("Invalid choice.")
            return

        self.__update()

        print("\nAccount Updated Successfully!")
        print(f"Name           : {userAccount['name']}")
        print(f"Age            : {userAccount['age']}")
        print(f"Pin            : {userAccount['pin']}")
        print(f"Email          : {userAccount['email']}")
        print(f"Account Number : {userAccount['account_number']}")
        print(f"Balance        : {userAccount['balance']}")
    
    
    def deleteAccount(self):
        userAccount = self.__authenticate()

        if userAccount is None:
            return

        print("\nAccount Details")
        print(f"Name           : {userAccount['name']}")
        print(f"Age            : {userAccount['age']}")
        print(f"Email          : {userAccount['email']}")
        print(f"Account Number : {userAccount['account_number']}")
        print(f"Balance        : {userAccount['balance']}")

        choice = input("\nAre you sure you want to delete this account? (Y/N): ").strip().upper()

        if choice == "Y":
            self.data.remove(userAccount)
            self.__update()
            print("Account deleted successfully.")
        else:
            print("Account deletion cancelled.")
    
    # this is a public method
    def createBankAccount(self):
        name = input("Enter your name: ").strip()
        age = int(input("Enter your age: "))
        if age < 18:
            print("You must be at least 18 years old to create an account.")
            return
        email = input("Enter your email: ").strip()
        for account in self.data:
            if account["email"] == email:
                print("Email already exists.")
                return
        pin = input("Enter your pin: ").strip()
        if len(pin) != 4:
            print("PIN must be exactly 4 characters long.")
            return
        # account_number = cls.__accountNumGenerate()
        account_number = self._Bank__accountNumGenerate()
        data = {
            "name": name,
            "age": age,
            "email": email,
            "pin": pin,
            "account_number": account_number,
            "balance": 0
        }
        self.data.append(data)
        self.__update()
        # print account details 
        
        print("\nAccount Details")
        print(f"Name           : {data['name']}")
        print(f"Age            : {data['age']}")
        print(f"Email          : {data['email']}")
        print(f"Pin          : {data['pin']}")
        print(f"Account Number : {data['account_number']}")
        print(f"Balance        : {data['balance']}")
        
        print("Account has been successfully created")


user = Bank() 
print("Welcome to Bank Management")
print("Press 1 for Create Account: open a new bank account")
print("Press 2 for Deposit: add money to the account")
print("Press 3 for Withdraw: take money out of the account")
print("Press 4 for Account Details: view account information")
print("Press 5 for Update Details: change account information")
print("Press 6 for Delete Account: remove the account")
print("Press 9 to Exit")

while True:
    try:
        check = int(input("Enter Your Response :- "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        continue

    if check == 1:
        user.createBankAccount()
        print("Create Account selected")
    elif check == 2:
        user.depositMoney()
        print("Deposit selected")
    elif check == 3:
        user.withdrawMoney()
        print("Withdraw selected")
    elif check == 4:
        user.accountDetails()
        print("Account Details selected")
    elif check == 5:
        user.updateAccountDetails()
        print("Update Details selected")
    elif check == 6:
        user.deleteAccount()
        print("Delete Account selected")
    elif check == 9:
        print("Exiting...")
        break
    else:
        print("Invalid selection")


