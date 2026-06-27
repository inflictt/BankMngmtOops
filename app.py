import json
import random
import string
from pathlib import Path

import streamlit as st


# ----------------------------- Logic Layer -----------------------------
class Bank:

    database = 'data.json'  # path de diya
    data = []  # it will be having dummy data

    @classmethod
    def load(cls):  # read file
        try:
            if Path(cls.database).exists():
                with open(cls.database) as fs:  # by def reading phase
                    cls.data = json.loads(fs.read())
            else:
                cls.data = []  # no file
        except Exception as error:
            cls.data = []  # safe fallback
            print(f"Exception occured {error}")

    @staticmethod  # not for all its a decorator
    def __update():
        with open(Bank.database, "w", encoding="utf-8") as fs:
            fs.write(json.dumps(Bank.data))  # data dumping

    @classmethod
    def __accountNumGenerate(cls):  # id maker
        alpha = random.choices(string.ascii_letters, k=3)
        num = random.choices(string.digits, k=3)
        spchar = random.choices("!@#$%^&*", k=1)

        account_id = alpha + num + spchar
        random.shuffle(account_id)

        return "".join(account_id)

    @classmethod
    def authenticate(cls, account_number, pin):  # login check
        for account in cls.data:
            if account["account_number"] == account_number and account["pin"] == pin:
                return account
        return None  # no match

    @classmethod
    def find(cls, account_number):  # fetch account
        for account in cls.data:
            if account["account_number"] == account_number:
                return account
        return None  # not found

    @classmethod
    def create_account(cls, name, age, email, pin):  # new account
        # validations
        if not name:
            return False, "Name cannot be empty."
        if age < 18:
            return False, "You must be at least 18 years old to create an account."
        if not email:
            return False, "Email cannot be empty."
        for account in cls.data:
            if account["email"] == email:
                return False, "Email already exists."
        if len(pin) != 4 or not pin.isdigit():
            return False, "PIN must be exactly 4 digits."

        account_number = cls.__accountNumGenerate()  # gen id
        record = {  # account schema
            "name": name,
            "age": age,
            "email": email,
            "pin": pin,
            "account_number": account_number,
            "balance": 0,
        }
        cls.data.append(record)
        cls.__update()
        return True, record  # success

    @classmethod
    def deposit(cls, account_number, amount):  # add money
        account = cls.find(account_number)
        if account is None:
            return False, "Account not found."
        if amount <= 0:
            return False, "Deposit amount must be positive."
        account["balance"] += amount
        cls.__update()
        return True, account["balance"]  # new balance

    @classmethod
    def withdraw(cls, account_number, amount):  # take money
        account = cls.find(account_number)
        if account is None:
            return False, "Account not found."
        if amount <= 0:
            return False, "Withdrawal amount must be positive."
        if amount > account["balance"]:
            return False, "Insufficient balance."
        account["balance"] -= amount
        cls.__update()
        return True, account["balance"]  # new balance

    @classmethod
    def update_field(cls, account_number, field, value):  # edit account
        account = cls.find(account_number)
        if account is None:
            return False, "Account not found."
        account[field] = value
        cls.__update()
        return True, account  # updated record

    @classmethod
    def delete(cls, account_number):  # remove account
        account = cls.find(account_number)
        if account is None:
            return False, "Account not found."
        cls.data.remove(account)
        cls.__update()
        return True, "Account deleted successfully."  # done


# ----------------------------- Helpers -----------------------------
def show_account(account):  # detail card
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Name:** {account['name']}")
        st.write(f"**Age:** {account['age']}")
        st.write(f"**Email:** {account['email']}")
    with col2:
        st.write(f"**Account Number:** `{account['account_number']}`")
        st.write(f"**Balance:** ₹ {account['balance']}")


def do_logout():  # clear session
    st.session_state.logged_in = False
    st.session_state.acc_no = None


def flash(message, kind="success"):  # queue message
    st.session_state.flash_msg = (kind, message)


def show_flash():  # render queued message
    if st.session_state.get("flash_msg"):
        kind, message = st.session_state.flash_msg
        getattr(st, kind)(message)  # st.success / st.error / st.info
        st.session_state.flash_msg = None  # clear once shown


# ----------------------------- Screens -----------------------------
def auth_screen():  # logged out view
    login_tab, create_tab = st.tabs(["🔑 Login", "🆕 Create Account"])

    # ---- login ----
    with login_tab:
        st.subheader("Login to your account")
        acc = st.text_input("Account Number", key="login_acc")
        pin = st.text_input("PIN", type="password", key="login_pin")

        if st.button("Login", type="primary"):
            account = Bank.authenticate(acc.strip(), pin.strip())
            if account:
                st.session_state.logged_in = True
                st.session_state.acc_no = account["account_number"]
                st.rerun()  # refresh view
            else:
                st.error("Invalid account number or PIN")

    # ---- create ----
    with create_tab:
        st.subheader("Open a new account")
        name = st.text_input("Name", key="c_name")
        age = st.number_input("Age", min_value=0, max_value=120, step=1, key="c_age")
        email = st.text_input("Email", key="c_email")
        pin = st.text_input("4-digit PIN", type="password", max_chars=4, key="c_pin")

        if st.button("Create Account", type="primary"):
            ok, result = Bank.create_account(
                name.strip(), int(age), email.strip(), pin.strip()
            )
            if ok:
                st.success("Account has been successfully created")
                st.info(f"Save this Account Number to log in: **{result['account_number']}**")
                show_account(result)  # show details
                st.balloons()
            else:
                st.error(result)


