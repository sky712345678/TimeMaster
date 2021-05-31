from .database import db
from datetime import datetime

class Items(db.Model):
    __tablename__ = 'Items'
    Category = db.Column(db.VARCHAR(20), nullable=False)
    ItemNumber = db.Column(db.CHAR(6), primary_key=True)
    Name = db.Column(db.VARCHAR(50), nullable=False)

    item_referenced_by_record = db.relationship('Records', lazy=True)
    item_referenced_by_goal = db.relationship('Goals', lazy=True)

    def __init__(self, category, itemNumber, name):
        self.Category = category
        self.ItemNumber = itemNumber
        self.Name = name

class Records(db.Model):
    __tablename__ = 'Records'
    ItemNumber = db.Column(db.CHAR(6), primary_key=True)
    Date = db.Column(db.CHAR(10), primary_key=True, default=datetime.today().strftime("%Y/%m/%d"))
    Duration = db.Column(db.Integer, nullable=False)
    GoalNumber = db.Column(db.CHAR(6), default=None)
    AchievePercentage = db.Column(db.Integer, default=None)
    Description = db.Column(db.VARCHAR(100))

    __table_args__ = (
        db.ForeignKeyConstraint(['ItemNumber'], ['Items.ItemNumber']),
        db.ForeignKeyConstraint(['GoalNumber'], ['Goals.GoalNumber']),
    )

    def __init__(self, itemNumber, date, duration, goalNumber, achievePercentage, description):
        self.ItemNumber = itemNumber
        self.Date = date
        self.Duration = duration
        self.GoalNumber = goalNumber
        self.AchievePercentage = achievePercentage
        self.Description = description

class Goals(db.Model):
    __tablename__ = 'Goals'
    GoalNumber = db.Column(db.CHAR(6), primary_key=True)
    ItemNumber = db.Column(db.CHAR(6), nullable=False)
    Goal = db.Column(db.VARCHAR(100), nullable=False)
    Achieved = db.Column(db.CHAR(1), nullable=False)
    SetDate = db.Column(db.CHAR(10))
    AchieveDate = db.Column(db.CHAR(10))

    __table_args__ = (
        db.ForeignKeyConstraint(['ItemNumber'], ['Items.ItemNumber']),
    )

    goal_referenced_by_record = db.relationship('Records', lazy=True, foreign_keys='Records.GoalNumber')

    def __init__(self, goalNumber, itemNumber, goal):
        self.GoalNumber = goalNumber
        self.ItemNumber = itemNumber
        self.Goal = goal
        self.Achieved = 'N'
        self.SetDate = datetime.today().strftime("%Y/%m/%d")
        self.AchieveDate = None