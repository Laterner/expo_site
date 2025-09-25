# admin_view.py
import sqlite3

def view_contacts():
    conn = sqlite3.connect('contacts.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM contacts ORDER BY created_at DESC')
    contacts = cursor.fetchall()
    
    print(f"Всего контактов: {len(contacts)}")
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