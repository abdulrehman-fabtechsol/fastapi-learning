from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field, field_validator
import asyncio
from typing import Optional


app = FastAPI()




# students = {}


# @app.get("/all-students")
# async def say_hello():
#     await asyncio.sleep(1)  # Simulating async work
#     print("Hello")
#     return {"message": "Hello", "students": students}


# @app.get("/get-student/{student_id}")
# async def get_student(student_id: int):
#     if student_id <= 10:
#         return {"error": "student_id must be greater than 10"}
#     await asyncio.sleep(1)
#     return students[student_id]



# @app.get("/get-student-params")
# async def get_student(*,student_id: Optional[int] = None,name: Optional[str] = None):
#     try:
#         print(name)
#         if student_id is None:
#             return {"students": students}
#         if student_id <= 10:
#             raise ValueError("student_id must be greater than 10")
#         await asyncio.sleep(1)
#         return students[student_id]
#     except KeyError:
#         raise HTTPException(status_code=404, detail="Student not found")
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))

# class Student(BaseModel):
#     name: str = Field(..., min_length=2, max_length=50)  # Required, 2-50 chars
#     age: int = Field(..., ge=16, le=100)  # Required, 16-100
#     major: str = Field(..., min_length=3)

#     @field_validator("name")
#     @classmethod
#     def name_must_not_be_numeric(cls, v):
#         if v.isdigit():
#             raise ValueError("Name cannot be purely numeric")
#         return v

#     @field_validator("major")
#     @classmethod
#     def major_must_be_valid(cls, v):
#         valid_majors = {"Software Engineering", "Computer Science", "Mathematics"}
#         if v not in valid_majors:
#             raise ValueError(f"Major must be one of {', '.join(valid_majors)}")
#         return v

# class StudentPUT(BaseModel):
#     name: Optional[str] = None
#     age: Optional[int] = None
#     major: Optional[str] = None

#     @field_validator("name", mode="before")
#     @classmethod
#     def validate_name(cls, name: Optional[str]):
#         if name and len(name) > 10:
#             raise ValueError("Name should not be more than 10 characters")
#         return name

# @app.post("/post-student/{student_id}")
# async def create_student(student_id: int, student: Student):
#     if student_id in students:
#         raise HTTPException(status_code=400, detail={"error": "Student ID already exists", "student_id": student_id})
#     students[student_id] = student.model_dump()
#     await asyncio.sleep(1)
#     return {"message": "Student created successfully", "student": students[student_id]}

# @app.put("/put-student/{student_id}")
# async def update_student(student_id: int, student: StudentPUT):
#     if student_id not in students:
#         raise HTTPException(status_code=404, detail="Student not found")
    
#     stored_student_data = students[student_id]
#     stored_student_model = Student(**stored_student_data)
#     update_data = student.model_dump(exclude_unset=True)
#     updated_student = stored_student_model.copy(update=update_data)
#     students[student_id] = updated_student.model_dump()
    
#     return {"message": "Student updated successfully", "student": students[student_id]}



# @app.delete("/delete-student/{student_id}")
# async def delete_student(student_id: int):
#     if student_id not in students:
#         raise HTTPException(status_code=404, detail={"error": "Student not found", "student_id": student_id})
#     del students[student_id]
#     return {"message": "Student deleted successfully", "student_id": student_id}

# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request, exc):
#     errors = []
#     for error in exc.errors():
#         errors.append({
#             "field": ".".join(map(str, error["loc"][1:])),  # Exclude "body new " 
#             "message": error["msg"],
#             "provided_value": error.get("input", None)
#         })
    
#     return JSONResponse(
#         status_code=422,
#         content={"error": "Validation failed", "details": errors},
#     )




from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, FastAPI, HTTPException
from app.database import get_async_db
from app import models, schemas
import asyncio
from app.tasks import create_user_message
app = FastAPI()

from sqlalchemy.future import select
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException

@app.post("/users/", response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_async_db)):
    existing_user = await db.execute(
        select(models.User).where(models.User.email == user.email)
    )
    existing_user = existing_user.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    new_user = models.User(
        username=user.username,
        email=user.email,
        password=user.password  # Hash it in production!
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    print("User created:", new_user.username)

    # ✅ Run Celery task in the background
    create_user_message.delay(new_user.id)

    return new_user


