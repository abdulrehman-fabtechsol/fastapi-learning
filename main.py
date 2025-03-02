from fastapi import FastAPI
import asyncio
from fastapi import HTTPException
from typing import Optional

app = FastAPI()

# Define the student dictionary
student = {
    1: {"name": "Alice", "age": 20, "major": "Computer Science"},
    2: {"name": "Bob", "age": 22, "major": "Mathematics"},
    3: {"name": "Charlie", "age": 21, "major": "Physics"}
}

@app.get("/all-students")
async def say_hello():
    await asyncio.sleep(1)  # Simulating async work
    print("Hello")
    return {"message": "Hello", "students": student}



@app.get("/get-student/{student_id}")
async def get_student(student_id: int):
    if student_id <= 10:
        return {"error": "student_id must be greater than 10"}
    await asyncio.sleep(1)
    return student[student_id]


@app.get("/get-student-params")
async def get_student(*,student_id: Optional[int] = None,name: Optional[str] = None):
    try:
        print(name)
        if student_id is None:
            return {"students": student}
        if student_id <= 10:
            raise ValueError("student_id must be greater than 10")
        await asyncio.sleep(1)
        return student[student_id]
    except KeyError:
        raise HTTPException(status_code=404, detail="Student not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

