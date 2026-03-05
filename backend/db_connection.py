import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="swims_user",
        password="swims_pass",
        database="swims"
    )