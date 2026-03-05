from .db_connection import get_connection
import mysql.connector

def fetch_suppliers():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT Supplier_id, supplier_name, contact_email, phone_number FROM SUPPLIER")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    except: return []

def fetch_products():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.Product_id, p.Product_name, p.category, p.unit_price, s.supplier_name 
            FROM PRODUCT p
            JOIN SUPPLIER s ON p.supplier_id = s.Supplier_id
        """)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    except: return []

def fetch_inventory():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT i.Product_id, p.Product_name, i.warehouse_id, w.Location, i.quantity
            FROM INVENTORY i
            JOIN PRODUCT p ON i.Product_id = p.Product_id
            JOIN WAREHOUSE w ON i.warehouse_id = w.warehouse_id
        """)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    except: return []

def fetch_stock_transactions():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT st.transaction_id, st.Transaction_date, st.transaction_type, st.quantity,
                   p.Product_name, w.Location, e.name AS employee_name
            FROM STOCK_TRANSACTION st
            JOIN PRODUCT p ON st.product_id = p.Product_id
            JOIN WAREHOUSE w ON st.warehouse_id = w.warehouse_id
            JOIN EMPLOYEE e ON st.employee_id = e.Employee_id
            ORDER BY st.Transaction_date DESC
        """)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    except: return []

def fetch_warehouses():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT warehouse_id, Location, capacity FROM WAREHOUSE")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    except: return []

def fetch_employees():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT Employee_id, name, role FROM EMPLOYEE")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    except: return []

def add_stock_movement(prod_id, wh_id, emp_id, qty, t_type):
    if not all([prod_id, wh_id, emp_id, qty]): return False
    conn = get_connection()
    cursor = conn.cursor()
    try:
        conn.start_transaction()
        cursor.execute("""
            INSERT INTO STOCK_TRANSACTION 
            (Transaction_date, transaction_type, product_id, quantity, warehouse_id, employee_id)
            VALUES (NOW(), %s, %s, %s, %s, %s)
        """, (t_type, prod_id, qty, wh_id, emp_id))

        adj_qty = int(qty) if t_type == 'IN' else -int(qty)
        cursor.execute("""
            INSERT INTO INVENTORY (Product_id, warehouse_id, quantity)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE quantity = quantity + %s
        """, (prod_id, wh_id, adj_qty, adj_qty))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()