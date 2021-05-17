from .database import db

# Learning
class Courses(db.Model):
    Semester = db.Column(db.VARCHAR(6), nullable=False)
    CourseNumber = db.Column(db.CHAR(6), primary_key=True)
    CourseName = db.Column(db.VARCHAR(50), nullable=False)
    Credits = db.Column(db.Integer)

    def __init__(self, Semester, CourseNumber, CourseName, Credits):
        self.Semester = Semester
        self.CourseNumber = CourseNumber
        self.CourseName = CourseName
        self.Credits = Credits


class Studies(db.Model):
    CourseNumber = db.Column(db.CHAR(6), primary_key=True)
    Date = db.Column(db.CHAR(8), primary_key=True)
    Duration = db.Column(db.Integer, nullable=False)
    Content = db.Column(db.VARCHAR(100), primary_key=True)

    def __init__(self, CourseNumber, Date, Duration, Content):
        self.CourseNumber = CourseNumber
        self.Date = Date
        self.Duration = Duration
        self.Content = Content


class Tests(db.Model):
    CourseNumber = db.Column(db.CHAR(6), primary_key=True)
    Date = db.Column(db.CHAR(8), nullable=False, primary_key=True)
    Grade = db.Column(db.Integer, nullable=False)
    Comment = db.Column(db.VARCHAR(100))

    def __init__(self, CourseNumber, Date, Grade, Comment):
        self.CourseNumber = CourseNumber
        self.Date = Date
        self.Grade = Grade
        self.Comment = Comment


class Assignments(db.Model):
    CourseNumber = db.Column(db.CHAR(6), primary_key=True)
    Description = db.Column(db.VARCHAR(100), primary_key=True)
    Grade = db.Column(db.Integer, nullable=False)

    def __init__(self, CourseNumber, Description, Grade):
        self.CourseNumber = CourseNumber
        self.Description = Description
        self.Grade = Grade