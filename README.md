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

### ** Import or Update Files
Clone this repository to save locally and open on Visual Studio

### ** Run on MySQL Workbench
Open SQL Scripts on MySQL Workbench and run 'create_tables.sql' to create the database locally
You can edit the SQL scripts on both MySQL Workbench and Visual Studio simultaneously

### ** Commit Changes to GitHub
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


