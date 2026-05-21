# 🛒 Multi Vendor E-Commerce API (FastAPI)

| Section | Details |
|--------|---------|
| 🚀 Project Name | Multi Vendor E-Commerce API |
| 🧠 Type | Backend REST API |
| ⚙️ Framework | FastAPI |
| 🗄️ Database | PostgreSQL |
| 🔐 Auth | JWT Authentication |
| 🧩 ORM | SQLAlchemy |
| 📦 Migration | Alembic |

---

## 🚀 Features

| Module | Features |
|--------|----------|
| 🔐 Authentication | JWT login, register, role-based access (admin/vendor/user) |
| 👤 User System | User profile & current user |
| 🛍️ Product System | CRUD, stock management, active/inactive products |
| 🛒 Cart System | Add / update / delete cart items, stock validation |
| 🧾 Checkout System | Cart → Order conversion with stock deduction |
| 📦 Order System | Order creation, status tracking, order items |
| 💳 Payment System | Payment creation, transaction ID, admin confirmation |
| 🏠 Address System | Multiple addresses, default address support |

---

## 🏗️ Tech Stack

| Layer | Technology |
|------|------------|
| Backend | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Migration | Alembic |
| Authentication | JWT |
| Validation | Pydantic |

---

## 📁 Project Structure

| Folder | Purpose |
|--------|--------|
| db/ | Database models |
| repositories/ | Business logic |
| apis/ | API routes |
| schemas/ | Pydantic schemas |
| utils/ | Helper functions |
| alembic/ | Database migrations |

---

## ⚙️ Installation

| Step | Command |
|------|--------|
| 1️⃣ Clone Repo | ```bash git clone https://github.com/your-username/multi-vendor-ecommerce-api.git ``` |
| 2️⃣ Go to Project | ```bash cd multi-vendor-ecommerce-api ``` |
| 3️⃣ Create Virtual Environment | ```bash python -m venv venv ``` |
| 4️⃣ Activate (Windows) | ```bash venv\Scripts\activate ``` |
| 5️⃣ Install Dependencies | ```bash pip install -r requirements.txt ``` |
| 6️⃣ Setup Environment | Create `.env` file: <br> ```env DATABASE_URL=postgresql://user:password@localhost/dbname SECRET_KEY=your_secret_key ALGORITHM=HS256 ACCESS_TOKEN_EXPIRE_MINUTES=60 ``` |
| 7️⃣ Run Migrations | ```bash alembic upgrade head ``` |
| 8️⃣ Start Server | ```bash uvicorn main:app --reload ``` |

---

## 🔑 Environment Variables

| Variable | Value |
|----------|-------|
| DATABASE_URL | postgresql://user:password@localhost/db |
| SECRET_KEY | your_secret_key |
| ALGORITHM | HS256 |
| ACCESS_TOKEN_EXPIRE_MINUTES | 60 |

---

## 📌 API Endpoints

| Module | Endpoints |
|--------|----------|
| Auth | `/auth/register`, `/auth/login` |
| Products | `/products` |
| Cart | `/cart-items` |
| Checkout | `/checkout` |
| Orders | `/orders`, `/orders/{id}/status` |
| Payments | `/payments`, `/payments/{id}/success` |
| Address | `/addresses` |

---

## 🧠 Future Improvements

| Feature | Status |
|--------|--------|
| Payment Gateway (SSLCommerz/Stripe) | Planned |
| Order Tracking System | Planned |
| Email Notification System | Planned |
| Redis Cache | Planned |
| Docker Deployment | Planned |
| CI/CD Pipeline | Planned |

---

## 👨‍💻 Author

| Name | Role |
|------|------|
| Almas Hossen | Backend Developer (FastAPI) |

---

## ⭐ Note

| Info | Description |
|------|-------------|
| Project Type | Learning + Production-ready backend |
| Status | Actively improving step-by-step |