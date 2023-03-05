from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql.schema import ForeignKey, Table
from sqlalchemy.sql.sqltypes import DateTime


from connect_db import engine, session

"""Реалізуйте свої моделі SQLAlchemy, для таблиць:

Таблиця студентів;
Таблиця груп;
Таблиця викладачів;
Таблиця предметів із вказівкою викладача, який читає предмет;
Таблиця де кожен студент має оцінки з предметів із зазначенням коли оцінку отримано;"""

Base = declarative_base()


class StudentsGroup(Base):
    __tablename__ = "students_groups"
    id = Column(Integer, primary_key=True)
    group_name = Column(String(250))


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    fullname = Column(String(250))
    group_id = Column(Integer, ForeignKey("students_groups.id"))
    group = relationship("StudentsGroup", backref="students")


class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True)
    fullname = Column(String(250))


class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    course_name = Column(String(50))
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    teacher = relationship("Teacher", backref="courses")


class Grade(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True)
    course_name = Column(String(50))
    course_id = Column(Integer, ForeignKey("courses.id"))
    student_id = Column(Integer, ForeignKey("students.id"))
    grade = Column(Integer)
    date_of = Column(DateTime)
    course = relationship("Course", backref="grades")
    student = relationship("Student", backref="grades")


Base.metadata.create_all(engine)
Base.metadata.bind = engine
