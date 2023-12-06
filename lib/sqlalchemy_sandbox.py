#!/usr/bin/env python3

from datetime import datetime

from sqlalchemy import (create_engine, desc, func,
    CheckConstraint, PrimaryKeyConstraint, UniqueConstraint,
    Index, Column, DateTime, Integer, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define a base class for declarative models
Base = declarative_base()

# Define the Student class, which inherits from Base
class Student(Base):
    __tablename__ = 'students'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='id_pk'),
        UniqueConstraint('email', name='unique_email'),
        CheckConstraint('grade BETWEEN 1 AND 12', name='grade_between_1_and_12')
    )

    Index('index_name', 'name')

    # Define columns for the students table
    id = Column(Integer(), primary_key=True)
    name = Column(String())
    email = Column(String(55))
    grade = Column(Integer())
    birthday = Column(DateTime())
    enrolled_date = Column(DateTime(), default=datetime.now())

    def __repr__(self):
        return f"Student {self.id}: " \
            + f"{self.name}, " \
            + f"Grade {self.grade}"

# Check if the script is being run as the main program
if __name__ == '__main__':
    # Create an in-memory SQLite database engine
    engine = create_engine('sqlite:///:memory:')
    
    # Create the students table in the database
    Base.metadata.create_all(engine)

    # Create a session to interact with the database
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create instances of Student class
    albert_einstein = Student(
        name="Albert Einstein",
        email="albert.einstein@zurich.edu",
        grade=6,
        birthday=datetime(year=1879, month=3, day=14),
    )
    alan_turing = Student(
        name="Alan Turing",
        email="alan.turing@sherborne.edu",
        grade=11,
        birthday=datetime(year=1912, month=6, day=23),
    )
   
    # Add students to the session and commit changes
    session.bulk_save_objects([albert_einstein, alan_turing])
    session.commit()
    
    # Query and print all students
    students = session.query(Student)
    print([student for student in students])
    
    # Query and print all students using another method
    students = session.query(Student).all()
    print(students)

    # Query and print names of all students
    names = [name for name in session.query(Student.name)]
    print(names)
    
    # Query and print students ordered by name
    students_by_name = [student for student in session.query(
        Student.name).order_by(Student.name)]
    print(students_by_name)

    # Query and print students ordered by grade in descending order
    students_by_grade_desc = [student for student in session.query(
        Student.name, Student.grade).order_by(desc(Student.grade))]
    print(students_by_grade_desc)

    # Query and print information about the oldest student
    oldest_student = [student for student in session.query(
        Student.name, Student.birthday).order_by(desc(Student.grade)).limit(1)]
    print(oldest_student)

    # Query and print information about the oldest student using first()
    oldest_student = session.query(
        Student.name, Student.birthday).order_by(
        desc(Student.grade)).first()
    print(oldest_student)

    # Query and print the count of students
    student_count = session.query(func.count(Student.id)).first()
    print(student_count)

    # Query and print the name of students with certain conditions
    query = session.query(Student).filter(
        Student.name.like('%Alan%'),
        Student.grade == 11
    )
    for record in query:
        print(record.name)

    # Update the grade of all students and commit changes
    for student in session.query(Student):
        student.grade += 1
    session.commit()

    # Print names and grades of all students after the update
    print([(student.name, student.grade) for student in session.query(Student)])
    
    # Query and delete a specific student (Albert Einstein)
    query = session.query(Student).filter(Student.name == "Albert Einstein")
    albert_einstein = query.first()
    session.delete(albert_einstein)
    session.commit()

    # Try to retrieve the deleted student
    albert_einstein = query.first()
    print(albert_einstein)  # Should print None

    # Query and delete all students with a certain condition
    query = session.query(Student).filter(Student.name == "Albert Einstein")
    query.delete()
    albert_einstein = query.first()
    print(albert_einstein)  # Should print None




