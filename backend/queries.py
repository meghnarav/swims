from .db_connection import get_connection
import mysql.connector

# ======================
# READ OPERATIONS (FETCH)
# ======================

def fetch_suppliers():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Supplier")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def fetch_products():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    # Joining with Supplier to show where the product comes from
    cursor.execute("""
        SELECT p.product_id, p.product_name, p.category, s.supplier_name 
        FROM Product p
        JOIN Supplier s ON p.supplier_id = s.supplier_id
    """)
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
    cursor.close()
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
        ORDER BY st.transaction_date DESC
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def fetch_warehouses():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT warehouse_id, location FROM Warehouse")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

# ======================
# WRITE OPERATIONS (CRUD)
# ======================

def add_stock_transaction(product_id, warehouse_id, employee_id, quantity, transaction_type):
    """
    Handles a stock movement. 
    1. Records the transaction in Stock_Transaction.
    2. Updates or Inserts the quantity in the Inventory table.
    Uses a Database Transaction to ensure data integrity.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Start Transaction
        conn.start_transaction()

        # 1. Insert the log entry
        insert_query = """
            INSERT INTO Stock_Transaction (product_id, warehouse_id, employee_id, quantity, transaction_type, transaction_date)
            VALUES (%s, %s, %s, %s, %s, NOW())
        """
        cursor.execute(insert_query, (product_id, warehouse_id, employee_id, quantity, transaction_type))

        # 2. Update Inventory
        # We use 'ON DUPLICATE KEY UPDATE' to handle the case where the product/warehouse 
        # combo doesn't exist yet in the Inventory table.
        
        # Determine multiplier (positive for receiving, negative for removal)
        adj_quantity = int(quantity) if transaction_type.upper() == 'IN' else -int(quantity)

        update_inventory_query = """
            INSERT INTO Inventory (product_id, warehouse_id, quantity)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE quantity = quantity + %s
        """
        cursor.execute(update_inventory_query, (product_id, warehouse_id, adj_quantity, adj_quantity))

        # Commit changes
        conn.commit()
        return {"status": "success", "message": "Transaction recorded successfully"}

    except mysql.connector.Error as err:
        conn.rollback()
        print(f"Error: {err}")
        return {"status": "error", "message": str(err)}
    
    finally:
        cursor.close()
        conn.close()

def add_new_product(name, category, supplier_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = "INSERT INTO Product (product_name, category, supplier_id) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, category, supplier_id))
        conn.commit()
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        cursor.close()
        conn.close()