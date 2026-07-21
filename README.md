
---

# 🏭 G-INOS – Global Integrated Neural Operating System

> **🌐 Language Notice:**
> While this README is provided in English for a broader overview, please note that the underlying project source code, database architecture (e.g., tables like `Materials_lager` or `prod_Maschinen`), business logic, and frontend HTML user interfaces are developed entirely in **German**.

G-INOS is a state-of-the-art, modular Enterprise Resource Planning (ERP) and Production Planning and Control (PPS) system. Built with **Python**, **Flask**, and **MySQL**, the system is specifically designed for the manufacturing industry (Hilde AG). It implements strict Role-Based Access Control (RBAC) to ensure maximum operational security and data integrity.

*(Note: Screenshots of the user interface can be found in the `/assets` directory.)*

---

## 🚀 Current Development Status & Core Features

The system is under active development and already covers the central operational pillars of a modern industrial plant:

### 1. 👥 Human Resources & Security Management (`Employers`)

* Secure user registration and encrypted login processes.
* Granular Role-Based Access Control (RBAC: Plant Manager, Production Manager, Shift Supervisor, Production Worker).

### 2. 📦 Inventory & Warehouse Management (`Materials_lager` / `Lagerbestand`)

* Real-time management of material inventory and warehouse locations.
* Automated warning system for low stock levels.
* Dynamic financial valuation of inventory (total value and broken down by location).
* Integrated Excel export functionality for administrative audits and reporting.

### 3. ⚙️ Production & Maintenance Management (`prod_Maschinen` & `Logbuch`)

* Live monitoring of machine status and centralized logging of machine failures.
* **Intelligent Maintenance Simulation:** Dynamic calculation of realistic repair times linked to system-defined failure priorities, automatically generating historical training data.

### 4. 📋 Customer Order Control Center (`Kunden_auftraege`)

* Operational creation and strategic management of customer orders.
* Automated assignment of Plant IDs based on the active user session to prevent cross-plant booking errors.

---

## 🤖 Feature Teaser: Branch `Aufträge_prediction_manager`

In the current development branch **`Aufträge_prediction_manager`**, we are driving the digital transformation of G-INOS toward Industry 4.0.

This branch lays the foundation for a true **Predictive Maintenance Module**:

* **Machine Learning in ERP:** Integration of a data science model utilizing **Pandas** and **Scikit-Learn**.
* **Linear Regression:** The system analyzes historical logbook entries and learns the mathematical correlation between failure priorities and actual downtime.
* **AI-Powered Forecasting Engine:** The trained model automatically calculates a precise estimate of the expected repair duration for future machine failures. This provides management with valuable decision-making data to drastically minimize factory downtime.

---

## 💻 Technology Stack

| Domain | Technologies |
| --- | --- |
| **Backend** | Python 3.x, Flask (Blueprints), MySQL Connector |
| **Database** | MySQL |
| **Frontend** | HTML5, CSS3 (Ergonomic, dual-pane control center layouts), Jinja2 Templating |
| **Data Science & ML** | Pandas, Scikit-Learn (Linear Regression) |
| **Security** | Flask-WTF (CSRF-Protection), PBKDF2 Password Hashing, Secure Session Management |
