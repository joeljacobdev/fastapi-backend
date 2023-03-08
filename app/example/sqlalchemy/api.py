from fastapi import APIRouter, Depends
from sqlalchemy import func, Integer
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.asyncio import AsyncSession

from app.example.sqlalchemy import schemas as app_schemas
from app.example.sqlalchemy.setup import get_db_session

router = APIRouter()


@router.get("/setup")
async def setup(session: AsyncSession = Depends(get_db_session)):
    await session.execute(
        app_schemas.College.__table__.insert(),
        [{"name": f"College {i}"} for i in range(10)],
    )
    result = await session.execute(select(app_schemas.College.id))
    college_ids = result.scalars().all()
    department_batches = []
    for college_id in college_ids:
        department_batches.extend(
            [{"college_id": college_id, "batch": batch} for batch in range(2010, 2023)]
        )
    await session.execute(
        app_schemas.DepartmentBatch.__table__.insert(),
        department_batches,
    )
    result = await session.execute(select(app_schemas.DepartmentBatch.id))
    department_batch_ids = result.scalars().all()
    courses = []
    for dept_batch_id in department_batch_ids:
        courses.extend(
            [
                {"name": f"Course {i}", "department_batch_id": dept_batch_id}
                for i in range(2)
            ]
        )
    await session.execute(
        app_schemas.Course.__table__.insert(),
        courses,
    )
    result = await session.execute(select(app_schemas.Course.id))
    course_ids = result.scalars().all()
    students = [app_schemas.Student(name=f"Student {i}") for i in range(100)]
    session.add_all(students)
    return []


@router.get("/m2m")
async def m2m(session: AsyncSession = Depends(get_db_session)):
    student_id = 1
    statement = (
        select(app_schemas.Student)
        .where(app_schemas.Student.id == student_id)
        .options(
            joinedload(app_schemas.Student.student_courses).options(
                joinedload(app_schemas.StudentCourse.course)
            )
        )
    )
    result = await session.execute(statement)
    return result.unique().all()


@router.get("/array_agg")
async def array_agg(session: AsyncSession = Depends(get_db_session)):
    college_id = 2
    statement = (
        select(
            app_schemas.College.name,
            func.array_agg(app_schemas.Course.id, type_=ARRAY(Integer)).label(
                "course_ids"
            ),
        )
        .outerjoin(
            app_schemas.DepartmentBatch,
            app_schemas.DepartmentBatch.college_id == app_schemas.College.id,
        )
        .outerjoin(
            app_schemas.Course,
            app_schemas.Course.department_batch_id == app_schemas.DepartmentBatch.id,
        )
        .where(app_schemas.College.id == college_id)
        .group_by(app_schemas.College.id)
    )
    result = await session.execute(statement)
    result = result.one()
    course_ids = result[1] if result else []
    return {"college_id": college_id, "course_ids": course_ids}
