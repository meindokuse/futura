from pydantic import BaseModel


class EmailRequest(BaseModel):
    email: str


class VerifyEmailRequest(BaseModel):
    email: str
    code: str


class PasswordRequest(BaseModel):
    current_password: str
    new_password: str
