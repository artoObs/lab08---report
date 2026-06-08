import os
import mysql.connector

class ItemModel:
    def __init__(self):
        self.config = {
            'host': os.getenv('DB_HOST'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASS'),
            'database': os.getenv('DB_NAME'),
            'charset': 'utf8mb4',
            'use_unicode': True,
            'collation': 'utf8mb4_unicode_ci'
        }

    def get_all_items(self):
        try:
            conn = mysql.connector.connect(**self.config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT name FROM items')
            items = cursor.fetchall()
            for item in items:
                if isinstance(item['name'], bytes):
                    item['name'] = item['name'].decode('utf-8')
                elif isinstance(item['name'], str):
                    try:
                        item['name'] = item['name'].encode('latin1').decode('utf-8')
                    except:
                        pass
            cursor.close()
            conn.close()
            return items
        except Exception as e:
            print(f"Error: {e}")
            return []
