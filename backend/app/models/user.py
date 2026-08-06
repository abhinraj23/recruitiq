from typing import Optional
from datetime import datetime

from sqlmodel import SQLModel,Field

class User(SQLModel,table=True):
    id:Optional[int]=Field(default=None,primary_key=True)
    name:str
    email:str=Field(index=True,unique=True)
    password_hash:str
    created_at:datetime=Field(default_factory=datetime.utcnow)

