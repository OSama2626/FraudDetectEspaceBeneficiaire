# backend/app/schemas/user.py
import pydantic
from typing import Optional

class UserSync(pydantic.BaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    imageUrl: Optional[str] = None
    email: Optional[str] = None