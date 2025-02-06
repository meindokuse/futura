from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from markdown_it.rules_inline import image

from src.api.residents import router
from src.middlewares.token_validator import TokenValidationMiddleware
from src.middlewares.admin_cheker import AdminRoleMiddleware
from src.api.auth import router as auth_router
from src.api.employers import router as employer_router
from src.api.workday import router as workday_router
from src.api.events import router as event_router
from src.api.product import router as product_router
from src.api.residents import router as residents_router
from src.api.locations import router as location_router
from src.api.files import router as files_router


app = FastAPI()



# app.add_middleware(TokenValidationMiddleware)
# app.add_middleware(AdminRoleMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить все источники (замените на конкретный домен для безопасности)
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы
    allow_headers=["*"],  # Разрешить все заголовки
)
app.include_router(auth_router)
app.include_router(employer_router)
app.include_router(workday_router)

app.include_router(event_router)
app.include_router(product_router)
app.include_router(residents_router)

app.include_router(location_router)

app.include_router(files_router)

@app.get("/favicon.ico")
async def favicon():
    return {}