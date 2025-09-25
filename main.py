from fastapi import FastAPI, Request, Depends, HTTPException, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, EmailStr, validator
from dotenv import load_dotenv
from typing import Optional
import sqlite3
import datetime
import re, os
import secrets

app = FastAPI(title="Event Agency", version="1.0.0")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")
security = HTTPBasic()

# Загрузка переменных из .env файла
load_dotenv()

# Database setup
def get_db_connection():
    conn = sqlite3.connect('contacts.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ip_address TEXT
        )
    ''')
    conn.commit()
    conn.close()

def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, os.getenv('ADMIN_USERNAME'))
    correct_password = secrets.compare_digest(credentials.password, os.getenv('ADMIN_PASSWORD'))
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=401,
            detail="Неверные учетные данные",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()

class ContactRequest(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    message: str

    @validator('name')
    def validate_name(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('Имя должно содержать минимум 2 символа')
        if len(v) > 100:
            raise ValueError('Имя слишком длинное')
        # Проверка на допустимые символы
        if not re.match(r'^[a-zA-Zа-яА-ЯёЁ\s\-]+$', v):
            raise ValueError('Имя содержит недопустимые символы')
        return v.strip()

    @validator('phone')
    def validate_phone(cls, v):
        if v is None:
            return v
        # Очистка номера от лишних символов
        cleaned_phone = re.sub(r'[^\d+]', '', v)
        if len(cleaned_phone) < 10:
            raise ValueError('Номер телефона слишком короткий')
        if len(cleaned_phone) > 20:
            raise ValueError('Номер телефона слишком длинный')
        return cleaned_phone

    @validator('message')
    def validate_message(cls, v):
        if len(v.strip()) < 10:
            raise ValueError('Сообщение должно содержать минимум 10 символов')
        if len(v) > 1000:
            raise ValueError('Сообщение слишком длинное')
        return v.strip()

def get_client_ip(request: Request):
    if "x-forwarded-for" in request.headers:
        return request.headers["x-forwarded-for"].split(",")[0]
    return request.client.host

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/contact")
async def contact_us(contact: ContactRequest, request: Request):
    try:
        client_ip = get_client_ip(request)
        
        # Подключение к базе данных
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Безопасная вставка с параметризованным запросом
        cursor.execute('''
            INSERT INTO contacts (name, email, phone, message, ip_address, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            contact.name,
            contact.email,
            contact.phone,
            contact.message,
            client_ip,
            datetime.datetime.now()
        ))
        
        conn.commit()
        contact_id = cursor.lastrowid
        conn.close()
        
        # Логирование успешной отправки (в продакшене лучше использовать logging)
        print(f"Новый контакт сохранен: ID {contact_id}, Email: {contact.email}, IP: {client_ip}")
        
        return JSONResponse({
            "status": "success",
            "message": "Ваше сообщение успешно отправлено! Мы свяжемся с вами в ближайшее время.",
            "contact_id": contact_id
        })
        
    except sqlite3.Error as e:
        # Логирование ошибки базы данных
        print(f"Ошибка базы данных: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Произошла ошибка при сохранении данных. Пожалуйста, попробуйте позже."
        )
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Произошла непредвиденная ошибка. Пожалуйста, попробуйте позже."
        )

# Страница администрирования
@app.get("/admin")
async def admin_login(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request})


@app.get("/admin/contacts")
async def view_contacts(
    request: Request,
    username: str = Depends(authenticate_user),
    page: int = 1,
    search: str = None
):
    limit = 20
    offset = (page - 1) * limit
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Формируем запрос в зависимости от поиска
    if search:
        cursor.execute('''
            SELECT COUNT(*) FROM contacts 
            WHERE name LIKE ? OR email LIKE ? OR phone LIKE ?
        ''', (f'%{search}%', f'%{search}%', f'%{search}%'))
        
        cursor.execute('''
            SELECT * FROM contacts 
            WHERE name LIKE ? OR email LIKE ? OR phone LIKE ?
            ORDER BY created_at DESC 
            LIMIT ? OFFSET ?
        ''', (f'%{search}%', f'%{search}%', f'%{search}%', limit, offset))
    else:
        cursor.execute('SELECT COUNT(*) FROM contacts')
        cursor.execute('''
            SELECT * FROM contacts 
            ORDER BY created_at DESC 
            LIMIT ? OFFSET ?
        ''', (limit, offset))
    
    total_count = cursor.fetchone()[0]
    contacts = cursor.fetchall()
    
    conn.close()
    
    total_pages = (total_count + limit - 1) // limit
    
    return templates.TemplateResponse("admin_contacts.html", {
        "request": request,
        "contacts": contacts,
        "page": page,
        "total_pages": total_pages,
        "search": search or "",
        "total_count": total_count
    })

@app.delete("/admin/contacts/{contact_id}")
async def delete_contact(contact_id: int):
    """
    Endpoint для удаления контакта (в реальном приложении нужно добавить аутентификацию)
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Проверяем существование контакта
        cursor.execute('SELECT id FROM contacts WHERE id = ?', (contact_id,))
        contact = cursor.fetchone()
        
        if not contact:
            raise HTTPException(status_code=404, detail="Контакт не найден")
        
        # Безопасное удаление
        cursor.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))
        conn.commit()
        conn.close()
        
        return {"status": "success", "message": "Контакт удален"}
        
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail="Ошибка базы данных")

if __name__ == "__main__":
    import uvicorn
    HOST_NAME = os.getenv('HOST_NAME')
    HOST_PORT = os.getenv('HOST_PORT')
    uvicorn.run(app, host=HOST_NAME, port=HOST_PORT)