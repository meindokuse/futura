from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.middlewares.token_validator import TokenValidationMiddleware
from src.middlewares.admin_cheker import AdminRoleMiddleware
from src.api.users import router as auth_router

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