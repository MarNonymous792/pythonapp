import sys
sys.path.insert(0,'db/')
from dbhelper import getAll,getRecord,deleteRecord,addRecord,updateRecord

from flask import Flask, Response, render_template,redirect,session,request,flash,url_for

app:Flask = Flask(__name__)
app.secret_key = 'c6dff56e-9d95-403b-83a8-5fe2ba619b7f'

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
    
    email = request.form.get('email')
    password = request.form.get('password')
    
    user = getRecord('users', email=email,password=password)
    if len(user) > 0:
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
    
if __name__=="__main__":
    app.run(debug=True)