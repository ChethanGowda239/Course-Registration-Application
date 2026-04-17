from flask import Flask, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = "secret123"

# ---------------- ADMIN CREDENTIALS ----------------
ADMIN_USERNAME = "snpsu"
ADMIN_PASSWORD = "snpsu"

# ---------------- DATABASE CONNECTION ----------------
client = MongoClient("mongodb://localhost:27017/")
db = client["course_db"]
students_collection = db["students"]

def get_db_connection():
    return db

# ---------------- HOME / STUDENT REGISTER ----------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    # POST request
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    if students_collection.find_one({"email": email}):
        flash("❌ Email already registered", "danger")
        return redirect(url_for('register'))

    students_collection.insert_one({
        "name": name,
        "email": email,
        "password": password,
        "subscribed_courses": []
    })

    flash("✅ Registration successful", "success")
    return redirect(url_for('student_login'))

# ---------------- STUDENT LOGIN ----------------
@app.route('/student_login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        student = students_collection.find_one({
            "email": email,
            "password": password
        })

        if student:
            session['student'] = student['email']   # ✅ session set
            session['student_name'] = student['name']
            flash("✅ Student login successful", "success")
            return redirect(url_for('dashboard'))   # ✅ redirect here
        else:
            flash("❌ Invalid email or password", "danger")

    return render_template('student_login.html')


# ---------------- ADMIN LOGIN ----------------
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin'] = True
            flash("✅ Admin login successful", "success")
            return redirect(url_for('view'))
        else:
            flash("❌ Invalid admin credentials", "danger")

    return render_template('admin_login.html')

# ---------------- VIEW STUDENTS (ADMIN) ----------------
@app.route('/view')
def view():
    if 'admin' not in session:
        flash("❌ Admin login required", "danger")
        return redirect(url_for('admin_login'))

    students = list(students_collection.find({}, {
        "_id": 1,
        "name": 1,
        "email": 1
    }))

    return render_template('view.html', students=students)

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    flash("✅ Logged out successfully", "success")
    return redirect(url_for('index'))


@app.route('/dashboard')
def dashboard():
    if 'student' not in session:
        flash("❌ Please login first", "danger")
        return redirect(url_for('student_login'))

    student = students_collection.find_one({"email": session['student']})
    subscribed_courses = student.get('subscribed_courses', [])

    return render_template('dashboard.html', subscribed_courses=subscribed_courses)

# ============ SUBJECT PAGES ============
@app.route('/python')
def python_course():
    if 'student' not in session:
        flash("❌ Please login first", "danger")
        return redirect(url_for('student_login'))
    
    student = students_collection.find_one({"email": session['student']})
    if 'python' not in student.get('subscribed_courses', []):
        flash("❌ Please subscribe to Python first", "danger")
        return redirect(url_for('dashboard'))
    
    return render_template('python.html')

@app.route('/java')
def java_course():
    if 'student' not in session:
        flash("❌ Please login first", "danger")
        return redirect(url_for('student_login'))
    
    student = students_collection.find_one({"email": session['student']})
    if 'java' not in student.get('subscribed_courses', []):
        flash("❌ Please subscribe to Java first", "danger")
        return redirect(url_for('dashboard'))
    
    return render_template('java.html')

@app.route('/sql')
def sql_course():
    if 'student' not in session:
        flash("❌ Please login first", "danger")
        return redirect(url_for('student_login'))
    
    student = students_collection.find_one({"email": session['student']})
    if 'sql' not in student.get('subscribed_courses', []):
        flash("❌ Please subscribe to SQL first", "danger")
        return redirect(url_for('dashboard'))
    
    return render_template('sql.html')

@app.route('/web')
def web_course():
    if 'student' not in session:
        flash("❌ Please login first", "danger")
        return redirect(url_for('student_login'))
    
    student = students_collection.find_one({"email": session['student']})
    if 'web' not in student.get('subscribed_courses', []):
        flash("❌ Please subscribe to Web Programming first", "danger")
        return redirect(url_for('dashboard'))
    
    return render_template('web.html')

@app.route('/dsa')
def dsa_course():
    if 'student' not in session:
        flash("❌ Please login first", "danger")
        return redirect(url_for('student_login'))
    
    student = students_collection.find_one({"email": session['student']})
    if 'dsa' not in student.get('subscribed_courses', []):
        flash("❌ Please subscribe to DSA first", "danger")
        return redirect(url_for('dashboard'))
    
    return render_template('dsa.html')

@app.route('/c')
def c_course():
    if 'student' not in session:
        flash("❌ Please login first", "danger")
        return redirect(url_for('student_login'))
    
    student = students_collection.find_one({"email": session['student']})
    if 'c' not in student.get('subscribed_courses', []):
        flash("❌ Please subscribe to C first", "danger")
        return redirect(url_for('dashboard'))
    
    return render_template('c.html')

@app.route('/cpp')
def cpp_course():
    if 'student' not in session:
        flash("❌ Please login first", "danger")
        return redirect(url_for('student_login'))
    
    student = students_collection.find_one({"email": session['student']})
    if 'cpp' not in student.get('subscribed_courses', []):
        flash("❌ Please subscribe to C++ first", "danger")
        return redirect(url_for('dashboard'))
    
    return render_template('cpp.html')


@app.route('/subscribe/<course>', methods=['POST'])
def subscribe(course):
    if 'student' not in session:
        return {"success": False, "message": "Not logged in"}, 401

    student_email = session['student']
    students_collection.update_one(
        {"email": student_email},
        {"$addToSet": {"subscribed_courses": course}}  # addToSet to avoid duplicates
    )
    return {"success": True, "message": f"Subscribed to {course}"}


@app.route('/admin_dashboard')
def admin_dashboard():
    if 'admin' not in session:
        flash("❌ Admin login required", "danger")
        return redirect(url_for('admin_login'))

    return render_template('admin_dashboard.html')

# ---------------- ABOUT PAGE ----------------
@app.route('/about')
def about():
    return render_template('about.html')

# ---------------- RUN APP ----------------
if __name__ == '__main__':
    app.run(debug=True)
