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


class UserChangePwdDto(BaseModel):
    old_password: str = Field(min_length=4, max_length=10)
    new_password: str = Field(min_length=4, max_length=10)
    confirm_new_password: str = Field(min_length=4, max_length=10)

    @validator('new_password')
    def new_password_cannot_be_the_same_as_old(cls, new_password, values):  # noqa
        if 'old_password' in values and new_password == values['old_password']:
            raise ValueError('New password cannot be the same as an old.')
        return new_password

    @validator('confirm_new_password')
    def passwords_match(cls, confirm_new_password, values):  # noqa
        if 'new_password' in values and confirm_new_password != values['new_password']:
            raise ValueError('Passwords do not match: new_password and confirm_new_password must match.')
        return confirm_new_password
