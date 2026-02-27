# Student Management System

A desktop application built with **Python** and **PyQt6** for managing an educational institution's day-to-day operations — including students, teachers, classes, payments, finances, and attendance.

---

## Features

| Module | Description |
|---|---|
| 👨‍🎓 **Students** | Add, edit, and delete student records; track enrollment history |
| 👩‍🏫 **Teachers** | Manage teacher profiles and payment history |
| 🏫 **Classes** | Create and manage classes with pricing, sessions, and teacher assignments |
| 💳 **Payments** | Record student payments via cash, cheque, or bank transfer |
| 💰 **Finance** | Track all income (entries) and expenses (outgoing money); manage cash and bank accounts |
| 📅 **Attendance** | Log and review absence records for both students and teachers |
| 👤 **Users** | Role-based access control — grant or restrict access per module |
| ⚙️ **Settings** | Configure teaching modes, payment methods, entry codes, and other system parameters |
| 📄 **Reports** | Export data to Excel and generate print previews |

---

## Tech Stack

- **Language**: Python 3
- **GUI Framework**: [PyQt6](https://pypi.org/project/PyQt6/)
- **Database**: MySQL
- **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/)
- **Database Driver**: [PyMySQL](https://pypi.org/project/PyMySQL/)
- **UI Design**: Qt Designer (`.ui` files)

---

## Project Structure

```
student-management/
├── main.py                  # Application entry point (login screen)
├── app/
│   ├── database.py          # Database connection and engine setup
│   ├── models.py            # SQLAlchemy ORM models
│   ├── main_window.py       # Main application window
│   ├── students.py          # Student management logic
│   ├── classes.py           # Class management logic
│   ├── teacher.py           # Teacher management logic
│   ├── payment.py           # Payment processing logic
│   ├── money.py             # Financial management logic
│   ├── student_absent.py    # Student absence tracking
│   ├── teacher_absent.py    # Teacher absence tracking
│   ├── user.py              # User and role management
│   ├── settings.py          # Application settings
│   ├── help.py              # Shared helper/utility functions
│   └── devision.py          # UI layout helpers
├── tables_model/
│   ├── students_model.py    # Table model for student data
│   ├── classes_model.py     # Table model for class data
│   ├── teacher_model.py     # Table model for teacher data
│   ├── payment_model.py     # Table model for payment data
│   ├── money_tables.py      # Table models for financial data
│   └── abscent_models.py    # Table models for absence data
└── ui/                      # Qt Designer UI files (.ui)
    ├── login.ui
    ├── main.ui
    ├── students.ui
    ├── classes.ui
    └── ...                  # 30+ UI files for all screens
```

---

## Database Schema

The application uses a MySQL database with the following main tables:

| Table | Description |
|---|---|
| `users` | Application user accounts |
| `role` | Roles with per-module permissions |
| `students` | Student records |
| `students_history` | Student enrollment history |
| `teachers` | Teacher records |
| `teachershistory` | Teacher payment history |
| `classes` | Class definitions (price, sessions, teacher) |
| `classeleve` | Student ↔ class enrollment mapping |
| `entery` | Income transactions |
| `outmoney` | Expense transactions |
| `caisse` | Cash account ledger |
| `bank` | Bank account ledger |
| `absent_s` | Student absence records |
| `absent_t` | Teacher absence records |
| `settings` | System configuration values |

---

## Prerequisites

- Python 3.8+
- MySQL Server (local or network)

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yahiab05/student-management.git
   cd student-management
   ```

2. **Create and activate a virtual environment** *(recommended)*

   ```bash
   python -m venv env
   source env/bin/activate      # Linux / macOS
   env\Scripts\activate         # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install PyQt6 SQLAlchemy pymysql
   ```

4. **Configure the database connection**

   Open `app/database.py` and update the connection string with your MySQL credentials:

   ```python
   engine = create_engine("mysql+pymysql://<user>:<password>@<host>:<port>/<database>")
   ```

   Example:
   ```python
   engine = create_engine("mysql+pymysql://root:secret@localhost:3306/students_db")
   ```

   The application will create all required tables automatically on first run.

---

## Running the Application

```bash
python main.py
```

A login screen will appear. Enter your username and password to access the application.

---

## User Roles & Permissions

User access is controlled through roles. Each role can independently enable or disable access to the following modules:

- Classes
- Students
- Teachers
- Payments
- Finance
- Attendance
- Settings
- User Management
- Payment Editing

Roles and users are managed from within the application by an authorized administrator.

---

## License

This project is provided as-is for educational and personal use.
