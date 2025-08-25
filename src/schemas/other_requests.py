from pydantic import BaseModel


class EmailRequest(BaseModel):
    email: str


class VerifyEmailRequest(BaseModel):
    email: str
    code: str


class PasswordRequest(BaseModel):
    current_password: str
    new_password: str


class ResetPasswordRequest(BaseModel):
    email: str


class NewPasswordRequest(BaseModel):
    token: str
    new_password: str


class DeleteRequest(BaseModel):
    id: int
    name_object: str
