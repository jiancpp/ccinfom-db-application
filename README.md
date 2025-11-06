# CCINFOM Database Application

This project is a **MySQL-based database application** that manages artists, fanclubs, events, tickets, and merchandise.  
It models the relationships between users, artists, and their fan activities, including purchases and memberships.

---

## 📁 Project Structure

| File | Description |
|------|--------------|
| **create_tables.sql** | Defines all database tables (without foreign keys). |
| **constraints.sql** | Adds foreign key constraints and relational rules. |
| **insert_data.sql** | *(Optional)* Contains sample data for testing. |
| **queries.sql** | *(Optional)* Example queries and reports. |


## ⚙️ Setup & Workflow for SQL Writing

### 1️⃣ Import or Update Files
Clone this repository to save locally and open on Visual Studio

### 2️⃣ Run on MySQL Workbench
Open SQL Scripts on MySQL Workbench and run 'create_tables.sql' to create the database locally.
You can edit the SQL scripts on both MySQL Workbench and Visual Studio simultaneously

### 3️⃣ Commit Changes to GitHub
Using the Visual Studio or your terminal, commit and push your changes to the SQL files once saved

---

## 🧩 Database Schema Overview

### **Core Tables**

| Table | Description |
|--------|--------------|
| `users` | Stores user accounts, emails, and registration dates. |
| `artists` | Contains artist names, debut dates, and fanclub counts. |
| `events` | Represents concerts, fanmeets, and related artist/fanclub events. |
| `merchandise` | Tracks event- and artist-specific items available for sale. |

### **Additional Tables**

| Table | Description |
|--------|--------------|
| `fanclubs` | Represents fan communities of artists. |
| `venues` | Stores venue names, locations, and capacities. |
| `seats` | Defines detailed seating layouts per venue. |
| `ticket_tier` | Holds ticket categories, prices, and quantities. |

### **Transaction Tables**

| Table | Description |
|--------|--------------|
| `ticket_sales` | Records user purchases of event tickets. |
| `merchandise_sales` | Logs user purchases of merchandise. |
| `fanclub_membership` | Tracks which users joined which fanclubs. |

---

That's a fantastic idea\! A **README file** is essential for any project, especially a school project, as it clearly documents the setup process for you and your collaborators.

Here is the complete **README.md** file based on the **Step-by-Step MySQL-Flask Integration Checklist**, designed to be placed in your project's root directory (`/jiancpp`).

-----

# 🚀 Project Setup: MySQL-Flask Integration Checklist

This document guides you through setting up and running the Flask application, ensuring proper connection to the local MySQL database used in SQL Workbench.

## Prerequisites

Before starting, ensure you have the following:

1.  **Python 3.x** installed.
2.  **MySQL Server** running locally (via SQL Workbench, XAMPP, etc.).
3.  **Visual Studio Code** (or your preferred editor).
4.  The project structure (including the `data/`, `model/`, `schema/`, and `view/` folders) is in place.

-----

## 🛠️ Phase 1: Environment and Dependencies Setup

This phase ensures all required software libraries are installed and your project workspace is clean.

### 1\. Create and Activate Virtual Environment

A virtual environment isolates project dependencies from your global Python installation.

1.  **Navigate to the project root** (`/jiancpp`) in your terminal.
2.  **Create the environment:**
    ```bash
    python -m venv .venv
    ```
3.  **Activate the environment:**
      * **Windows (Command Prompt/PowerShell):**
        ```bash
        .venv\Scripts\activate
        ```
      * **macOS/Linux (Bash/Zsh):**
        ```bash
        source .venv/bin/activate
        ```
    *(Your terminal prompt should now start with `(.venv)`).*

### 2\. Install Project Dependencies

1.  **Create `requirements.txt`** in the project root with the following content:
    ```
    Flask
    Flask-SQLAlchemy
    PyMySQL
    python-dotenv
    ```
2.  **Install packages:**
    ```bash
    pip install -r requirements.txt
    pip install flask mysql-connector-python
    ```

### 3\. Configure Git (Optional but Recommended)

1.  **Create `.gitignore`** in the project root.
2.  **Add exclusions** to prevent committing sensitive files and large environments:
    ```
    # Virtual Environment
    .venv/

    # Sensitive Credentials
    .env

    # Python Files
    __pycache__/
    *.pyc
    ```

-----

## 🔒 Phase 2: Secure Database Connection

This phase securely provides the Flask application with the necessary credentials to connect to your local MySQL server.

1.  **Create `config.py` File**
    Create a file named **`config.py`** in the app folder. **Do NOT commit this file to Git.**

2.  **Populate `app/config.py`**
    Replace the placeholder values with your actual MySQL credentials used by SQL Workbench:

    ```
    # ============================================
    #           DATABASE CONFIGURATION
    # ============================================
    
    DB_USER = "root"
    DB_PASS = "YourPassword"
    DB_NAME = "dbApp"
    ```

-----

## 💻 Phase 3: Run the Flask Application

Once the environment and credentials are set up, you can start the application.

1.  **Verify Model Mapping**

      * Check **`app/models.py`** to ensure your SQLAlchemy model classes (table definitions) accurately match the columns and names of the tables in your MySQL schema.

2. **(Database Related) Initialize Seats**

    *  Run create_tables.sql, constraints.sql in your workbench
    *  In your terminal, run the python code to populate seats:
        ```bash
        python populate_seats.py
        ```
    * (Optional) Run all sql files in data. Can be done while running application
      
3.  **Run the Application**

      * Ensure your **MySQL Server is running**.
      * In your activated `(.venv)` terminal, run the entry point script:
        ```bash
        python run.py
        ```

        or

        ```bash
        flask run
        ```

4.  **Access the Application**

      * The terminal will display the running address (e.g., `http://127.0.0.1:5000/`).
      * Open this address in your web browser. If successful, the page will display data fetched directly from your MySQL database.


    ```

-----

## Troubleshooting Common Errors

| Error Message | Cause | Solution |
| :--- | :--- | :--- |
| `WinError 2: The system cannot find the file specified` (during pip install) | Lack of permissions or incomplete environment creation. | **Run the installation process again from a terminal started with "Run as administrator."** |
| `Can't connect to MySQL server` | Flask cannot reach the database. | 1. Ensure your **MySQL server service is running**. 2. Double-check all values in the **`.env`** file (User, Password, Host, DB name) are correct. |
| `No module named 'flask'` | Environment not active. | Stop the script and run **`.venv\Scripts\activate`** (Windows) or **`source .venv/bin/activate`** (Mac/Linux) before trying to run `python run.py` again. |

-----

