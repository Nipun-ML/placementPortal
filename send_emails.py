from flask import Flask,render_template
from flask_mail import Mail, Message

def send_mail(app):
          mail = Mail(app)
          msg = Message('Hello', sender = 'suradkarknipun@gmail.com', recipients = ['nipunrocks7@gmail.com'])
          msg.body = "Hello Flask message sent from Flask-Mail"
          args="student_signup"
          msg.html=render_template("msg.html",args=args)
          mail.send(msg)
def tpo(app,name,criteria,ctc,no,email,computer,mechanical,electronics):
         mail = Mail(app)
         computer     = "Computer" if computer=='Computer' else ""
         mechanical  = "Mechanical" if mechanical=='Mechanical' else ""
         electronics = "Electronics" if electronics=='Electronics' else ""
         args="student_signup"
         msg = Message('Company %s Has Requested A Time Slot'%(name), sender = 'suradkarknipun@gmail.com', recipients = ['tpoplacementportal@gmail.com'],
         html = "Hello Tpo sir,<br> Company %s is interested for placement in our campus and is offering %s lakhs as CTC for students with\
         students having Pointer above %s and is interested in branches: %s %s %s. <br> \
         The email address of the SPOC for the company is %s and his/her contact number is %s. <br> \
         <a href=\"http://127.0.0.1:5000/%s/give_slot\"> CLICK HERE TO ALLOT TIME TO THIS COMPANY </a>"%(name,ctc,criteria,computer,mechanical,electronics,email,no,name)
         )
         mail.send(msg)

def students(app,students,company):
        mail = Mail(app)
        with mail.connect() as conn:
            for student in students:
                print(student.get('name'))
                message = 'Hello %s,<br>The TPO wants to inform you that since you have a pointer greater than %d you are eligbile to \
                 sit for the %s test. The Test for the company is going to be held on %s.\
                <br> if you wish to sit for the company please click on the link below your information(as in placment portal) would \
                be automatically sent to the company<br> <a href=\"http://127.0.0.1:5000/%d/%s/entry\">CLICK HERE TO APPLY</a>' %(student.get('name'),
                company.get('criteria'),company.get('company'),company.get('start_date'),student.get('id'),company.get('company'))
                
                subject = "Congratulations, %s you are eligible to sit for %s" %(student.get("name"),company.get("company"))
                msg = Message(recipients=[student.get("email")], 
                    html=message,
                    sender = 'suradkarknipun@gmail.com',
                    subject=subject)

                conn.send(msg)