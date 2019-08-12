from flask import Flask,render_template, request,redirect
from cs50 import SQL


app = Flask(__name__)
db = SQL("sqlite:///placement_portal.db")
@app.route('/')
def index():
    return render_template("login.html")

@app.route('/check',methods=['post'])
def check():
    id_ = request.form.get('Id')
    password = request.form.get('password')
    rows = db.execute("Select * from students where id =:id and password = :password",id=id_,password=password)
    if len(rows) == 1 :
        return render_template("success.html")
    else:
        return render_template('failure.html')

@app.route('/student_signup',methods=['get'])
def student_signup():
    return render_template("student_signup.html")

@app.route('/company_signup',methods=['get'])
def company_signup():
    return render_template("company_signup.html")

@app.route('/display_list',methods=['post'])
def display_list():
    criteria = request.form.get('criteria')
    eligible = db.execute("Select name,email,cgpa from students where cgpa>=:criteria",criteria=criteria)
    return render_template("display_eligible_list.html",eligible=eligible)

@app.route('/db_put',methods=['post'])
def db_put():
    id_ = request.form.get("id")
    password = request.form.get("password")
    name = request.form.get("name")
    email = request.form.get("email")
    branch = request.form.get("branch")
    cgpa   = request.form.get("cgpa")
    result = db.execute("INSERT INTO 'students' (id,password,name,email,branch,cgpa) values(:id_,:password,:name,:email,:branch,:cgpa)",id_=id_,
    password=password,name=name,email=email,branch=branch,cgpa=cgpa)
    return redirect("/")