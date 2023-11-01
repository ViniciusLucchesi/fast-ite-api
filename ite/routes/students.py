from fastapi import APIRouter
from fastapi.responses import JSONResponse

from ite.config.database import mongo
from ite.schemas.students import student_list_schema, student_schema
from ite.models.student import Student


router = APIRouter()


@router.get("/list")
async def students_list():
    """Return a list of students."""
    students = []
    try:
        all_students = await mongo.students.find().to_list(None)
        students = student_list_schema(all_students)
    except Exception as error:
        return JSONResponse(content={"error": str(error)}, status_code=500)
    
    if len(students) == 0:
        return JSONResponse(content={"msg": "There is no Students in the database"}, status_code=200)
    
    return JSONResponse(content=students, status_code=200)


@router.get("/detail/{student_ra}")
async def student_detail(student_ra: str):
    """Return a student detail based on its RA."""
    student = None
    try:
        student = await mongo.students.find_one({"ra": student_ra})
    except Exception as error:
        return JSONResponse(content={"error": str(error)}, status_code=500)
    
    if student is None:
        return JSONResponse(content={"msg": "Student not found"}, status_code=404)
    data = Student(**student).model_dump()
    return JSONResponse(content=data, status_code=200)


@router.post('/create')
async def student_create(student: Student):
    """Create a new student."""
    student = student.model_dump()
    try:
        await mongo.students.insert_one(student)
    except Exception as error:
        return JSONResponse(content={"error": str(error)}, status_code=500)
    
    return JSONResponse(content={"msg": "Student created successfully"}, status_code=201)


@router.put('/update/{student_ra}')
async def student_update(student_ra: str, student: Student):
    """Update a student based on its RA."""
    try:
        student = dict(student)

        if student["email"] is None:
            del student["email"]
        if student["course"] is None:
            del student["course"]

        await mongo.students.find_one_and_update(
            {"ra": student_ra},
            {"$set": student}
        )
    except Exception as error:
        return JSONResponse(content={"error": str(error)}, status_code=500)
    
    return JSONResponse(content={"msg": "Student updated successfully"}, status_code=200)


@router.delete('/delete/{student_ra}')
async def student_delete(student_ra: str):
    """Delete a student based on its RA."""
    try:
        await mongo.students.find_one_and_delete({"ra": student_ra})
    except Exception as error:
        return JSONResponse(content={"error": str(error)}, status_code=500)
    
    return JSONResponse(content={"msg": "Student deleted successfully"}, status_code=200)