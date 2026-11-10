import sys
sys.path.insert(0,'db/')
from dbhelper import getAll,getRecord,deleteRecord,addRecord,updateRecord
from bcrypt import gensalt,checkpw,hashpw
import re
from flask import Flask, Response, render_template,redirect,session,request,flash,url_for

app:Flask = Flask(__name__)
app.secret_key = 'c6dff56e-9d95-403b-83a8-5fe2ba619b7f'

salt = gensalt()

@app.after_request
def app_header(response):
    response.headers["Cache-Control"] = "no-cache,must-revalidate,no-store"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route('/main')
def main():
    if 'email' not in session:
        return redirect(url_for('index'))
    students = getAll('students')
    return render_template('main.html',students=students)
    

@app.route('/')
def index():
    if 'email' in session:
        return redirect(url_for('main'))
    else:
        return render_template('index.html')

@app.route("/login",methods=['POST'])
def login():

    if 'email' in session:
        return redirect(url_for('main'))
    
    email = request.form['email']
    password = request.form['password']
    
    bpass:bytes = bytes(password,encoding='utf-8')
    
    user = getRecord('users', email=email)
    print(user)
    if len(user) > 0 and checkpw(bpass,user[0][2]):
        session['email'] = email
        flash(f'Logged In! Welcome {user[0][3]}','success')
        return redirect(url_for('main'))
    else: 
        flash("Wrong Email or Password","danger")
        return redirect(url_for('index'))
    
@app.route("/logout")
def logout():
    session.pop('email',None)
    session.clear()
    flash('Logged Out','success')
    return redirect(url_for('index'))
    
@app.route('/delete')
def delete():

    idno = request.args.get('idno')
    ok = deleteRecord('students',idno=idno)
    if ok:
        flash(f"Student {idno} deleted successfully", 'success')
    else:
        flash(f"Student {idno} not deleted", 'danger')
    return redirect(url_for('main'))

@app.route("/updatestudent")
def updatestudent():
    
    if 'email' not in session:
        return redirect('index')
    
    idno = request.args.get('idno')
    students = getRecord('students',idno=idno)
    return render_template('update.html',students=students)
    
@app.route('/add',methods=['POST'])
def add():
    idno = request.form.get('idno')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    course = request.form.get('course')
    level = request.form.get('level')
    
    ok = addRecord('students',idno=idno,first_name=first_name,last_name=last_name,course=course,level=level)
    if ok:
        flash(f'Student [{idno}] successfully created','success')
    else:
        flash(f'Student [{idno}] cannot be created','danger')
    return redirect(url_for('main'))

@app.route('/update', methods=['POST'])
def update():
    idno = request.form.get('idno')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    course = request.form.get('course')
    level = request.form.get('level')
    
    ok = updateRecord('students',idno=idno,first_name=first_name,last_name=last_name,course=course,level=level)
    if ok:
        flash(f"Student [{idno}] successfully updated", 'success')
    else:
        flash(f'Student [{idno}] cannot be updated','danger')
    return redirect(url_for('main'))


@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route("/register",methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    confirmpassword = request.form['confirmfield']
    
    if not validatepass(password):
        flash('Password should have at least 1 uppercase, 1 lowercase, 1 special character or digit, and at least 8 characters in length', 'warning')
        return redirect(url_for('signup'))

    if password != confirmpassword:
        flash('Passwords do not match', 'warning')
        return redirect(url_for('signup'))
    
    password = hashedpass(password)
    
    ok = addRecord('users',email=email,password=password,username=username)
    if ok:
        flash('User Created successfully', 'success')
        return redirect(url_for('index'))
    else:
        flash('User cannot be created','danger')
        return redirect(url_for('signup'))
    
def hashedpass(password:str):
    pw = bytes(password, encoding='UTF-8')
    return hashpw(pw, salt)

def validatepass(password):
    passregex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,20}$"
    if re.fullmatch(passregex, password):
        return True
    return False 

if __name__=="__main__":
    app.run(debug=True)