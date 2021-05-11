from .database import db

class Courses(db.Model):
    Semester = db.Column(db.VARCHAR(6), nullable=False)
    CourseNumber = db.Column(db.CHAR(6), primary_key=True)
    CourseName = db.Column(db.VARCHAR(100), nullable=False)
    Credits = db.Column(db.Integer)

    def __init__(self, Semester, CourseNumber, CourseName, Credits):
        self.Semester = Semester
        self.CourseNumber = CourseNumber
        self.CourseName = CourseName
        self.Credits = Credits