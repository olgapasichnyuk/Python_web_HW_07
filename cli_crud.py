import argparse
from datetime import datetime

from connect_db import session
from models import StudentsGroup, Student, Teacher, Course, Grade


parser = argparse.ArgumentParser(description='CRUD')

parser.add_argument('-a', '--action', help='Command: create, update, list, remove', required=True)
parser.add_argument('-m', '--model', required=True)
parser.add_argument('-n', '--name')
parser.add_argument('-id', '--id')
parser.add_argument('-g', '--grade')

arguments = parser.parse_args()
arg = vars(arguments)

MODELS = {"Teacher": Teacher,
          "Student": Student,
          "StudentsGroup": StudentsGroup,
          "Course": Course,
          "Grade": Grade
          }

action = arg.get("action")
object_name = arg.get("name")
grade = arg.get("grade")
model_name = MODELS.get(arg.get("model"))
try:
    object_id = int(arg.get("id"))
except TypeError:
    object_id = arg.get("id")


def create_person():
    session.add(model_name(fullname=object_name))
    session.commit()


def update_person():
    new_person = session.query(model_name).filter(model_name.id == object_id)
    if new_person:
        new_person.update({"fullname": object_name})
        session.commit()


def show_all_person():
    all_persons = session.query(model_name.fullname).all()
    for person in all_persons:
        print(person[0])


def remove_object():
    session.query(model_name).filter(model_name.id == object_id).delete()
    session.commit()


def create_group():
    session.add(model_name(group_name=object_name))
    session.commit()


def update_group():
    new_person = session.query(model_name).filter(model_name.id == object_id)
    if new_person:
        new_person.update({"group_name": object_name})
        session.commit()


def show_all_group():
    all_groups = session.query(model_name.group_name).all()
    for group in all_groups:
        print(group[0])


def create_course():
    session.add(model_name(course_name=object_name, teacher_id=object_id))
    session.commit()


def update_course():
    new_object = session.query(model_name).filter(model_name.id == object_id)
    if new_object:
        new_object.update({"course_name": object_name})
        session.commit()


def show_all_course():
    all_courses = session.query(model_name.course_name).all()
    for course in all_courses:
        print(course[0])


def create_grade():
    course_id = session.query(Course.id).filter(Course.course_name == object_name).one()[0]
    session.add(model_name(course_id=course_id, student_id=object_id, date_of=datetime.now(), grade=grade))
    session.commit()


def update_grade():
    new_object = session.query(model_name).filter(model_name.id == object_id)
    if new_object:
        new_object.update({"grade": grade})
        session.commit()


def show_grades():
    all_grades = session.query(model_name.grade).filter(model_name.course_id == object_id).all()
    for gr in all_grades:
        print(gr[0], end="; ")


crud = {Teacher: {"create": create_person,
                  "update": update_person,
                  "list": show_all_person,
                  "remove": remove_object},

        StudentsGroup: {"create": create_group,
                        "update": update_group,
                        "list": show_all_group,
                        "remove": remove_object},

        Student: {"create": create_person,
                  "update": update_person,
                  "list": show_all_person,
                  "remove": remove_object},

        Course: {"create": create_course,
                 "update": update_course,
                 "list": show_all_course,
                 "remove": remove_object},

        Grade: {"create": create_grade,
                "update": update_grade,
                "list": show_grades,
                "remove": remove_object}
        }

if __name__ == "__main__":
    
    crud[model_name][action]()
    
    # py cli_crud.py -a create -m Teacher -n "Маринчак Віктор"
    # py cli_crud.py -a update -m Teacher -id 1 -n "Косенко Оксана"
    # py cli_crud.py -a list -m Teacher
    # py cli_crud.py -a remove -m Teacher -id 1

    # py cli_crud.py -a create -m Student -n "Пасічнюк Ольга"
    # py cli_crud.py -a update -m Student -id 1 -n "Следь Іван"
    # py cli_crud.py -a list -m Student
    # py cli_crud.py -a remove -m Student -id 1

    # py cli_crud.py -a create -m StudentsGroup -n "нова група"
    # py cli_crud.py -a update -m StudentsGroup -id 1 -n "оновлена назва групи"
    # py cli_crud.py -a list -m StudentsGroup
    # py cli_crud.py -a remove -m StudentsGroup -id 1

    # py cli_crud.py -a create -m Course -n "Новий предмет" -id 1
    # py cli_crud.py -a update -m Course -id 1 -n "оновлена назва предмету"
    # py cli_crud.py -a list -m Course
    # py cli_crud.py -a remove -m Course -id 1

    # py cli_crud.py -a create -m Grade -n "Програмування" -id 1 -g 12
    # py cli_crud.py -a update -m Grade -id 1 -g 12
    # py cli_crud.py -a list -m Grade -id 1
    # py cli_crud.py -a remove -m Grade -id 1

