from sqlalchemy import func, desc, select, and_

from connect_db import session
from models import StudentsGroup, Student, Teacher, Course, Grade


def select_01():
    """1.Знайти 5 студентів із найбільшим середнім балом з усіх предметів."""

    res = session.query(Student.fullname, func.round(func.avg(Grade.grade), 3).label("avg_grade")) \
        .select_from(Grade) \
        .join(Student) \
        .group_by(Student.id) \
        .order_by(desc("avg_grade")) \
        .limit(5) \
        .all()

    return res


def select_02(course_id: int):
    """2. Знайти студента із найвищим середнім балом з певного предмета."""
    res = session.query(Student.fullname,
                        Course.course_name,
                        func.round(func.avg(Grade.grade), 3).label("avg_grade")) \
        .select_from(Grade) \
        .join(Student) \
        .join(Course) \
        .filter(Course.id == course_id) \
        .group_by(Student.id, Course.id) \
        .order_by(desc("avg_grade")) \
        .limit(1) \
        .all()
    return res


def select_03(courses_id: int):
    """3. Знайти середній бал у групах з певного предмета."""

    res = session.query(Course.course_name,
                        StudentsGroup.group_name,
                        func.round(func.avg(Grade.grade), 3)) \
        .select_from(StudentsGroup) \
        .join(Student) \
        .join(Grade) \
        .join(Course) \
        .filter(Grade.course_id == courses_id) \
        .group_by(Course.course_name, StudentsGroup.group_name) \
        .all()

    return res


def select_04():
    """4. Знайти середній бал на потоці (по всій таблиці оцінок)"""

    res = session.query(func.round(func.avg(Grade.grade), 3)).one()

    return res


def select_05(teacher_id: int):
    """5.Знайти які курси читає певний викладач."""

    res = session.query(Course.course_name) \
        .select_from(Course) \
        .filter(Course.teacher_id == teacher_id) \
        .all()

    teacher_name = session.query(Teacher.fullname).filter(Teacher.id == teacher_id).one()[0]

    return teacher_name, res


def select_06(group_id: int):
    """6.Знайти список студентів у певній групі."""

    res = session.query(Student.fullname).select_from(Student).filter(Student.group_id == group_id).all()

    return res


def select_07(group_id: int, course_id: int):
    """7.Знайти оцінки студентів у окремій групі з певного предмета."""

    res = session.query(Grade.grade).select_from(Grade).join(Student).filter(
        and_(Grade.course_id == course_id, Student.group_id == group_id)).all()

    return res


def select_08(teacher_id):
    """8.Знайти середній бал, який ставить певний викладач зі своїх предметів."""
    res = session.query(func.round(func.avg(Grade.grade), 3)) \
        .select_from(Grade) \
        .join(Course) \
        .filter(Course.teacher_id == teacher_id) \
        .one()

    return res


def select_09(student_id: int):
    """9. Знайти список курсів, які відвідує студент"""

    res = session.query(Course.course_name).select_from(Course).join(Grade).filter(Grade.student_id == student_id).all()

    return res


def select_10(student_id: int, teacher_id: int):
    """10. Список курсів, які певному студенту читає певний викладач."""
    res = session.query(Course.course_name) \
        .select_from(Course) \
        .join(Grade) \
        .join(Student) \
        .filter(and_(Student.id == student_id, Course.teacher_id == teacher_id)) \
        .all()

    return res


def select_11(student_id: int, teacher_id: int):
    """додаткове1 Середній бал, який певний викладач ставить певному студентові."""

    res = session.query(func.round(func.avg(Grade.grade), 3)) \
        .select_from(Grade) \
        .join(Course) \
        .filter(and_(Grade.student_id == student_id, Course.teacher_id == teacher_id)) \
        .one()

    return res


def select_12(group_id: int, course_id: int):
    """додаткове2 Оцінки студентів у певній групі з певного предмета на останньому занятті."""

    last_class_day = session.query(func.max(Grade.date_of)).select_from(Grade).join(Student).filter(
        and_(Student.group_id == group_id, Grade.course_id == course_id)).one()[0]

    res = session.query(Grade.grade) \
        .select_from(Grade) \
        .join(Student) \
        .filter(and_(Grade.course_id == course_id, Student.group_id == group_id, Grade.date_of == last_class_day)) \
        .all()

    return res


def print_resalts_all_selects():
    # select_01
    print("\n1.Знайти 5 студентів із найбільшим середнім балом з усіх предметів.\nРезультат:")
    for r in select_01():
        print('{:<25}: {:<10} '.format(r[0], r[1]))


    # select_02
    print("\n2. Знайти студента із найвищим середнім балом з певного предмета.\nРезультат:")
    for r in select_02(3):
        print('Студент {} має з предмету {} найвищий середній бал {}'.format(r[0], r[1], r[2]))

    # select_03
    print("\n3. Знайти середній бал у групах з певного предмета.\nРезультат:")
    for r in select_03(3):
        print('{:<25} {:<25} {:<10}'.format(r[0], r[1], r[2]))

    # select_04
    print("\n4. Знайти середній бал на потоці (по всій таблиці оцінок)\nРезультат:")
    print('Середній бал на потоці (по всій таблиці оцінок): {:<5}'.format(select_04()[0]))

    # select_05
    print("\n5.Знайти які курси читає певний викладач.\nРезультат:")
    teacher_name, res = select_05(3)
    print(f"Викладач {teacher_name} читаэ наступны курси:")
    for course_name in res:
        print(course_name[0])

    # select_06
    print("\n6.Знайти список студентів у певній групі.\nРезультат:")
    for student_name in set(select_06(3)):
        print(student_name[0])

    # select_07
    print("\n7.Знайти оцінки студентів у окремій групі з певного предмета.\nРезультат:")
    print(list(map(lambda x: x[0], select_07(2, 5))))

    # select_08
    print("\n8.Знайти середній бал, який ставить певний викладач зі своїх предметів.\nРезультат:")
    print('Середній бал, який ставить певний викладач зі своїх предметів: {:<5}'.format(select_08(4)[0]))

    # select_09
    print("\n9. Знайти список курсів, які відвідує студент.\nРезультат:")
    for course in set(map(lambda x: x[0], select_09(16))):
        print(course)

    # select_10
    print("\n10. Список курсів, які певному студенту читає певний викладач.\nРезультат:")
    for course in set(map(lambda x: x[0], select_10(16, 3))):
        print(course)

    # select_11
    print("\nдодаткове1 Середній бал, який певний викладач ставить певному студентові.\nРезультат:")
    print(select_11(16, 3)[0])

    # select_12
    print("\nдодаткове2 Оцінки студентів у певній групі з певного предмета на останньому занятті.\nРезультат:")
    print(list(map(lambda x: x[0], select_12(1, 5))))
    print("\n")


if __name__ == '__main__':
    print_resalts_all_selects()
