from pydantic import BaseModel


class Student(BaseModel):
    name: str
    ra: str
    email: str | None
    course: str | None


class UpdateStudent(BaseModel):
    name: str | None
    ra: str | None
    email: str | None
    course: str | None