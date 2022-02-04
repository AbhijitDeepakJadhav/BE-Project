from flask import Flask, render_template, redirect, url_for,request,flash
import flask
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import webbrowser
import pymysql
import datetime
import time

connection = pymysql.connect(host="be-project-database-1.chcsrix3zvtg.ap-south-1.rds.amazonaws.com",user="vrunda",password="vrunda1527",db="BE_Project")
cursor = connection.cursor()

reader = SimpleMFRC522()
app = Flask(__name__)
app.secret_key = '_5#y2L"F4Q8z\n\xec]/'

@app.route('/register-new-member', methods=['GET','POST'])
def Registeruser():
	#For Registration
	insertqr = "insert into rfiduserdata(`Tagid`,`Name`, `Mname`, `Sname`,`Email`,`phone_no`,`flat_no`,`reg_date`,`dob`,`password`,`vaccination`,`frontline`)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	insertuioc = "insert into inoutcount(`Tagid`, `EntryCount`, `ExitCount`,`inmonth`,`reset`,`Email`)values(%s,%s,%s,%s,%s,%s)"
	if request.method == 'POST':
		details=request.form
		name = details['Fname']
		Mname = details['Mname']
		Sname = details['Sname']
		Email = details['Email']
		Phonenum = details['Phonenum']
		Flatnum = details['Flatnum']
		Regdate = details['Regdate']
		DOB = details['DOB']
		Password = details['Password']
		vaccine = details['vaccine']
		frontline = details['frontline']
		print("Now scan the User's RFID Tag that is to be registered")
		print("Waiting.....")
		try:
			id,text=reader.read()
			# id = input()
			# print(id)
			reader.write(name+" "+Mname+" "+Sname)
		finally:
			GPIO.cleanup()
			flash("New Member Registered Successfully")
		cursor.execute(insertqr,(id,name,Mname,Sname,Email,Phonenum,Flatnum,Regdate,DOB,Password,vaccine,frontline))
		cursor.execute(insertuioc, (id,0,0,0,0,Email))
		connection.commit()
		print("User " + name+" "+Sname + " Registered succesfully")
		return redirect(url_for('index'))
	return render_template('register.html')

@app.route('/')
def index():
	insertrec = "insert into userinout(`Tagid`, `Date`, `Time`, `Inout_Status`,`Email`)values(%s,%s,%s,%s,%s)"
	updatentry = "update inoutcount set EntryCount=EntryCount+1,currentstat=%s where Tagid = %s"
	updatexit = "update inoutcount set ExitCount=ExitCount+1,currentstat=%s where Tagid = %s"
	try:
		print("Please Tap you card...")
		id,text=reader.read()
		# text="name"
		# id=(int)(input())
		print(id)
		if(id==386930524072):
			return redirect(url_for('Registeruser'))
		cursor.execute("Select count(Tagid) from rfiduserdata where Tagid = %s",id)
		count=(cursor.fetchall())[0][0]
		
		if(count==0):
			return render_template('index.html',**{'indentificationSts':"Unauthorized user"})
			
		dt = str(datetime.datetime.now())
		date = dt[0:10]
		tme = dt[11:19]
		cursor.execute("Select EntryCount, Email from inoutcount where Tagid = %s",id)
		info=(cursor.fetchall())
		count=info[0][0]
		Email = info[0][1]
		
		if(count==0):
			status="in"
		else:
			cursor.execute("Select currentstat from inoutcount where Tagid = %s",id)
			prevsts=(cursor.fetchall())[0][0]
			if(prevsts == 'in'):
				status = "out"
			else:
				status = "in"
		
		if(status=="out"):
			dt = str(datetime.datetime.now())
			onlydate = (int)(dt[8:10])
			
			cursor.execute("Select reset from inoutcount where Tagid = %s",id)
			rst=(cursor.fetchall())[0][0]
			if(onlydate == 28 and rst==0):
				cursor.execute("update inoutcount set inmonth=0 where tagid=%s",id)
				cursor.execute("update inoutcount set reset=1 where tagid=%s",id)
				connection.commit()
			else:
				if(onlydate == 29):
					cursor.execute("update inoutcount set reset=0 where tagid=%s",id)
					connection.commit()
			
			cursor.execute("Select inmonth from inoutcount where Tagid = %s",id)
			inmonth = cursor.fetchall()[0][0]
			if(inmonth<5):
				cursor.execute("update inoutcount set inmonth=inmonth+1 where tagid=%s",id)
				connection.commit()
			else:
				return render_template('index.html',**{'indentificationSts':"your outgoing count has been expired so you are not allowed to go out"})
		
		print(type(id))
		print(id)
		print(text)
		print(tme)
		print(date)
		print("Status = "+status) 
		
		data={
		  'name':text,
		  'Date':date,
		  'Time':tme,
		  'Sts' :status
			}
			
		cursor.execute(insertrec,(id,date,tme,status,Email))
		if(status == "in"):
			cursor.execute(updatentry,(status,id))
		else:
			cursor.execute(updatexit,(status,id))
		connection.commit()
		return render_template('index.html',**data)
	finally:
		# time.sleep(1)	
		GPIO.cleanup()
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=3000, debug=True)