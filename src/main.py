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

app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["https://frontend.example.com"],  # Разрешить запросы с этого домена
#     allow_credentials=True,  # Разрешить отправку cookies или заголовков авторизации
#     allow_methods=["GET", "POST"],  # Разрешить только эти методы
#     allow_headers=["Authorization", "Content-Type"],  # Разрешить только эти заголовки
# )


# app.add_middleware(TokenValidationMiddleware)
# app.add_middleware(AdminRoleMiddleware)

app.include_router(auth_router)
app.include_router(employer_router)
app.include_router(workday_router)