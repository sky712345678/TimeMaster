from .database import db
from datetime import datetime

class Items(db.Model):
    __tablename__ = 'Items'
    Category = db.Column(db.VARCHAR(20), nullable=False)
    SerialNumber = db.Column(db.CHAR(6), primary_key=True)
    Name = db.Column(db.VARCHAR(50))

    # item_referenced_by_record = db.relationship('Records', backref='Items', lazy=True)
    item_referenced_by_goal = db.relationship('Goals', lazy=True)

    def __init__(self, Category, SerialNumber, Name):
        self.Category = Category
        self.SerialNumber = SerialNumber
        self.Name = Name

class Records(db.Model):
    __tablename__ = 'Records'
    SerialNumber = db.Column(db.CHAR(6), primary_key=True)
    Date = db.Column(db.CHAR(10), primary_key=True, default=datetime.today().strftime("%Y/%m/%d"))
    Duration = db.Column(db.Integer, nullable=False)
    Goal = db.Column(db.VARCHAR(100), nullable=True, default=None)
    AchievePercentage = db.Column(db.Integer, default=None)
    SetDate = db.Column(db.CHAR(10), nullable=True, default=None)
    Description = db.Column(db.VARCHAR(100))

    __table_args__ = (
        db.ForeignKeyConstraint(['SerialNumber', 'Goal', 'SetDate'], ['Goals.SerialNumber', 'Goals.Goal', 'Goals.SetDate']),
    )

    def __init__(self, SerialNumber, Date, Duration, Goal, AchievePercentage, GoalSetDate, Description):
        self.SerialNumber = SerialNumber
        self.Date = Date
        self.Duration = Duration
        self.Goal = Goal
        self.AchievePercentage = AchievePercentage
        self.SetDate = GoalSetDate
        self.Description = Description

class Goals(db.Model):
    __tablename__ = 'Goals'
    SerialNumber = db.Column(db.CHAR(6), primary_key=True)
    Goal = db.Column(db.VARCHAR(100), primary_key=True)
    Achieved = db.Column(db.CHAR(1), nullable=False)
    SetDate = db.Column(db.CHAR(10), primary_key=True)
    AchieveDate = db.Column(db.CHAR(10))

    __table_args__ = (
        db.ForeignKeyConstraint(['SerialNumber'], ['Items.SerialNumber']),
    )

    SerialNumber_referenced_by_record = db.relationship('Records', lazy=True, foreign_keys='Records.SerialNumber')
    Goal_referenced_by_record = db.relationship('Records', lazy=True, foreign_keys='Records.Goal')
    SetDate_referenced_by_record = db.relationship('Records', lazy=True, foreign_keys='Records.SetDate')

    def __init__(self, SerialNumber, Goal):
        self.SerialNumber = SerialNumber
        self.Goal = Goal
        self.Achieved = 'N'
        self.SetDate = datetime.today().strftime("%Y/%m/%d")
        self.AchieveDate = None