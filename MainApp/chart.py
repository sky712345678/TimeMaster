from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route("/")
def chart():
    labels = ["January","February","March","April","May","June","July","August"]
    values = [10, 2, 1, 7, 9, 3, 4, 5]
    values2 = [9, 4, 3, 8, 9, 6, 7, 6]
    return render_template('chart.html', values=values, pass_labels=labels, values2=values2)


if __name__ == "__main__":
    app.run(host='127.0.0.2', port="5001", debug=True)

