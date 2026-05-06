"""
University Database – Flask Frontend
=====================================
Run:
    pip install flask flask-mysqldb werkzeug
    python app.py

Set environment variables (or edit DEFAULT_CONFIG below):
    DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, SECRET_KEY
"""
import bcrypt
import pymysql
pymysql.install_as_MySQLdb()
import os
from flask import (Flask, render_template_string, request,
                   redirect, url_for, flash, session, g)
from werkzeug.security import generate_password_hash, check_password_hash

# — App & config —
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-me-in-production")

def get_db():
    return pymysql.connect(
        host=os.environ.get('MYSQL_HOST', 'mysql.railway.internal'),
        user=os.environ.get('MYSQL_USER'),
        password=os.environ.get('MYSQL_PASSWORD'),
        database=os.environ.get('MYSQL_DB'),
        port=int(os.environ.get('MYSQL_PORT', 3306)),
        cursorclass=pymysql.cursors.DictCursor
    )
# ── BASE HTML TEMPLATE ──────────────────────────────────────
BASE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>University_Of_O – {% block title %}{% endblock %}</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=DM+Sans:wght@300;400;500&display=swap');
  :root{
    --ink:#0d0d0d;--paper:#f5f0e8;--gold:#c9a84c;--rust:#b34a2f;
    --muted:#7a7060;--card:#fffdf7;--border:#e0d8c8;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  body{font-family:'DM Sans',sans-serif;background:var(--paper);color:var(--ink);min-height:100vh}
  nav{background:var(--ink);padding:0 2rem;display:flex;align-items:center;gap:2rem;height:56px}
  nav a{color:#fff;text-decoration:none;font-size:.85rem;letter-spacing:.06em;text-transform:uppercase;opacity:.75;transition:.2s}
  nav a:hover,nav a.active{opacity:1;color:var(--gold)}
  nav .brand{font-family:'Playfair Display',serif;color:var(--gold);font-size:1.25rem;margin-right:auto}
  .container{max-width:1100px;margin:0 auto;padding:2.5rem 1.5rem}
  h1{font-family:'Playfair Display',serif;font-size:2rem;margin-bottom:1.5rem}
  h2{font-family:'Playfair Display',serif;font-size:1.4rem;margin-bottom:1rem}
  .card{background:var(--card);border:1px solid var(--border);border-radius:4px;padding:1.75rem;margin-bottom:1.5rem;box-shadow:0 2px 8px rgba(0,0,0,.04)}
  table{width:100%;border-collapse:collapse;font-size:.9rem}
  th{background:var(--ink);color:#fff;padding:.65rem 1rem;text-align:left;font-weight:500;letter-spacing:.04em}
  td{padding:.6rem 1rem;border-bottom:1px solid var(--border)}
  tr:hover td{background:#f0ead8}
  .btn{display:inline-block;padding:.5rem 1.25rem;border-radius:3px;font-size:.85rem;font-weight:500;cursor:pointer;border:none;transition:.2s;text-decoration:none}
  .btn-primary{background:var(--ink);color:#fff}.btn-primary:hover{background:#333}
  .btn-gold{background:var(--gold);color:#fff}.btn-gold:hover{background:#b8923e}
  .btn-danger{background:var(--rust);color:#fff}.btn-danger:hover{background:#922b1a}
  .btn-sm{padding:.35rem .85rem;font-size:.8rem}
  label{display:block;font-size:.82rem;font-weight:500;margin-bottom:.35rem;color:var(--muted)}
  input,select,textarea{width:100%;padding:.55rem .85rem;border:1px solid var(--border);border-radius:3px;font-size:.9rem;font-family:inherit;background:#fff;margin-bottom:1rem}
  input:focus,select:focus,textarea:focus{outline:none;border-color:var(--gold)}
  .grid-2{display:grid;grid-template-columns:1fr 1fr;gap:1.25rem}
  .alert{padding:.75rem 1rem;border-radius:3px;margin-bottom:1rem;font-size:.9rem}
  .alert-success{background:#e8f5e9;color:#2e7d32;border:1px solid #a5d6a7}
  .alert-error{background:#fdecea;color:#c62828;border:1px solid #ef9a9a}
  .badge{display:inline-block;padding:.2rem .6rem;border-radius:12px;font-size:.75rem;font-weight:500}
  .badge-gold{background:#fdf3d8;color:#7a5a00}
  .badge-green{background:#e8f5e9;color:#1b5e20}
  .stat-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:1rem;margin-bottom:2rem}
  .stat{background:var(--card);border:1px solid var(--border);border-radius:4px;padding:1.25rem;text-align:center}
  .stat-num{font-family:'Playfair Display',serif;font-size:2.2rem;color:var(--gold)}
  .stat-lbl{font-size:.78rem;text-transform:uppercase;letter-spacing:.08em;color:var(--muted)}
  .page-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:1.5rem}
  .empty{text-align:center;padding:3rem;color:var(--muted);font-style:italic}
</style>
</head>
<body>
<nav>
  <span class="brand">University_Of_O</span>
  {% if session.user_id %}
    <a href="{{ url_for('dashboard') }}">Dashboard</a>
    <a href="{{ url_for('users') }}">Users</a>
    <a href="{{ url_for('students') }}">Students</a>
    <a href="{{ url_for('lecturers') }}">Lecturers</a>
    <a href="{{ url_for('courses') }}">Courses</a>
    <a href="{{ url_for('faculties') }}">Faculties</a>
    <a href="{{ url_for('departments') }}">Departments</a>
    <a href="{{ url_for('logout') }}" style="margin-left:auto;color:var(--rust);opacity:1">Logout</a>
  {% endif %}
</nav>
<div class="container">
  {% with msgs = get_flashed_messages(with_categories=true) %}
    {% for cat,msg in msgs %}
      <div class="alert alert-{{ cat }}">{{ msg }}</div>
    {% endfor %}
  {% endwith %}
  {% block content %}{% endblock %}
</div>
</body>
</html>
"""

def render(template_str, **ctx):
    """Wrap a page fragment inside BASE."""
    full = BASE.replace("{% block title %}{% endblock %}", "{{ _title }}")
    full = full.replace("{% block content %}{% endblock %}", template_str)
    return render_template_string(full, **ctx)

def db():
    conn = get_db()
    cur = conn.cursor()
    return conn, cur

@app.route("/setup", methods=["GET", "POST"])
def setup():
    # TEMPORARILY COMMENTED OUT:
    # cur.execute("SELECT COUNT(*) AS n FROM user")
    # count = cur.fetchone()["n"]
    # if count > 0:
    #     return redirect(url_for("login"))
    if request.method == "POST":
        f = request.form
        pw = generate_password_hash(f["password"])
        cur.execute("""INSERT INTO user(user_name,full_name,cell,email,address,password)
                       VALUES(%s,%s,%s,%s,%s,%s)""",
                    (f["user_name"], f["full_name"], f["cell"], f["email"], f["address"], pw))
        conn.commit()
        flash("Admin user created — please sign in", "success")
        return redirect(url_for("login"))
    return render("""
    <div style="max-width:480px;margin:4rem auto">
      <div class="card">
        <h2 style="text-align:center;margin-bottom:.5rem">Initial Setup</h2>
        <p style="text-align:center;color:var(--muted);font-size:.88rem;margin-bottom:1.5rem">
          Create the first admin account. This page is disabled once a user exists.
        </p>
        <form method="POST">
          <div class="grid-2">
            <div><label>Username</label><input name="user_name" required></div>
            <div><label>Full Name</label><input name="full_name" required></div>
            <div><label>Email</label><input name="email" type="email" required></div>
            <div><label>Cell</label><input name="cell"></div>
          </div>
          <label>Address</label><textarea name="address" rows="2"></textarea>
          <label>Password</label><input name="password" type="password" required>
          <button class="btn btn-gold" style="width:100%">Create Admin User</button>
        </form>
      </div>
    </div>
    """, _title="Setup")
# ── AUTH ────────────────────────────────────────────────────
@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        conn, cur = db()
        cur.execute("SELECT * FROM user WHERE email=%s", (request.form["email"],))
        user = cur.fetchone()
        if user and check_password_hash(user["password"], request.form["password"]):
            session["user_id"]   = user["id"]
            session["user_name"] = user["user_name"]
            session["full_name"] = user["full_name"]
            return redirect(url_for("dashboard"))
        flash("Invalid credentials", "error")
    return render("""
    <div style="max-width:400px;margin:4rem auto">
      <div class="card">
        <h2 style="text-align:center;margin-bottom:1.5rem">Sign In</h2>
        <form method="POST">
          <label>Email</label><input name="email" type="email" required>
          <label>Password</label><input name="password" type="password" required>
          <button class="btn btn-primary" style="width:100%">Sign In</button>
        </form>
      </div>
    </div>
    """, _title="Login")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("user_id"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

# ── DASHBOARD ───────────────────────────────────────────────
@app.route("/dashboard")
@login_required
def dashboard():
    conn, cur = db()
    cur.execute("SELECT COUNT(*) AS n FROM user")
    u = cur.fetchone()["n"]
    cur.execute("SELECT COUNT(*) AS n FROM student")
    s = cur.fetchone()["n"]
    cur.execute("SELECT COUNT(*) AS n FROM lecturer")
    l = cur.fetchone()["n"]
    cur.execute("SELECT COUNT(*) AS n FROM course")
    c = cur.fetchone()["n"]
    cur.execute("SELECT COUNT(*) AS n FROM faculty")
    f = cur.fetchone()["n"]
    cur.execute("SELECT COUNT(*) AS n FROM dept")
    d = cur.fetchone()["n"]
    return render("""
    <h1>Dashboard</h1>
    <p style="color:var(--muted);margin-top:-.5rem;margin-bottom:1.5rem">
      Welcome back, <strong>{{ session.full_name }}</strong>
    </p>
    <div class="stat-grid">
      <div class="stat"><div class="stat-num">{{u}}</div><div class="stat-lbl">Users</div></div>
      <div class="stat"><div class="stat-num">{{s}}</div><div class="stat-lbl">Students</div></div>
      <div class="stat"><div class="stat-num">{{l}}</div><div class="stat-lbl">Lecturers</div></div>
      <div class="stat"><div class="stat-num">{{c}}</div><div class="stat-lbl">Courses</div></div>
      <div class="stat"><div class="stat-num">{{f}}</div><div class="stat-lbl">Faculties</div></div>
      <div class="stat"><div class="stat-num">{{d}}</div><div class="stat-lbl">Departments</div></div>
    </div>
    """, _title="Dashboard", u=u, s=s, l=l, c=c, f=f, d=d)

# ── USERS ────────────────────────────────────────────────────
@app.route("/users")
@login_required
def users():
    conn, cur = db()
    cur.execute("SELECT id,user_name,full_name,email,cell FROM user ORDER BY id")
    rows = cur.fetchall()
    return render("""
    <div class="page-header">
      <h1>Users</h1>
      <a href="{{ url_for('add_user') }}" class="btn btn-gold">+ Add User</a>
    </div>
    <div class="card" style="padding:0">
    <table>
      <tr><th>#</th><th>Username</th><th>Full Name</th><th>Email</th><th>Cell</th><th></th></tr>
      {% for r in rows %}
      <tr>
        <td>{{r.id}}</td><td>{{r.user_name}}</td><td>{{r.full_name}}</td>
        <td>{{r.email}}</td><td>{{r.cell}}</td>
        <td>
          <a href="{{ url_for('edit_user', uid=r.id) }}" class="btn btn-sm btn-primary">Edit</a>
          <a href="{{ url_for('delete_user', uid=r.id) }}" class="btn btn-sm btn-danger"
             onclick="return confirm('Delete this user?')">Del</a>
        </td>
      </tr>
      {% else %}<tr><td colspan="6" class="empty">No users found</td></tr>
      {% endfor %}
    </table></div>
    """, _title="Users", rows=rows)

@app.route("/users/add", methods=["GET","POST"])
@login_required
def add_user():
    if request.method == "POST":
        f = request.form
        pw = generate_password_hash(f["password"])
        conn, cur = db()
        cur.execute("""INSERT INTO user(user_name,full_name,cell,email,address,password)
                       VALUES(%s,%s,%s,%s,%s,%s)""",
                    (f["user_name"],f["full_name"],f["cell"],f["email"],f["address"],pw))
        conn.commit()
        flash("User created successfully", "success")
        return redirect(url_for("users"))
    return render("""
    <h1>Add User</h1>
    <div class="card">
      <form method="POST">
        <div class="grid-2">
          <div><label>Username</label><input name="user_name" required></div>
          <div><label>Full Name</label><input name="full_name" required></div>
          <div><label>Email</label><input name="email" type="email" required></div>
          <div><label>Cell</label><input name="cell"></div>
        </div>
        <label>Address</label><textarea name="address" rows="2"></textarea>
        <label>Password</label><input name="password" type="password" required>
        <button class="btn btn-gold">Create User</button>
        <a href="{{ url_for('users') }}" class="btn btn-primary" style="margin-left:.5rem">Cancel</a>
      </form>
    </div>
    """, _title="Add User")

@app.route("/users/edit/<int:uid>", methods=["GET","POST"])
@login_required
def edit_user(uid):
    conn, cur = db()
    if request.method == "POST":
        f = request.form
        cur.execute("""UPDATE user SET user_name=%s,full_name=%s,cell=%s,email=%s,address=%s
                       WHERE id=%s""",
                    (f["user_name"],f["full_name"],f["cell"],f["email"],f["address"],uid))
        conn.commit()
        flash("User updated", "success")
        return redirect(url_for("users"))
    cur.execute("SELECT * FROM user WHERE id=%s", (uid,))
    u = cur.fetchone()
    return render("""
    <h1>Edit User #{{u.id}}</h1>
    <div class="card">
      <form method="POST">
        <div class="grid-2">
          <div><label>Username</label><input name="user_name" value="{{u.user_name}}" required></div>
          <div><label>Full Name</label><input name="full_name" value="{{u.full_name}}" required></div>
          <div><label>Email</label><input name="email" type="email" value="{{u.email}}" required></div>
          <div><label>Cell</label><input name="cell" value="{{u.cell or ''}}"></div>
        </div>
        <label>Address</label><textarea name="address" rows="2">{{u.address or ''}}</textarea>
        <button class="btn btn-gold">Save Changes</button>
        <a href="{{ url_for('users') }}" class="btn btn-primary" style="margin-left:.5rem">Cancel</a>
      </form>
    </div>
    """, _title="Edit User", u=u)

@app.route("/users/delete/<int:uid>")
@login_required
def delete_user(uid):
    conn, cur = db()
    cur.execute("DELETE FROM user WHERE id=%s", (uid,))
    conn.commit()
    flash("User deleted", "success")
    return redirect(url_for("users"))

# ── STUDENTS ─────────────────────────────────────────────────
@app.route("/students")
@login_required
def students():
    conn, cur = db()
    cur.execute("""
        SELECT s.id, u.full_name, u.email, s.reg_no, dp.deg_name
        FROM student s
        JOIN user u ON u.id=s.user_id
        JOIN degree_program dp ON dp.id=s.programme_id
        ORDER BY s.id
    """)
    rows = cur.fetchall()
    return render("""
    <div class="page-header"><h1>Students</h1>
      <a href="{{ url_for('add_student') }}" class="btn btn-gold">+ Enroll Student</a>
    </div>
    <div class="card" style="padding:0"><table>
      <tr><th>#</th><th>Name</th><th>Email</th><th>Reg No</th><th>Programme</th></tr>
      {% for r in rows %}
      <tr><td>{{r.id}}</td><td>{{r.full_name}}</td><td>{{r.email}}</td>
          <td><span class="badge badge-gold">{{r.reg_no}}</span></td><td>{{r.deg_name}}</td></tr>
      {% else %}<tr><td colspan="5" class="empty">No students enrolled</td></tr>
      {% endfor %}
    </table></div>
    """, _title="Students", rows=rows)

@app.route("/students/add", methods=["GET","POST"])
@login_required
def add_student():
    conn, cur = db()
    if request.method == "POST":
        f = request.form
        cur.execute("INSERT INTO student(user_id,reg_no,programme_id) VALUES(%s,%s,%s)",
                    (f["user_id"], f["reg_no"], f["programme_id"]))
        conn.commit()
        flash("Student enrolled", "success")
        return redirect(url_for("students"))
    cur.execute("SELECT id,full_name FROM user ORDER BY full_name")
    users_ = cur.fetchall()
    cur.execute("SELECT id,deg_name FROM degree_program ORDER BY deg_name")
    progs = cur.fetchall()
    return render("""
    <h1>Enroll Student</h1>
    <div class="card"><form method="POST">
      <label>User</label>
      <select name="user_id" required>
        {% for u in users_ %}<option value="{{u.id}}">{{u.full_name}}</option>{% endfor %}
      </select>
      <label>Registration Number</label><input name="reg_no" required>
      <label>Programme</label>
      <select name="programme_id" required>
        {% for p in progs %}<option value="{{p.id}}">{{p.deg_name}}</option>{% endfor %}
      </select>
      <button class="btn btn-gold">Enroll</button>
      <a href="{{ url_for('students') }}" class="btn btn-primary" style="margin-left:.5rem">Cancel</a>
    </form></div>
    """, _title="Enroll Student", users_=users_, progs=progs)

# ── LECTURERS ────────────────────────────────────────────────
@app.route("/lecturers")
@login_required
def lecturers():
    conn, cur = db()
    cur.execute("""
        SELECT l.id, u.full_name, u.email, f.faculty_name
        FROM lecturer l
        JOIN user u    ON u.id=l.user_id
        JOIN faculty f ON f.id=l.faculty_id
        ORDER BY l.id
    """)
    rows = cur.fetchall()
    return render("""
    <div class="page-header"><h1>Lecturers</h1>
      <a href="{{ url_for('add_lecturer') }}" class="btn btn-gold">+ Add Lecturer</a>
    </div>
    <div class="card" style="padding:0"><table>
      <tr><th>#</th><th>Name</th><th>Email</th><th>Faculty</th></tr>
      {% for r in rows %}
      <tr><td>{{r.id}}</td><td>{{r.full_name}}</td><td>{{r.email}}</td>
          <td><span class="badge badge-green">{{r.faculty_name}}</span></td></tr>
      {% else %}<tr><td colspan="4" class="empty">No lecturers</td></tr>
      {% endfor %}
    </table></div>
    """, _title="Lecturers", rows=rows)

@app.route("/lecturers/add", methods=["GET","POST"])
@login_required
def add_lecturer():
    conn, cur = db()
    if request.method == "POST":
        f = request.form
        cur.execute("INSERT INTO lecturer(user_id,faculty_id) VALUES(%s,%s)",
                    (f["user_id"], f["faculty_id"]))
        conn.commit()
        flash("Lecturer added", "success")
        return redirect(url_for("lecturers"))
    cur.execute("SELECT id,full_name FROM user ORDER BY full_name")
    users_ = cur.fetchall()
    cur.execute("SELECT id,faculty_name FROM faculty ORDER BY faculty_name")
    facs = cur.fetchall()
    return render("""
    <h1>Add Lecturer</h1>
    <div class="card"><form method="POST">
      <label>User</label>
      <select name="user_id" required>
        {% for u in users_ %}<option value="{{u.id}}">{{u.full_name}}</option>{% endfor %}
      </select>
      <label>Faculty</label>
      <select name="faculty_id" required>
        {% for f in facs %}<option value="{{f.id}}">{{f.faculty_name}}</option>{% endfor %}
      </select>
      <button class="btn btn-gold">Add Lecturer</button>
      <a href="{{ url_for('lecturers') }}" class="btn btn-primary" style="margin-left:.5rem">Cancel</a>
    </form></div>
    """, _title="Add Lecturer", users_=users_, facs=facs)

# ── COURSES ──────────────────────────────────────────────────
@app.route("/courses")
@login_required
def courses():
    conn, cur = db()
    cur.execute("""
        SELECT c.id, c.course_name, c.course_desc, f.faculty_name,
               COUNT(DISTINCT e.student_id) AS enrolled,
               COUNT(DISTINCT cl.lecturer_id) AS lecturers
        FROM course c
        JOIN faculty f ON f.id=c.faculty_id
        LEFT JOIN enrollment e ON e.course_id=c.id
        LEFT JOIN course_lecturer cl ON cl.course_id=c.id
        GROUP BY c.id
        ORDER BY c.id
    """)
    rows = cur.fetchall()
    return render("""
    <div class="page-header"><h1>Courses</h1>
      <a href="{{ url_for('add_course') }}" class="btn btn-gold">+ Add Course</a>
    </div>
    <div class="card" style="padding:0"><table>
      <tr><th>#</th><th>Course Name</th><th>Faculty</th><th>Students</th><th>Lecturers</th></tr>
      {% for r in rows %}
      <tr>
        <td>{{r.id}}</td>
        <td><strong>{{r.course_name}}</strong><br><small style="color:var(--muted)">{{r.course_desc or ''}}</small></td>
        <td>{{r.faculty_name}}</td>
        <td><span class="badge badge-gold">{{r.enrolled}}</span></td>
        <td><span class="badge badge-green">{{r.lecturers}}</span></td>
      </tr>
      {% else %}<tr><td colspan="5" class="empty">No courses</td></tr>
      {% endfor %}
    </table></div>
    """, _title="Courses", rows=rows)

@app.route("/courses/add", methods=["GET","POST"])
@login_required
def add_course():
    conn, cur = db()
    if request.method == "POST":
        f = request.form
        cur.execute("INSERT INTO course(course_name,course_desc,faculty_id) VALUES(%s,%s,%s)",
                    (f["course_name"], f["course_desc"], f["faculty_id"]))
        conn.commit()
        flash("Course added", "success")
        return redirect(url_for("courses"))
    cur.execute("SELECT id,faculty_name FROM faculty ORDER BY faculty_name")
    facs = cur.fetchall()
    return render("""
    <h1>Add Course</h1>
    <div class="card"><form method="POST">
      <label>Course Name</label><input name="course_name" required>
      <label>Description</label><textarea name="course_desc" rows="3"></textarea>
      <label>Faculty</label>
      <select name="faculty_id" required>
        {% for f in facs %}<option value="{{f.id}}">{{f.faculty_name}}</option>{% endfor %}
      </select>
      <button class="btn btn-gold">Add Course</button>
      <a href="{{ url_for('courses') }}" class="btn btn-primary" style="margin-left:.5rem">Cancel</a>
    </form></div>
    """, _title="Add Course", facs=facs)

# ── FACULTIES ────────────────────────────────────────────────
@app.route("/faculties")
@login_required
def faculties():
    conn, cur = db()
    cur.execute("SELECT * FROM faculty ORDER BY id")
    rows = cur.fetchall()
    return render("""
    <div class="page-header"><h1>Faculties</h1>
      <a href="{{ url_for('add_faculty') }}" class="btn btn-gold">+ Add Faculty</a>
    </div>
    <div class="card" style="padding:0"><table>
      <tr><th>#</th><th>Name</th><th>Description</th></tr>
      {% for r in rows %}
      <tr><td>{{r.id}}</td><td>{{r.faculty_name}}</td><td>{{r.faculty_desc or ''}}</td></tr>
      {% else %}<tr><td colspan="3" class="empty">No faculties</td></tr>
      {% endfor %}
    </table></div>
    """, _title="Faculties", rows=rows)

@app.route("/faculties/add", methods=["GET","POST"])
@login_required
def add_faculty():
    if request.method == "POST":
        f = request.form
        conn, cur = db()
        cur.execute("INSERT INTO faculty(faculty_name,faculty_desc) VALUES(%s,%s)",
                    (f["faculty_name"], f["faculty_desc"]))
        conn.commit()
        flash("Faculty added", "success")
        return redirect(url_for("faculties"))
    return render("""
    <h1>Add Faculty</h1>
    <div class="card"><form method="POST">
      <label>Faculty Name</label><input name="faculty_name" required>
      <label>Description</label><textarea name="faculty_desc" rows="3"></textarea>
      <button class="btn btn-gold">Add Faculty</button>
      <a href="{{ url_for('faculties') }}" class="btn btn-primary" style="margin-left:.5rem">Cancel</a>
    </form></div>
    """, _title="Add Faculty")

# ── DEPARTMENTS ──────────────────────────────────────────────
@app.route("/departments")
@login_required
def departments():
    conn, cur = db()
    cur.execute("SELECT * FROM dept ORDER BY id")
    rows = cur.fetchall()
    return render("""
    <div class="page-header"><h1>Departments</h1>
      <a href="{{ url_for('add_dept') }}" class="btn btn-gold">+ Add Department</a>
    </div>
    <div class="card" style="padding:0"><table>
      <tr><th>#</th><th>Name</th><th>Description</th></tr>
      {% for r in rows %}
      <tr><td>{{r.id}}</td><td>{{r.dept_name}}</td><td>{{r.dept_desc or ''}}</td></tr>
      {% else %}<tr><td colspan="3" class="empty">No departments</td></tr>
      {% endfor %}
    </table></div>
    """, _title="Departments", rows=rows)

@app.route("/departments/add", methods=["GET","POST"])
@login_required
def add_dept():
    if request.method == "POST":
        f = request.form
        conn, cur = db()
        cur.execute("INSERT INTO dept(dept_name,dept_desc) VALUES(%s,%s)",
                    (f["dept_name"], f["dept_desc"]))
        conn.commit()
        flash("Department added", "success")
        return redirect(url_for("departments"))
    return render("""
    <h1>Add Department</h1>
    <div class="card"><form method="POST">
      <label>Department Name</label><input name="dept_name" required>
      <label>Description</label><textarea name="dept_desc" rows="3"></textarea>
      <button class="btn btn-gold">Add Department</button>
      <a href="{{ url_for('departments') }}" class="btn btn-primary" style="margin-left:.5rem">Cancel</a>
    </form></div>
    """, _title="Add Department")

# ── ENTRY POINT ──────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)



