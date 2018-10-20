import sqlite3
from datetime import datetime
import numpy as np
from flask import Flask, render_template, request, url_for, redirect
app = Flask(__name__)


def days(dep_date, arr_date):
    date_format = "%d/%m/%Y"
    dep_date = datetime.strptime(dep_date, date_format)
    arr_date = datetime.strptime(arr_date, date_format)
    delta = arr_date - dep_date
    return delta.days


@app.route('/')
def trip():
    return render_template('trip.html')


@app.route('/result', methods=['GET', 'POST'])
def result():
    conn = sqlite3.connect('reise.db')
    c = conn.cursor()
    if request.method == 'POST':
        # try:
        emp = request.form['Employee']
        print(type(emp))
        dep_date = request.form['Departure date']
        arr_date = request.form['Arrival date']
        country = request.form['Country']
        # with sqlite3.connect("reise.db") as conn:
        #     c = conn.cursor()
        # query =
        # print(query)
        emp_id = c.execute("SELECT id_employee FROM Employees WHERE name = ?", (emp,))
        emp_id = emp_id.fetchone()[0]
        print('test', emp_id)
        country_id = c.execute("SELECT id_country FROM Countries WHERE country = ?", (country,)).fetchone()[0]
        days_ = days(dep_date, arr_date)
        rate = c.execute("SELECT rate FROM Countries WHERE country = ?", (country,)).fetchone()[0]
        pay_day = c.execute("SELECT day_payment FROM Countries WHERE country = ?", (country,)).fetchone()[0]
        sum_ = np.round(days_ * rate * pay_day, 2)
        c.execute("INSERT INTO Trips (employee_id, dep_date ,arr_date, country_id, sum) VALUES (?,?,?,?,?)", \
                  (emp_id, dep_date, arr_date, country_id, sum_))
        #             c.execute("INSERT INTO Trips (sum) SELECT dep_date, arr_date, arr_date - dep_date FROM Trips  ")
        conn.commit()
        msg = "Record successfully added"
            # return render_template("result.html", msg=msg)
            # return redirect(url_for('trip'), msg=msg, code=307)
        # except:
        #     conn.rollback()
        #     msg = "error in insert operation"
        # finally:
        return render_template("result.html", msg=msg)


@app.route('/list')
def list():
    conn = sqlite3.connect("reise.db")
    conn.row_factory = sqlite3.Row

    c = conn.cursor()
    c.execute("SELECT * FROM Trips")

    rows = c.fetchall()
    return render_template("list.html",rows = rows)


if __name__ == '__main__':
    app.run(host='localhost', port=5003,debug = True)