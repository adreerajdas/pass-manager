import mysql.connector

try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="2405",
        database="adreepass"
    )

    cursor = db.cursor()
    cursor.execute("SELECT DATABASE();")
    database_name = cursor.fetchone()[0]

    print(f"✅ Connected to MySQL database: {database_name}")

    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()
    print("📌 Tables in the database:")
    for table in tables:
        print(f" - {table[0]}")

    db.close()
except mysql.connector.Error as err:
    print(f"❌ Error: {err}")
