from pydantic import (BaseModel,
                      constr,
                      model_validator)


class UserBase(BaseModel):
    login: constr(min_length=3, max_length=8, to_lower=True)


class UserCreate(UserBase):
    password: constr(min_length=5, max_length=15, to_lower=True)
    password2: str

    @model_validator(mode='after')
    def login_equals(self) -> 'UserCreate':
        if self.login == self.password:
            raise ValueError('login')
        return self

    @model_validator(mode='after')
    def passwords_equals(self) -> 'UserCreate':
        pw1 = self.password
        pw2 = self.password2
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError('password2')
        return self


class User(UserBase):
    id: int
    points: int

    class Config:
        from_attributes = True
