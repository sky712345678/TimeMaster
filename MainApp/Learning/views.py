from flask import Flask                  #Flask
from flask import render_template        #rendering template
from flask_sqlalchemy import SQLAlchemy  #SQL
from MainApp.database import db          #created database
from MainApp.models import Courses       #include the table in database
from MainApp.models import Studies
from MainApp.models import Assignments
from MainApp.models import Tests

def insertTuple(tupleToInsert):
    db.session.add(tupleToInsert)
    db.session.commit()

def course():
    return render_template('learning/learning_course_input.html')

def inputCourse(request):
    semester = None
    courseNumber = None
    courseName = None
    credits = None

    if request.method == 'POST':
        semester = request.form['semester']
        courseNumber = request.form['courseNumber']
        courseName = request.form['courseName']
        credits = request.form['credits']

        result = Courses.query.filter_by(CourseNumber=courseNumber).first()
        # Check the request and update the database
        if result is None:
            tupleToInsert = Courses(semester, courseNumber, courseName, credits)
            insertTuple(tupleToInsert)
            return '<h2>Successfully added.</h2>'
        else:
            return '<h2>Course already existed!!!</h2>'

def listAllCourses():
    '''
    result = db.session.execute('SELECT * FROM Courses')
    return render_template('learning_courses_listAll.html', courses=result)
    '''
    return render_template('learning/learning_courses_listAll.html', courses=Courses.query.all())

def study():
    return render_template('learning/learning_study_input.html', courses=Courses.query.all())

def inputStudy(request):
    courseNumber = None
    date = None
    duration = None
    content = None

    if request.method == 'POST':
        courseNumber = request.form['courseNumber']
        date = request.form['date']
        duration = request.form['duration']
        content = request.form['content']

        result = Studies.query.filter_by(CourseNumber=courseNumber, Date=date, Content=content).first()

        if result is None:
            tupleToInsert = Studies(courseNumber, date, duration, content)
            insertTuple(tupleToInsert)
            return '<h2>Successfully added.</h2>'
        else:
            return '<h2>Study record already existed!!!</h2>'

def listAllStudies():
    result = db.session.execute('SELECT S.CourseNumber, C.CourseName, S.Date, S.Duration, S.Content '+
                                'FROM Studies AS S, Courses AS C '+
                                'WHERE S.CourseNumber=C.CourseNumber')
    return render_template('learning/learning_study_listAll.html', studies=result)
    
    # return render_template('learning/learning_study_listAll.html', studies=Studies.query.all())

def test():
    return render_template('learning/learning_test_input.html', courses=Courses.query.all())

def inputTest(request):
    courseNumber = None
    date = None
    grade = None
    comment = None

    if request.method == 'POST':
        courseNumber = request.form['courseNumber']
        date = request.form['date']
        grade = request.form['grade']
        comment = request.form['comment']

        result = Tests.query.filter_by(CourseNumber=courseNumber, Date=date).first()

        if result is None:
            tupleToInsert = Tests(courseNumber, date, grade, comment)
            insertTuple(tupleToInsert)
            return '<h2>Successfully added.</h2>'
        else:
            return '<h2>Test record already existed!!!</h2>'

def listAllTests():
    result = db.session.execute('SELECT T.CourseNumber, C.CourseName, T.Date, T.Grade, T.Comment '+
                                'FROM Tests AS T, Courses AS C '+
                                'WHERE T.CourseNumber=C.CourseNumber')
    return render_template('learning/learning_test_listAll.html', tests=result)
    # return render_template('learning/learning_test_listAll.html', tests=Tests.query.all())

def assignment():
    return render_template('learning/learning_assignment_input.html', courses=Courses.query.all())

def inputAssignment(request):
    courseNumber = None
    description = None
    grade = None

    if request.method == 'POST':
        courseNumber = request.form['courseNumber']
        description = request.form['description']
        grade = request.form['grade']

        result = Assignments.query.filter_by(CourseNumber=courseNumber, Description=description).first()

        if result is None:
            tupleToInsert = Assignments(courseNumber, description, grade)
            insertTuple(tupleToInsert)
            return '<h2>Successfully added.</h2>'
        else:
            return '<h2>Assignment already existed!!!</h2>'

def listAllAssignments():
    result = db.session.execute('SELECT A.CourseNumber, C.CourseName, A.Description, A.Grade '+
                                'FROM Assignments AS A, Courses AS C '+
                                'WHERE A.CourseNumber=C.CourseNumber')
    return render_template('learning/learning_assignment_listAll.html', assignments=result)
    # return render_template('learning/learning_assignment_listAll.html', assignments=Assignments.query.all())