from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    UniqueConstraint,
    DateTime,
    func,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

from app.example.sqlalchemy.setup import Base


class DateMixin:
    updated_at = Column(DateTime, onupdate=func.now())
    created_at = Column(DateTime, server_default=func.now())


class College(DateMixin, Base):
    __tablename__ = "app__colleges"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    department_batches = relationship("DepartmentBatch", back_populates="college")

    def __repr__(self):
        return self.name


class DepartmentBatch(DateMixin, Base):
    __tablename__ = "app__department_batch"
    id = Column(Integer, primary_key=True)
    college_id = Column(Integer, ForeignKey("app__colleges.id"))
    batch = Column(Integer)
    college = relationship("College", back_populates="department_batches")

    def __repr__(self):
        return f"{self.college.name} {self.batch}"


class Course(DateMixin, Base):
    __tablename__ = "app__course"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    department_batch_id = Column(Integer, ForeignKey("app__department_batch.id"))
    course_students = relationship("StudentCourse", back_populates="course")
    students = association_proxy("course_students", "student")


class StudentCourse(DateMixin, Base):
    __tablename__ = "app__student_course"
    __table_args__ = (
        UniqueConstraint("course_id", "student_id", name="student_course_contraint"),
    )
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("app__course.id"))
    student_id = Column(Integer, ForeignKey("app__student.id"))
    joining_year = Column(Integer)
    student = relationship("Student", back_populates="student_courses")
    course = relationship("Course", back_populates="course_students")


class Student(DateMixin, Base):
    __tablename__ = "app__student"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    student_courses = relationship("StudentCourse", back_populates="student")
    courses = association_proxy("student_courses", "course")
