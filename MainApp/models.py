from .database import db

class Items(db.Model):
    Category = db.Column(db.VARCHAR(20), nullable=False)
    SerialNumber = db.Column(db.CHAR(6), primary_key=True)
    Name = db.Column(db.VARCHAR(50), primary_key=True)

    def __init__(self, Category, SerialNumber, Name):
        self.Category = Category
        self.SerialNumber = SerialNumber
        self.Name = Name

class Records(db.Model):
    SerialNumber = db.Column(db.CHAR(6), primary_key=True)
    Date = db.Column(db.CHAR(8), primary_key=True)
    Duration = db.Column(db.Integer, nullable=False)
    Goal = db.Column(db.VARCHAR(100))
    AchievePercentage = db.Column(db.Integer)
    Description = db.Column(db.VARCHAR(100))

    def __init__(self, SerialNumber, Date, Duration, Goal, AchievePercentage, Description):
        self.SerialNumber = SerialNumber
        self.Date = Date
        self.Duration = Duration
        self.Goal = Goal
        self.AchievePercentage = AchievePercentage
        self.Description = Description

class Goals(db.Model):
    SerialNumber = db.Column(db.CHAR(6), primary_key=True)
    Goal = db.Column(db.VARCHAR(100), primary_key=True)
    Achieved = db.Column(db.CHAR(1), nullable=False)
    SetDate = db.Column(db.CHAR(8), primary_key=True)
    AchieveDate = db.Column(db.CHAR(8))

    def __init__(self, SerialNumber, Goal, Achieved, SetDate, AchieveDate):
        self.SerialNumber = SerialNumber
        self.Goal = Goal
        self.Achieved = Achieved
        self.SetDate = SetDate
        self.AchieveDate = AchieveDate