def dashboard():  # logged in view
    account = Bank.find(st.session_state.acc_no)
    if account is None:  # account got deleted
        do_logout()
        st.rerun()

    # ---- sidebar ----
    with st.sidebar:
        st.write(f"👤 **{account['name']}**")
        st.caption(account["account_number"])
        st.metric("Balance", f"₹ {account['balance']}")
        page = st.radio(  # menu nav
            "Menu",
            ["📋 Details", "💰 Deposit", "🏧 Withdraw", "✏️ Update", "🗑️ Delete"],
            key="nav",
        )
        st.divider()
        if st.button("Logout"):
            do_logout()
            st.rerun()

    # ---- details ----
    if page == "📋 Details":
        st.subheader("Account Details")
        show_account(account)

    # ---- deposit ----
    elif page == "💰 Deposit":
        st.subheader("Deposit Money")
        amt = st.number_input(
            "Enter amount you want to deposit", min_value=0, step=100, key="dep_amt"
        )
        if st.button("Deposit", key="dep_btn"):
            ok, result = Bank.deposit(account["account_number"], int(amt))
            if ok:
                flash(f"Deposited ₹ {int(amt)} — Updated Balance = ₹ {result}")
                st.rerun()  # refresh balance
            else:
                st.error(result)

    # ---- withdraw ----
    elif page == "🏧 Withdraw":
        st.subheader("Withdraw Money")
        amt = st.number_input(
            "Enter amount you want to withdraw", min_value=0, step=100, key="wd_amt"
        )
        if st.button("Withdraw", key="wd_btn"):
            ok, result = Bank.withdraw(account["account_number"], int(amt))
            if ok:
                flash(f"Withdrawn ₹ {int(amt)} — Updated Balance = ₹ {result}")
                st.rerun()  # refresh balance
            else:
                st.error(result)

    # ---- update ----
    elif page == "✏️ Update":
        st.subheader("Update Details")
        field = st.selectbox("What do you want to update?", ["Name", "Email", "PIN", "Age"])

        if field == "Name":
            new_name = st.text_input("Enter new name", key="u_name")
            if st.button("Save", key="u_name_btn"):
                if not new_name.strip():
                    st.error("Name cannot be empty.")
                else:
                    Bank.update_field(account["account_number"], "name", new_name.strip())
                    flash("Account Updated Successfully!")
                    st.rerun()

        elif field == "Email":
            new_email = st.text_input("Enter new email", key="u_email")
            if st.button("Save", key="u_email_btn"):
                if not new_email.strip():
                    st.error("Email cannot be empty.")
                else:
                    Bank.update_field(account["account_number"], "email", new_email.strip())
                    flash("Account Updated Successfully!")
                    st.rerun()

        elif field == "PIN":
            new_pin = st.text_input("Enter new 4-digit PIN", type="password", max_chars=4, key="u_pin")
            if st.button("Save", key="u_pin_btn"):
                if len(new_pin) != 4 or not new_pin.isdigit():
                    st.error("PIN must be exactly 4 digits.")
                else:
                    Bank.update_field(account["account_number"], "pin", new_pin)
                    flash("Account Updated Successfully!")
                    st.rerun()

        elif field == "Age":
            new_age = st.number_input("Enter new age", min_value=0, max_value=120, step=1, key="u_age")
            if st.button("Save", key="u_age_btn"):
                if int(new_age) < 18:
                    st.error("Age must be greater than equal to 18.")
                else:
                    Bank.update_field(account["account_number"], "age", int(new_age))
                    flash("Account Updated Successfully!")
                    st.rerun()

    # ---- delete ----
    elif page == "🗑️ Delete":
        st.subheader("Delete Account")
        show_account(account)
        confirm = st.checkbox("I am sure I want to delete this account")
        if st.button("Delete Account", type="primary", disabled=not confirm):
            Bank.delete(account["account_number"])
            do_logout()
            flash("Account deleted successfully.")
            st.rerun()


# ----------------------------- App Entry -----------------------------
def main():  # page setup
    st.set_page_config(page_title="Bank Management", page_icon="🏦")
    Bank.load()  # refresh data

    # session defaults
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "acc_no" not in st.session_state:
        st.session_state.acc_no = None

    st.title("🏦 Bank Management System")
    show_flash()  # pending message

    # route view
    if st.session_state.logged_in:
        dashboard()
    else:
        auth_screen()


main()  # run app