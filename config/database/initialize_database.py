# initialize_database.py
import sqlite3

def create_server_ips_table():
    # Connect to or create the data.db file
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Create the server_ips table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS server_ips (
            id INTEGER PRIMARY KEY,
            ip_address TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_server_ips_table()
