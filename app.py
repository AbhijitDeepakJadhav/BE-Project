from flask import Flask, render_template,redirect,url_for,request
import pymysql
import os
from os.path import join, dirname, realpath
from werkzeug.utils import secure_filename

connection = pymysql.connect(host="be-project-database-1.chcsrix3zvtg.ap-south-1.rds.amazonaws.com",user="vrunda",password="vrunda1527",db="BE_Project")
cursor = connection.cursor()

app = Flask(__name__)

addressimg = join(dirname(realpath(__file__)), 'static/uploads/images')
app.config['addressimg'] = addressimg

addresspdf = join(dirname(realpath(__file__)), 'static/uploads/pdfs')
app.config['addresspdf'] = addresspdf

loginstat = False
dashdata = {}
Name=""
Loginid=""
profadd="../static/uploads/images/"+Name+"."+"jpg"
certadd="../static/uploads/pdfs/"+Name+"."+"pdf"




@app.route('/')
def index():
    return render_template('index.html',**{'LOGIN':'LOGIN'})

@app.route('/home')
def home():
    if(loginstat):
        return render_template('index.html',**{'LOGIN':Name})
    else:
        return render_template('index.html',**{'LOGIN':'LOGIN'})

@app.route('/Dashboard')
def dashboard():
    if(loginstat):
        return render_template('userDashboard.html',**dashdata)
    else:
        return render_template('index.html',**{'LOGIN':'LOGIN'})

@app.route('/',methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        idpass = request.form
        loginid = idpass['loginid']
        password = idpass['password']
        cursor.execute("select Email, password from rfiduserdata where Email=%s and password=%s",(loginid,password))
        data = cursor.fetchall()
        if (len(data)==1):
            global loginstat,Loginid,Name,profadd,certadd
            loginstat = True
            Loginid=loginid
            cursor.execute("select * from rfiduserdata where Email=%s",(loginid))
            data = cursor.fetchall()
            Name=data[0][1]
            cursor.execute("select EntryCount,ExitCount from inoutcount where Email=%s",(loginid))
            data2 = cursor.fetchall()
            cursor.execute("select SR_NO,Date,Time,Inout_Status from userinout where Email=%s",(loginid))
            data3 = cursor.fetchall()
            cursor.execute("select Name,Sname from rfiduserdata where flat_no=%s",(data[0][6]))
            data4 = cursor.fetchall()
            profadd="../static/uploads/images/"+Name+"."+"jpg"
            certadd="../static/uploads/pdfs/"+Name+"."+"pdf"
            global dashdata
            dashdata={
                'fullname':data4,
                'email':data[0][4],
                'phone':data[0][5],
                'flatno':data[0][6],
                'regdate':data[0][7],
                'DOB':data[0][8],
                'vaccStatus':data[0][10],
                'flineworker':data[0][11],
                'incount':data2[0][0],
                'outcount':data2[0][1],
                'value': data3,
                'profileaddress':profadd,
                'certaddress':certadd
            }
            print(certadd)
            return render_template('userDashboard.html',**dashdata)
        else:
            return redirect(url_for('index'))

@app.route('/profile-submitted', methods=['GET','POST'])
def editprof():
    if request.method =='POST':
        file = request.files['profile']
        if file:
            file.filename = Name+"."+"jpg"
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['addressimg'],filename))
    return render_template('userDashboard.html',**dashdata)

@app.route('/cert-submitted', methods=['GET','POST'])
def editcert():
    if request.method =='POST':
        file = request.files['cert']
        if file:
            file.filename = Name+"."+"pdf"
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['addresspdf'],filename))
    return render_template('userDashboard.html',**dashdata)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=3000,debug=True)