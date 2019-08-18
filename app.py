from flask import Flask,render_template, request,redirect
from cs50 import SQL
from flask_mail import Mail, Message
import send_emails
import googlesheets

app = Flask(__name__)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'suradkarknipun@gmail.com'
app.config['MAIL_PASSWORD'] = 'NipuN@123'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
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
          send_emails.send_mail(app)
          return render_template("success.html")
    else:
        return render_template('failure.html')

@app.route('/student_signup',methods=['get'])
def student_signup():
    return render_template("student_signup.html")

@app.route('/company_signup',methods=['get'])
def company_signup():
    return render_template("company_signup.html")

@app.route('/<comp_name>/give_slot',methods=['get'])
def give_slot(comp_name):
    return render_template("slot_booking.html",comp_name=comp_name)


@app.route('/time_slot',methods=['post']) 
def time_slot():
    company_name = request.form.get('company_name')
    criteria     = request.form.get('elg_criteria')
    ctc          = request.form.get('ctc')
    contact_no   = request.form.get('contact_no')
    contact_email = request.form.get('contact_email')
    computer      = request.form.get('computer')
    mechanical    = request.form.get('mechanical')
    electronics   = request.form.get('electronics')
    iscomputer    = True if computer=='Computer' else False
    ismechanical  = True if mechanical=='Mechanical' else False
    iselectronics = True if electronics=='Electronics' else False
    result = db.execute("INSERT INTO 'companies' (company,criteria,ctc,number,email,computer,mechanical,electronics) values(:name,:criteria,:ctc,:no,:email,:computer,:mechanical,:electronics)"
    ,name=company_name,criteria=criteria,ctc=ctc,no=contact_no,email=contact_email,computer=iscomputer,mechanical=ismechanical,electronics=iselectronics)
    send_emails.tpo(app,company_name,criteria,ctc,contact_no,contact_email,computer,mechanical,electronics)
    return "We have Successfully received your data.The TPO would get back to you as soon as possible"
'''
@app.route('/display_list',methods=['post'])
def display_list():
    criteria = request.form.get('criteria')
    eligible = db.execute("Select name,email,cgpa from students where cgpa>=:criteria",criteria=criteria)
    return render_template("display_eligible_list.html",eligible=eligible)
'''
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

@app.route('/<comp_name>/notify',methods=["post"])
def notify(comp_name):
    deadline = request.form.get('deadline')
    startdate = request.form.get('start-date')
    enddate   = request.form.get('end-date')
    update = db.execute("update companies set deadline=:deadline,start_date=:start_date,end_date=:end_date  where company=:name",name=comp_name,
    deadline = deadline,start_date=startdate,end_date=enddate)
    info_criteria = db.execute("Select * from companies where company=:name",name=comp_name)
    entry = info_criteria[0]
    branch_list=[]
    if entry.get("computer")==1:
        branch_list.append("Computers")
    if entry.get("mechanical")==1:
        branch_list.append("Mechanical")
    if entry.get("electronics")==1:
        branch_list.append("Electronics")
    eligible_students = db.execute("select id,name,email,branch,cgpa from students where cgpa>=:criteria and branch in (:branch_list)",branch_list=branch_list,criteria=entry.get("criteria"))
    send_emails.students(app,eligible_students,entry)
    return "ALL THE ELIGIBLE STUDENTS WHERE INFORMED"

@app.route('/<id_>/<comp_name>/entry',methods=['get'])
def google_sheet(id_,comp_name):
     applied = db.execute("select id,name,email,branch,cgpa from students where id=:id",id=id_)
     print(len(applied))
     comp_info = db.execute("select company,email from companies where company=:company",company=comp_name)
     googlesheets.make_entry(applied[0],comp_info[0])
     return "Success"