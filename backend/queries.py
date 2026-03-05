from .db_connection import get_connection

def fetch_suppliers():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Supplier")
    data = cursor.fetchall()
    conn.close()
    return data



def fetch_products():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Product")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def fetch_inventory():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT i.product_id, p.product_name, i.warehouse_id, w.location, i.quantity
        FROM Inventory i
        JOIN Product p ON i.product_id = p.product_id
        JOIN Warehouse w ON i.warehouse_id = w.warehouse_id
    """)
    data = cursor.fetchall()
    conn.close()
    return data

def fetch_stock_transactions():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT st.transaction_id, st.transaction_date, st.transaction_type, st.quantity,
               p.product_name, w.location, e.name AS employee_name
        FROM Stock_Transaction st
        JOIN Product p ON st.product_id = p.product_id
        JOIN Warehouse w ON st.warehouse_id = w.warehouse_id
        JOIN Employee e ON st.employee_id = e.employee_id
    """)
    data = cursor.fetchall()
    conn.close()
    return data