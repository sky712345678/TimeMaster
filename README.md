# TimeMaster
This is a project for Database System course at NCKU  
To read this in HackMD, go to: https://hackmd.io/@zewunwang/Sy-qZ3P_d

## Prerequisites ##
#### Create a virtual environment ####
On Linux: `$ python3 -m venv venv`
On Windows: `> py -3 -m venv venv`
#### Activate/deactivate virtual environment ####
On Linux: `$ . venv/bin/activate`
On Windows: `> venv\Scripts\activate`
#### Install Flask in virtual environment ####
`$ pip install Flask`
#### Install Flask-SQLAlchemy in virtual environment ####
`$ pip install flask-sqlalchemy`

## Run server ##
On Linux, go to the path to app and run:
```
$ export FLASK_APP=main.py
$ python -m flask run
```
On Windows, go to the path to app and run:
```
> set FLASK_APP=main.py
> python -m flask run
```

## The structure of this project ##
```
/TimeMaster
    /MainApp
        /individual app
            __init__.py   #required
            views.py      #your code for "individual app"
        /Learning
            __init__.py
            views.py      #code for "Learning" app
        ...
        /templates
            your_template.html
            ...
        __init__.py       #initialize MainApp
        database.py       #for database file creation
        models.py         #for database definition
    main.py               #main function for the project
    README.md
```

## To develop a new app ##
1. create a new directory under "MainApp" directory
2. go to the new directory
3. create `__init__.py` file (可以空白)
4. create `views.py` file (也可以取別的名字) and start coding
例如：我開發了Learning這個App，把程式碼命名為`views.py`，並在其中寫了以下的function，查詢資料庫、列出所有的課程:
```python=
from flask import Flask                  #Flask
from flask import render_template        #rendering templates
from flask_sqlalchemy import SQLAlchemy  #SQL
from MainApp.database import db          #created database
from MainApp.models import Courses       #include the table in database

def listAllCourses():
    return render_template('learning_list_courses.html', values=Courses.query.all())
```
5. edit `main.py`
6. add a new line `from MainApp.YourApp import views as yourApp`
例如：我開發了Learning這個App，把程式碼命名為`views.py`，那麼我要新增：
`from MainApp.Learning import views as learning`
7. add routing and call the specific function as:
```python=
@app.route('some/url')
def specificFunction():
    return yourApp.specificFunction()
```
例如：我要用輸入一網址，並列出所有的課程：
```python=
@app.route('/learning/ListCourses')
def listCourses():
    return learning.listAllCourses()
```
See also:
https://flask.palletsprojects.com/en/1.1.x/ <- Flask official documentation
## To create a new table in database ##
1. edit `models.py`
2. add a new class and define attributes
例如：我要開"課程"的table：
```python=
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
```
See also:
https://flask-sqlalchemy.palletsprojects.com/en/2.x/ <- Flask SQLAlchemy official documentation
https://hackmd.io/@shaoeChen/SJ9x3N9zz?type=view <- tutorial by shaoeChen
