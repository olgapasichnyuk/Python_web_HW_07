from datetime import timedelta, datetime
from random import choice, randint

import faker
from sqlalchemy import select

from connect_db import session
from models import StudentsGroup, Student, Teacher, Course, Grade

"""Заповніть отриману базу даних випадковими даними:
(~30-50 студентів, 3 групи, 5-8 предметів, 3-5 викладачів, 
до 20 оцінок у кожного студента з усіх предметів).
Використовуйте пакет Faker для наповнення. """

NAME_OF_GROUPS = ["група 1", "група 2", "група 3"]
COURSES = [
    "Вища математика",
    "Дискретна математика",
    "Лінійна Алгебра",
    "Програмування",
    "Теорія імовірності",
    "Історія України",
    "Англійська",
    "Креслення"
]

NUMBER_TEACHERS = 5
NUMBER_STUDENTS = 50


def generate_list_with_fake_names(required_amount) -> list[str]:
    res = []
    fake_data = faker.Faker()

    for _ in range(required_amount):
        res.append(fake_data.name())

    return res


def seed_groups():
    for group_name in NAME_OF_GROUPS:
        session.add(StudentsGroup(group_name=group_name))
    session.commit()


def seed_teachers():
    teacher_names = generate_list_with_fake_names(NUMBER_TEACHERS)
    for teacher_name in teacher_names:
        session.add(Teacher(fullname=teacher_name))
    session.commit()


def seed_students():
    group_ids = session.scalars(select(StudentsGroup.id)).all()
    student_names = generate_list_with_fake_names(NUMBER_STUDENTS)
    for student_name in student_names:
        student = Student(fullname=student_name, group_id=choice(group_ids))
        session.add(student)
    session.commit()


def seed_courses():
    teachers_ids = session.scalars(select(Teacher.id)).all()
    for name_of_course in COURSES:
        course = Course(course_name=name_of_course, teacher_id=choice(teachers_ids))
        session.add(course)
    session.commit()


def seed_grades():
    courses_ids = session.scalars(select(Course.id)).all()
    students_ids = session.scalars(select(Student.id)).all()

    start_date = datetime.strptime("2022-09-01", "%Y-%m-%d")
    end_date = datetime.strptime("2023-06-15", "%Y-%m-%d")

    def get_list_date(start, end) -> list:
        result = []
        current_date = start
        while current_date <= end:
            if current_date.isoweekday() < 6:
                result.append(current_date)
            current_date += timedelta(1)
        return result

    list_dates = get_list_date(start_date, end_date)

    for day in list_dates:
        random_course_id = choice(courses_ids)
        random_student_ids = [choice(students_ids) for _ in range(5)]
        for random_student in random_student_ids:
            grade = Grade(grade=randint(1, 12),
                          date_of=day,
                          student_id=random_student,
                          course_id=random_course_id)
            session.add(grade)
    session.commit()


def seed():
    seed_groups()
    seed_teachers()
    seed_students()
    seed_courses()
    seed_grades()


if __name__ == "__main__":
    seed()
