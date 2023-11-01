from pydantic import BaseModel


class Student(BaseModel):
    name: str
    ra: str
    email: str | None
    course: str | None
