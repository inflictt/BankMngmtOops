# 🏦 BankMngmtOops — Bank Management System

A complete **bank management system** written in Python to practice core **Object-Oriented Programming (OOP)** concepts. It comes in two forms: an original **command-line version** and an interactive **Streamlit web app** with a clean dashboard, login flow, and persistent storage.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Status](https://img.shields.io/badge/status-active-success)
![License](https://img.shields.io/badge/license-MIT-blue)

> 🔗 **Live demo:** _add your `https://<your-subdomain>.streamlit.app` link here once deployed_

---

## ✨ Features

- 🆕 **Create account** — open a new account with name, age, email, and PIN validation
- 🔐 **Secure login** — authenticate with account number + PIN
- 💰 **Deposit** — add money to your balance
- 🏧 **Withdraw** — take money out, with insufficient-balance checks
- 📋 **View details** — see all your account information at a glance
- ✏️ **Update details** — change your name, email, PIN, or age
- 🗑️ **Delete account** — remove your account with a confirmation step
- 💾 **Persistent storage** — all data is saved to a JSON file
- 🧭 **Session-based auth** — log in once and stay logged in while you use the app

---

## 🛠️ Tech Stack

- **Python 3.9+**
- **Streamlit** — for the interactive web UI
- **JSON** — lightweight file-based storage

---

## 📂 Project Structure

```
BankMngmtOops/
├── app.py            # Streamlit web app  ← run this one
├── main.py           # Original command-line (CLI) version
├── requirements.txt  # Python dependencies
├── .gitignore        # Keeps data.json and cache files out of Git
└── data.json         # Local account data (auto-created, not committed)
```

---

## 🚀 Getting Started (Run Locally)

**Prerequisites:** Python 3.9 or newer installed on your machine.

```bash
# 1. Clone the repository
git clone https://github.com/inflictt/BankMngmtOops.git
cd BankMngmtOops

# 2. (Optional) create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # On Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch the web app
streamlit run app.py
```

The app will open automatically at **http://localhost:8501**.

Prefer the terminal version? Run the original CLI app instead:

```bash
python main.py
```

---

## ☁️ Deployment

This app is built to run on **Streamlit Community Cloud** (free hosting).

To deploy your own copy:

1. Push the project to GitHub.
2. Go to **[share.streamlit.io](https://share.streamlit.io)** and sign in with GitHub.
3. Click **Create app**, then set:
   - **Repository:** `inflictt/BankMngmtOops`
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. Click **Deploy** — your app goes live in a couple of minutes.

Every `git push` after that updates the live app automatically.

---

## 🧠 OOP Concepts Demonstrated

This project is a hands-on demonstration of Object-Oriented Programming in Python:

- **Encapsulation** — all banking logic and data live inside a single `Bank` class.
- **Private methods (name mangling)** — internal helpers like `__update()` and `__accountNumGenerate()` are hidden from outside access using the `__` prefix.
- **`@staticmethod`** — used for the file-writing helper that doesn't need instance or class data.
- **`@classmethod`** — used for methods that read and modify shared class-level data.
- **Class-level vs. instance data** — the account list is stored on the class and shared across the app.
- **Separation of concerns** — the business logic (`Bank` class) is kept completely separate from the UI layer.

---

## 📖 How to Use

1. Open the app and go to the **Create Account** tab. Fill in your details and **save the account number it gives you** — you'll need it to log in.
2. Switch to the **Login** tab and enter your account number and PIN.
3. Use the **sidebar menu** to Deposit, Withdraw, view Details, Update info, or Delete your account.

---

## ⚠️ Notes & Limitations

- **This is a learning project, not a real banking system.** PINs are stored in plain text — never enter a real PIN.
- **Data is not permanent on the cloud.** Streamlit Community Cloud uses temporary storage, so accounts created on the live version reset whenever the app restarts or sleeps. For permanent storage, a real database would be needed.

---

## 🔮 Possible Improvements

- Swap the JSON file for a real database (SQLite, PostgreSQL, or Supabase)
- Hash PINs instead of storing them as plain text
- Add a transaction history / statement view
- Stronger email and input validation

---

## 👤 Author

**inflictt** · [GitHub Profile](https://github.com/inflictt)

---

## 📝 License

Released under the **MIT License** — free to use, modify, and learn from. Add a `LICENSE` file to your repo to make it official on GitHub.