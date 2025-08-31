from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Event Agency", version="1.0.0")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

class ContactRequest(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    message: str

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/contact")
async def contact_us(contact: ContactRequest):
    # Здесь можно добавить логику обработки формы (отправка email, сохранение в БД и т.д.)
    return {
        "status": "success",
        "message": "Ваше сообщение успешно отправлено! Мы свяжемся с вами в ближайшее время."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)