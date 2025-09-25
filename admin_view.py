# admin_view.py
import sqlite3

def view_contacts():
    conn = sqlite3.connect('contacts.db')
    cursor = conn.cursor()
    
    page = 1
    limit = 20
    offset = (page - 1) * limit
    search = "shvedskiy@maction.ru2"
    
    
    if search:
        like = f"%{search}%"

        # Считаем количество
        cursor.execute('''
            SELECT COUNT(*) FROM contacts 
            WHERE name LIKE ? OR email LIKE ? OR phone LIKE ?
        ''', (like, like, like))
        total_count = cursor.fetchone()[0]

        # Получаем записи
        cursor.execute('''
            SELECT * FROM contacts 
            WHERE name LIKE ? OR email LIKE ? OR phone LIKE ?
            ORDER BY created_at DESC 
            LIMIT ? OFFSET ?
        ''', (like, like, like, limit, offset))
        contacts = cursor.fetchall()

    else:
        # Считаем количество
        cursor.execute('SELECT COUNT(*) FROM contacts')
        total_count = cursor.fetchone()[0]

        # Получаем записи
        cursor.execute('''
            SELECT * FROM contacts 
            ORDER BY created_at DESC 
            LIMIT ? OFFSET ?
        ''', (limit, offset))
        contacts = cursor.fetchall()
    
    print(f"Всего контактов: {total_count}")
    print("-" * 80)
    
    for contact in contacts:
        print(f"ID: {contact[0]}")
        print(f"Имя: {contact[1]}")
        print(f"Email: {contact[2]}")
        print(f"Телефон: {contact[3]}")
        print(f"Сообщение: {contact[4][:100]}...")
        print(f"Дата: {contact[5]}")
        print(f"IP: {contact[6]}")
        print("-" * 80)
    
    conn.close()

if __name__ == "__main__":
    view_contacts()