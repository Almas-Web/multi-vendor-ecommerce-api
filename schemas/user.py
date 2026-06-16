from email_validator import validate_email, EmailNotValidError
from pydantic import BaseModel, Field, EmailStr
from fastapi import HTTPException, status


#  USER CREATE 
class UserCreate(BaseModel):
    email: str
    password: str = Field(..., min_length=4)

    def __init__(self, **data):
        super().__init__(**data)

        if self.email:
            try:
                emailinfo = validate_email(self.email, check_deliverability=False)
                self.email = emailinfo.normalized

            except EmailNotValidError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Not a valid email!"
                )


#  USER RESPONSE MODEL
class UserView(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    is_superuser: bool
    is_vendor: bool

    class Config:
        from_attributes = True



#  TOKEN RESPONSE

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    
# ROLE UPDATE SCHEMA
class UserRoleUpdate(BaseModel):
    is_vendor: bool = False
    is_superuser: bool = False