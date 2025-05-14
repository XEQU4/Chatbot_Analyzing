# Chatbot for Survey and Survey Analysis

![CI](https://github.com/XEQU4/BaseTelegramBot/actions/workflows/ci.yml/badge.svg)

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Aiogram](https://img.shields.io/badge/Aiogram-3.20.0+-green)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-blue)
![Tooling](https://img.shields.io/badge/Tool-uv-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📋 Description

This chatbot is designed for **collecting surveys and analyzing the results**.
It works closely with a second bot that handles **mass messaging**.
Recipients receive a message with a link to this chatbot, where they complete a survey.
The collected survey results are then **sent to managers** along with a **link to the respondent's profile**.

---

## 🛠️ Technologies Used

* Python 3.13
* Aiogram 3
* PostgreSQL
* Docker
* uv
* Ruff
* Pytest

---

## ⚙️ Functionality

* **Clients**:

  * After clicking the button at the bottom of the welcome message, clients go through the survey step-by-step.
* **Admins**:

  * Access to two buttons:

    * **Start Survey** — to manually go through the survey process
    * **Statistics** — to view bot activity statistics, database insights, and mailing analytics

---

## 📄 Environment Variables

A `.env.example` template is included for your convenience.
You can simply copy and configure it:

```bash
   cp .env.example .env
```

Example `.env` settings:

```dotenv
# Bot token
TOKEN="123456789:ABCdefGhIjkLmNoPqRsTuVwXyZ"

# MANAGERS=48461533212/84651231321/4563464
MANAGERS=123465478/

# Using the url connection to PostgreSQL Database
#DSN="postgres://postgres:pass@localhost:5432/postgres"  # For locally database
DSN="postgres://user:pass@postgres:5432/mydb"  # For docker
```

---

## 🚀 Installation and Launch

> ⚡ This project uses **uv** (fast package manager) and **Docker Compose** for database management.

### Option 1: Local Launch (via `uv`)

```bash
   pip install -U uv
   uv venv
   uv sync
   uv run bot.py
```

### Option 2: Docker Launch

```bash
   docker-compose up --build
```

---

## 🧪 Running Tests

If you want to run tests:

```bash
   uv run pytest
```

---

## 📷 UI Preview

### **Client Side:**

![Coming soon!](assets/cstart.png)
![Coming soon!](assets/cstart2.png)

### **Admin Side:**

![Coming soon!](assets/astart.png)
![Coming soon!](assets/astatistic.png)
![Coming soon!](assets/aclient.png)

### **Project Structure and Docker Build:**

![Coming soon!](assets/project_structure.png)
![Coming soon!](assets/docker.png)

---

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

---

**Author:** [XEQU](https://github.com/XEQU4)