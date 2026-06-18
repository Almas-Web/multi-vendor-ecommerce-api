# 🛒 Multi Vendor E-Commerce API (FastAPI)

A production-ready Multi Vendor E-Commerce Backend API built with FastAPI, PostgreSQL, SQLAlchemy, and JWT Authentication.

---

## 🚀 Project Overview

| Section          | Details                     |
| ---------------- | --------------------------- |
| Project Name     | Multi Vendor E-Commerce API |
| Type             | Backend REST API            |
| Framework        | FastAPI                     |
| Database         | PostgreSQL                  |
| ORM              | SQLAlchemy                  |
| Authentication   | JWT                         |
| Validation       | Pydantic                    |
| Migration        | Alembic                     |
| Containerization | Docker & Docker Compose     |

---

## 🚀 Features

### 🔐 Authentication & Authorization

* User Registration
* User Login
* JWT Authentication
* Role-Based Access Control (Admin / Vendor / User)

### 👤 User Management

* User Profile
* Current User Endpoint
* User Role Management

### 🛍️ Product Management

* Create Product
* Update Product
* Delete Product
* Product Listing
* Product Stock Management
* Active / Inactive Product Support

### 🛒 Cart System

* Add Items to Cart
* Update Cart Quantity
* Remove Cart Items
* Stock Validation

### 🧾 Checkout System

* Convert Cart into Order
* Automatic Stock Deduction
* Order Generation

### 📦 Order Management

* Order Creation
* Order Details
* Order Status Update
* Order Item Management

### 💳 Payment System

* Payment Creation
* Transaction ID Support
* Admin Payment Confirmation
* Payment Status Tracking

### 🏠 Address Management

* Multiple Addresses
* Default Address Support
* CRUD Operations

### 📧 Email Notification System

* Welcome Email on Registration
* HTML Email Templates
* SMTP Email Support
* Reusable Email Manager

### 🐳 Docker Support

* Docker Configuration
* Docker Compose Setup
* Environment Variable Support
* Easy Deployment

---

## 🏗️ Tech Stack

| Layer            | Technology |
| ---------------- | ---------- |
| Backend          | FastAPI    |
| Database         | PostgreSQL |
| ORM              | SQLAlchemy |
| Authentication   | JWT        |
| Validation       | Pydantic   |
| Migration        | Alembic    |
| Email            | SMTP       |
| Containerization | Docker     |

---

## 📁 Project Structure

```text
multi_vendor_ecommerce_api/
│
├── alembic/
├── apis/
├── core/
├── db/
├── repositories/
├── schemas/
├── templates/
├── uploads/
├── utils/
│   └── email_manager/
├── .env.example
├── docker-compose.yml
├── requirements.txt
└── main.py
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/your-username/multi-vendor-ecommerce-api.git
cd multi-vendor-ecommerce-api
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux / Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Setup Environment Variables

Copy:

```bash
cp .env.example .env
```

Update values inside `.env`.

### Run Database Migration

```bash
alembic upgrade head
```

### Run Application

```bash
uvicorn main:app --reload
```

---

## 🐳 Docker Setup

Build and Run:

```bash
docker-compose up --build
```

Run in Background:

```bash
docker-compose up -d
```

Stop Containers:

```bash
docker-compose down
```

---

## 🔑 Environment Variables

```env
DATABASE_URL=
SECRET_KEY=
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_FROM=
MAIL_PORT=
MAIL_SERVER=
MAIL_STARTTLS=True
MAIL_SSL_TLS=False
```

---

## 📌 Main API Modules

| Module    | Endpoint    |
| --------- | ----------- |
| Auth      | /auth       |
| Users     | /users      |
| Products  | /products   |
| Cart      | /cart-items |
| Checkout  | /checkout   |
| Orders    | /orders     |
| Payments  | /payments   |
| Addresses | /addresses  |

---

## 🧠 Future Improvements

* Payment Gateway Integration (SSLCommerz / Stripe)
* Order Tracking System
* Redis Cache
* CI/CD Pipeline
* Background Task Processing (Celery)

---

## 👨‍💻 Author

**Almas Hossen**

Backend Developer (FastAPI)

---

## ⭐ Project Status

Actively maintained and continuously improved.

This project is being developed to demonstrate real-world backend development skills using FastAPI and PostgreSQL.
