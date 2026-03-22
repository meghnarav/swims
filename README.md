# 📦 SWIMS – Supplier Warehouse Inventory Management System

A full-stack inventory management system built with **React + FastAPI + MySQL (Docker)**, designed using **3NF normalization** for efficient and scalable data handling.

---

## Abstract

This application supports inventory operations for a warehouse-based organization that sources products from multiple suppliers and manages their storage across several warehouse locations. It is used to monitor product availability, track where items are stored, and record all stock movements that occur during routine warehouse operations. The system ensures that inventory quantities are consistently updated whenever goods are received into a warehouse or removed from it, reducing errors and improving visibility into current stock levels.

Warehouses can store a wide range of products, and the same product may be distributed across multiple warehouses based on storage capacity, demand, or operational needs. Inventory levels are maintained separately for each warehouse to ensure accurate, location-specific tracking. Employees are responsible for handling inventory activities such as receiving goods, updating stock quantities, and recording stock movements. Every stock movement is logged to ensure accountability and to allow tracing of inventory changes over time.

The application is strictly focused on inventory control and internal warehouse operations. It does not manage customer information, sales, order processing, or billing, and is intended solely to support efficient and transparent warehouse management.

---

## 🚀 Features

- 📊 Real-time inventory dashboard
- 📦 Product & supplier management
- 🏢 Warehouse stock tracking
- 🔁 Stock movement logging (INWARD / OUTWARD)
- 👨‍💼 Employee management (role-based)
- 📈 Charts for stock distribution & daily transactions
- 🧱 Fully normalized database (up to 3NF)

---

## 🧠 Database Design (3NF)

The database follows **Third Normal Form (3NF)**.

**Key improvements:**
- `Category` separated from `Product`
- `Role` separated from `Employee`
- No transitive dependencies
- All non-key attributes depend only on the primary key

**Tables:**

| Table | Description |
|---|---|
| `Supplier` | Stores details of product suppliers including contact information. |
| `Category` | Defines product categories to avoid repetition and ensure consistency. |
| `Product` | Contains product details and links each product to its supplier and category. |
| `Warehouse` | Stores information about warehouse locations and their storage capacity. |
| `Inventory` | Tracks the quantity of each product available in each warehouse. |
| `Role` | Defines different employee roles to eliminate redundancy in role names. |
| `Employee` | Stores employee details and links each employee to a role. |
| `Permanent_Employee` | Stores additional details specific to permanent employees like salary and benefits. |
| `Contract_Employee` | Stores details specific to contract employees like hourly rate and contract duration. |
| `Stock_Transaction` | Records all stock movements (inward/outward) with product, warehouse, and employee details. |

---

## 🛠️ Tech Stack

| Layer      | Technology                  |
|------------|-----------------------------|
| Frontend   | React (Vite) + Recharts     |
| Backend    | FastAPI (Python)             |
| Database   | MySQL (Dockerized)           |
| Other      | Docker, REST APIs            |

---

## 📂 Project Structure

```
inventory-management-system/
│
├── backend/
│   ├── api.py
│   ├── db_connection.py
│   ├── queries.py
│   └── __init__.py
│
├── db/
│   ├── schema.sql
│   └── seed_data.sql
│
├── ui/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── styles.css
│   ├── index.html
│   └── package.json
│
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Start MySQL (Docker)

```bash
docker start swims-mysql
```

If not yet created:

```bash
docker run -d \
  --name swims-mysql \
  -e MYSQL_ROOT_PASSWORD=rootpass \
  -e MYSQL_DATABASE=swims \
  -p 3306:3306 \
  mysql:latest
```

### 2️⃣ Load Database

```bash
docker cp db/schema.sql swims-mysql:/schema.sql
docker cp db/seed_data.sql swims-mysql:/seed_data.sql

docker exec -it swims-mysql mysql -u root -prootpass
```

Inside MySQL:

```sql
SOURCE /schema.sql;
SOURCE /seed_data.sql;
```

### 3️⃣ Backend Setup

```bash
cd backend
pip install -r ../requirements.txt
```

Run the backend:

```bash
python -m backend.api
```

API runs at: `http://127.0.0.1:8000`

### 4️⃣ Frontend Setup

```bash
cd ui
npm install
npm run dev
```

Frontend runs at: `http://localhost:5173`

---

## 🔗 API Endpoints

| Endpoint        | Description          |
|-----------------|----------------------|
| `/products`     | Get all products     |
| `/suppliers`    | Get suppliers        |
| `/inventory`    | Inventory data       |
| `/transactions` | Stock transactions   |
| `/employees`    | Employee list        |
| `/warehouses`   | Warehouse list       |

---

## 📊 Dashboard Includes

- Total Products
- Total Suppliers
- Total Stock Units
- Total Transactions
- Inventory by Warehouse *(Bar Chart)*
- Daily Movements *(Line Chart)*

---

## ⚠️ Common Issues & Fixes

**❌ Empty API response (`[]`)**
- ✔ Ensure DB is loaded using `SOURCE`
- ✔ Check backend DB connection (`rootpass`)

**❌ MySQL connection error**
- ✔ Confirm Docker container is running
- ✔ Use: `docker ps`

**❌ Module import error**  
Run backend using:
```bash
python -m backend.api
```

---

## 📌 Future Improvements

- Authentication system
- Role-based access control
- Low-stock alerts
- Advanced analytics
- Export reports

---

## 👩‍💻 Author

**Meghna Ravikumar**  
B.Tech CSE (AI & ML) – VIT Chennai

---

## ⭐ Final Note

This project demonstrates:
- Practical DBMS normalization (3NF)
- Full-stack integration
- Real-time data visualization
- Clean modular backend design
