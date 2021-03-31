from pydantic import BaseModel, EmailStr, Field, validator


class UserRegisterDto(BaseModel):
    email: EmailStr
    password: str = Field(min_length=4, max_length=10)
    confirm_password: str

    @validator('confirm_password')
    def passwords_match(cls, confirm_password, values):  # noqa
        if 'password' in values and confirm_password != values['password']:
            raise ValueError('passwords do not match')
        return confirm_password


class UserLoginDto(BaseModel):
    email: EmailStr
    password: str = Field(min_length=4, max_length=10)
