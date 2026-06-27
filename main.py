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

    def depositMoney(self): #first user valid accNum and pass
        account_number = input("Enter your account number: ").strip()
        pin = input("Enter your PIN: ").strip()
        
        # Validate account and pin
        for account in self.data:
            if account["account_number"] == account_number and account["pin"] == pin:
                print("Account validated successfully")
                return account
        
        print("Invalid account number or PIN")
        return None
    
    # this is a public method
    def createBankAccount(self):
        name = input("Enter your name: ").strip()
        age = int(input("Enter your age: "))
        if age < 18:
            print("You must be at least 18 years old to create an account.")
            return
        email = input("Enter your email: ").strip()
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
        print("Withdraw selected")
    elif check == 4:
        print("Account Details selected")
    elif check == 5:
        print("Update Details selected")
    elif check == 6:
        print("Delete Account selected")
    elif check == 9:
        print("Exiting...")
        break
    else:
        print("Invalid selection")


