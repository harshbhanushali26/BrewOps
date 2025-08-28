# ☕ BrewOps

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Repo Size](https://img.shields.io/github/repo-size/harshbhanushali26/BrewOps)](../../)
[![Issues](https://img.shields.io/github/issues/harshbhanushali26/BrewOps)](../../issues)
[![Last Commit](https://img.shields.io/github/last-commit/harshbhanushali26/BrewOps)](../../commits/main)

A modular **Python + Rich** based CLI system to manage café operations with menu, orders, and analytics — built for both customers and admins.

---

## 🚀 Features
* 🔑 **Admin Authentication** – Secure login system with username & password validation, hashing, and salting.
    - Username: 8–12 characters, must include **1 uppercase, 1 lowercase, and 1 number**.
    - Password: 8–12 characters, must include **1 uppercase, 1 lowercase, and 1 number**.
* 📋 **Menu & Category Management** – Add, update, remove, and filter items.
* 🛒 **Order Management** – Place, view, update, mark paid, filter orders.
* 📊 **Analytics & Dashboard** – Daily & monthly summaries, menu insights.
* 👤 **Customer CLI** – Browse menu, place/view orders.
* 🛠️ **Admin CLI** – Manage items, categories, orders, analytics, and authentication.

---

## 📂 Project Structure

```
BrewOps/
├── analytics/analyzer.py     # Daily/monthly summary & menu insights
├── auth/auth.py              # Core auth: register, login, hashing, salting 
├── cli/
|   ├── admin_auth_cli.py     # Admin auth: username & password input
│   ├── admin_cli.py          # Admin: items, categories, orders, analysis
│   ├── customer_cli.py       # Customer: browse, place, track orders
│   ├── items_category_cli.py # Item/category CRUD & filters
│   └── order_cli.py          # Order CRUD, status updates, filtering
├── menu/
│   ├── items.py              # Item core class (with from_dict & to_dict)
│   └── manager.py            # Item manager (CRUD + features)
├── orders/
│   ├── order.py              # Order core class
│   └── order_manager.py      # Order manager (CRUD + ops)
├── shared/
│   ├── managers.py           # Manager class imports
│   └── order_helper.py       # Helpers for placing orders (admin/customer)
├── utils/
│   ├── display.py            # UI functions (Rich-based)
│   ├── filtering.py          # Menu maps & filters
│   ├── json_io.py            # Save/load JSON files
│   └── validation.py         # Item & order validation
├── data/
│   ├── menu.json             # Café menu data
│   ├── orders.json           # Orders data
|   └── users.json            # Admin accounts (hashed & salted passwords)
|
├── main_menu.py              # Entry: admin & customer portal
└── main.py                   # Main entry point
                 
```

---

## ⚙️ Tech Stack

* **Python 3.10+** – Core programming language
* **Rich** – Beautiful CLI interface
* **JSON** – Lightweight storage  storage

---

## ▶️ Run the Project

```bash
git clone https://github.com/your-username/cafe-system.git
cd BrewOps
python main.py
```

---

## 📌 Roadmap

* [✅] Authentication system
* [ ] Session Management
* [ ] Export reports (CSV/PDF/JSON)
* [ ] Inventory management


---

## 🤝 Contribution

PRs are welcome! Fork the repo and submit improvements 🚀

## 📜 License

MIT License – feel free to use and modify.
