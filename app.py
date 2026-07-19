from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "attendance123"

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'revathi*123'
app.config['MYSQL_DB'] = 'attendance_db'

mysql = MySQL(app)

# Home
@app.route('/')
def home():
    return redirect('/login')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM admin WHERE username=%s AND password=%s",
            (username, password)
        )
        user = cur.fetchone()

        if user:
            session['admin'] = username
            return redirect('/dashboard')
        else:
            return "Invalid Username or Password"

    return render_template('login.html')


# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'admin' in session:
        return render_template('dashboard.html')
    return redirect('/login')


# Student List
@app.route('/students')
def students():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students")
    data = cur.fetchall()
    return render_template('students.html', students=data)


# Add Student
@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form['name']
    roll = request.form['roll']
    dept = request.form['department']

    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO students(name, roll_no, department) VALUES(%s,%s,%s)",
        (name, roll, dept)
    )
    mysql.connection.commit()

    return redirect('/students')


# Attendance Page
@app.route('/attendance')
def attendance():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students")
    students = cur.fetchall()
    return render_template('attendance.html', students=students)


# Save Attendance
@app.route('/save_attendance', methods=['POST'])
def save_attendance():
    student_id = request.form['student_id']
    attendance_date = request.form['attendance_date']
    status = request.form['status']

    cur = mysql.connection.cursor()
    cur.execute(
        """
        INSERT INTO attendance(student_id, attendance_date, status)
        VALUES(%s, %s, %s)
        """,
        (student_id, attendance_date, status)
    )

    mysql.connection.commit()

    return redirect('/report')


# Report
@app.route('/report')
def report():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT students.name,
               students.roll_no,
               students.department,
               attendance.attendance_date,
               attendance.status
        FROM attendance
        JOIN students
        ON attendance.student_id = students.id
        ORDER BY attendance.attendance_date DESC
    """)

    records = cur.fetchall()

    return render_template('report.html', records=records)


# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)