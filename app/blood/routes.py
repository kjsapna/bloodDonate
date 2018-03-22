


# from flask import Flask,render_template, request, flash
# app = Flask(__name__)

from blood import app
from flask_mail import Message
from flask import render_template, request, flash,redirect,url_for,session
from model import PeopleProfile as p,UserModel as u,RecipientProfile as r,DonorProfile as d, DonorRecipient as o, bloodCategory as b
from . import db, mail
from itsdangerous import Signer, BadSignature
from sqlalchemy import func
# from model.PeopleProfile import PeopleProfile

@app.route('/')
def index():
	result = []
	profiles=db.engine.execute("select R.*,blood_type from tbl_bloodcategory bd JOIN tbl_recipient R ON bd.id=R.bloodCategoryId  WHERE status = 1 AND received = 0 AND DATEDIFF(CURDATE(),posted_date)<7 ")
	for row in profiles:
		result.append(row)
	print result

	newresult = []
	donor = db.engine.execute("select * from tbl_donor D")
	for row in donor:
		newresult.append(row)
	return render_template('index.html', results = result, newresult = newresult)

	# if name in session:
	# 	name = session['name']
	# 	return ('Logged in as' + name + '<br>' + "<b><a href="Logout">LOGOUT</a></b>")

	# return render_template('index.html')

@app.route('/home')
def home():
	return render_template('home.html')




@app.route('/admin')
def admin():
	return render_template('login.html')

@app.route('/user')
def user():
    return render_template('user_login.html')


@app.route('/admin/login',methods=['POST'])
def signin():

	if request.method == 'POST':
		email= request.form.get("email")
		password = request.form.get("password")


        user = u.User.query.filter_by(email=email).first()

        if user :
        	if user.password == password:
        		session['email'] = user.email
        		return redirect(url_for('dashboard'))

        	else:

        		flash("invlaid email or password")
        		return redirect(url_for('admin'))
        else:
        	flash("Invlaid email")
        	return redirect(url_for('admin'))

@app.route('/users')
def getAllUsers():
	userList=u.User.query.all()
	return render_template('user_list.html',userList=userList)

@app.route('/listProfile')
def listProfile():
	result = []
	profiles=db.engine.execute("select * from tbl_people_profile P inner join tbl_bloodcategory B on P.bloodCategoryId = B.id ")
	for row in profiles:
		result.append(row)
	print result
	return render_template('list_profile.html',results=result)


@app.route('/signout')
def signout():

  if 'email' not in session:
    return redirect(url_for('admin'))

  session.pop('email', None)
  return redirect(url_for('admin'))

# if __name__ == '__main__':
# 	app.run(debug=True
@app.route('/dashboard')
def dashboard():
	ar_history = []
	rhistory = db.engine.execute("select * from tbl_recipient R")
	for row in rhistory :
		ar_history.append(row)
		print(ar_history)

	d_history = []
	history = db.engine.execute("select r.*,rd.id,rd.posted_date from tbl_donor d JOIN tbl_recipient_donor rd ON d.id = rd.donor_id JOIN tbl_recipient r  ON r.id = rd.recipient_id")
	for row in history :
		d_history.append(row)
		print(d_history)

	if 'email' not in session:
		return redirect(url_for('admin'))
	user = u.User.query.filter_by(email=session['email']).first()
	if user is None:
		return redirect(url_for('admin'))
	else:
		totalNoOfBlood = db.session.query(p.PeopleProfile.id).count()
		print totalNoOfBlood
		bloodCategoryGroup=[]
		totalLists = db.engine.execute("select count(*) ,B.blood_type as bloodtype  from tbl_people_profile P inner join tbl_bloodcategory B on P.bloodCategoryId = B.id group by P.bloodCategoryId")
		for row in totalLists:
			bloodCategoryGroup.append(row)


		# return render_template('recipient_history.html', )








		return render_template('dashboard.html',totalB=bloodCategoryGroup,total=totalNoOfBlood, ar_history = ar_history, d_history = d_history)
@app.route('/addProfile',methods=['GET','POST'])
def addProfile():
	if request.method == 'GET':

		return render_template('addBlood.html')
	elif request.method == 'POST':
		name = request.form.get("name")
		email=request.form.get("email")
		phone = request.form.get("phone")
		address = request.form.get("address")
		bloodData = p.PeopleProfile(name,email,address,phone)
		db.session.add(bloodData)
     	db.session.commit()
     	flash('Record were added successfully')
	return render_template('addBlood.html' )

# @app.route('/addProfile',methods=['POST'])
# def addProfile():

	return render_template('addBlood.html');
@app.route('/testdb')
def testdb():
  if db.session.query("1").from_statement("SELECT 1").all():
    return 'It works.'
  else:
    return 'Something is broken.'



@app.route('/sign',methods=['GET','POST'])
def sign():
	# if request.method == 'GET':
	#
	# 	return render_template('user_signup.html')
	# elif request.method == 'POST':
	# 	name = request.form.get('name')
	# 	email=request.form.get('email')
	# 	password=request.form.get('password')
	# 	phone = request.form.get('phone')
	# 	address = request.form.get('address')
	# 	newUser = p.PeopleProfile(name,email,password, phone, address)
	# 	db.session.add(newUser)
    #  	db.session.commit()
    #  	flash('Record were added successfully')
	# return render_template('user_signup.html' )

	if request.method == 'POST':
		email = request.form.get("email")
		print email

		userS = p.PeopleProfile.query.filter_by(email=email).first()

		if userS :
			if userS.email == email:
				session['email'] = userS.email
				flash('email already registered')
				return render_template('user_signup.html')

		else:
			name = request.form.get('name')
			email = request.form.get('email')
			password = request.form.get('password')
			# hashpw = hash_password(password)
			phone = request.form.get('phone')
			address = request.form.get('address')
			bloodCategoryId = request.form.get('bloodCategory')
			# newUser = p.PeopleProfile(email = email)
			newUser = p.PeopleProfile( name, email, password, phone, address, bloodCategoryId)
			newUser.hash_password(password)
			db.session.add(newUser)
			db.session.commit()
			signer = Signer(app.secret_key)
			token = signer.sign(email)
			url = url_for('confirmation', token = token, _external = True)
			msg = Message("E-mail confirmation for Sahayog - A Blood Donation Portal", sender = "sahayog.project@gmail.com", recipients = [email])
			msg.body = url
			# flash(msg.body)
			mail.send(msg)
			flash('Record were added successfully')
		return render_template('user_signup.html' )

	elif request.method == 'GET':
		bloodCategoryL = b.BloodCategory.query.all()
		return render_template('user_signup.html', bloodCategoryList=bloodCategoryL )


# @app.route('/tdb')
# def tdb():
#   if db.session.query("1").from_statement("SELECT 1").all():
#     return 'It works.'
#   else:
#     return 'Something is broken.'

@app.route('/user/confirmation/<token>')
def confirmation(token):
	signer = Signer(app.secret_key)
	try:
		email = signer.unsign(token)

	except BadSignature :
		flash('Invalid token')
		return redirect(url_for('index'))

	else:
		userC = p.PeopleProfile.query.filter_by(email=email).first()
		userC.active = True
		db.session.add(userC)
		db.session.commit()
		flash('Your account is verified')
		return redirect(url_for('user'))






@app.route('/user/user_login',methods=['POST'])
def log():

	if request.method == 'POST':
		email = request.form.get("email")
		password = request.form.get("password")
		flash(email)


        userL = p.PeopleProfile.query.filter_by(email = email, active = True).first()
        if userL:
        	if userL.verify_password(password):
        		donorinfo = []
        		donor = d.DonorProfile.query.filter_by(people_profile_id = userL.id)
        		for row in donor:
					donorinfo.append(row)
					if not donorinfo:
						session['donor'] = 'False'
					else:
						session['donor'] = 'True'
						session['donor_blood_type'] = donorinfo[0].bloodCategoryId
        		session['id'] = userL.id
        		session['name'] = userL.name
        		session['email'] = userL.email
        		session['phone'] = userL.phone
        		session['address'] = userL.address

					# donorinfo = []
					# donor = db.engine.execute("select * from tbl_donor D where people_profile_id = %s limit 1",(session['id']))
					# for row in donor:
					# 	donorinfo .append(row)


					# if not donorinfo :
					# 	session['donor'] = True
					#
					# else:
					# 	print('hi')

        		# session['bloodgroup'] = userL.bloodgroup
        		return redirect(url_for('index'))

        	else:

        		flash("invlaid email or password")
        		return redirect(url_for('user'))
        else:
        	flash("Invalid email")
        	return render_template('user_login.html')

@app.route('/user/forgot_password', methods = ['GET','POST'])
def forgot_password():
	if request.method == 'POST':
		email = request.form.get("email")

		signerU = Signer(app.secret_key)
		token = signerU.sign(email)
		url = url_for('reset_password', token = token, _external = True)
		msg = Message("Reset password URL for Sahayog - A Blood Donation Portal", sender = "sahayog.project@gmail.com", recipients = [email])
		msg.body = url
		mail.send(msg)
		flash("Email Sent. Please check your inbox.")
		return render_template('forgot_password.html')

	elif request.method == 'GET':
		return render_template('forgot_password.html' )

@app.route('/user/reset/<email>', methods = ['GET', 'POST'])
def reset(email):
	if request.method == 'POST':
		newpassword = request.form.get('new_password')
		confirmpassword = request.form.get('confirm_password')

		if newpassword == confirmpassword:
			userZ = p.PeopleProfile.query.filter_by(email=email).first()
			userZ.hash_password(newpassword)
			db.session.add(userZ)
			db.session.commit()
			flash('Password reset')

			return redirect(url_for('user'))


		else:
			flash("Password does not match, Please enter the Password again")
			return render_template('reset_password.html')


@app.route('/user/reset_password/<token>', methods = ['GET','POST'])
def reset_password(token):

	signerU = Signer(app.secret_key)
	try:
		email = signerU.unsign(token)

	except BadSignature :
		flash('Invalid token')
		return redirect(url_for('index'))


	else:
		flash(email)

		return render_template('reset_password.html', email = email)
		#userC = p.PeopleProfile.query.filter_by(email=email).first()
		# userC.password = "newpassword"
		#db.sesion.add(userC)
		#db.session.commit()


		#return redirect(url_for('reset_password'))
		# if request.method == 'POST':
		# 	newpassword = request.form.get('new_password')
		# 	confirmpassword = request.form.get('confirm_password')
		#
		# 	if newpassword == confirmpassword:
		# 		userZ = p.PeopleProfile.query.filter_by(email=email).first()
		# 		flash(userZ)
		# 		newHashPassword = userR.hash_password(newpassword)
		# 		userZ.password(newpassword)
		# 		db.session.add(userZ)
		# 		db.session.commit()
		#
		# 		return redirect(url_for('index'))
		#
		# 		flash('testing')

		# # return redirect(url_for('index'))
		#
		# elif request.method == 'GET':
		#  	return render_template('reset_password.html' )

# @app.route('/user/reset_password', methods = ['GET', 'POST'])
# def reset_password():
# 	if request.method == 'POST':
# 		newpassword = request.form.get('new_password')
# 		confirmpassword = request.form.get('confirm_password')
#
# 		if newpassword == confirmpassword:
# 			userZ = p.PeopleProfile.query.filter_by(email = email).first()



@app.route('/recipient', methods = ['GET', 'POST'])
def recipient():
	if request.method == 'GET':
		bloodCategoryL = b.BloodCategory.query.all()
		return render_template('receive.html', bloodCategoryList = bloodCategoryL )

	elif request.method == 'POST':
		name = request.form.get('name')
		people_profile_id = session['id']
		phone = request.form.get('phone')
		email = request.form.get('email')
		address = request.form.get('address')
		bloodCategoryId = request.form.get('bloodCategoryId')
		userRecepient = r.RecipientProfile(people_profile_id, name, phone, email, address, bloodCategoryId)
		db.session.add(userRecepient)
		db.session.commit()
		flash('Form successfully Submitted')
    	return redirect(url_for('index'))

# @app.route('/listrecipient')
# def listrecipient():
# 	result = []
# 	profiles=db.engine.execute("select * from tbl_recipient R")
# 	for row in profiles:
# 		result.append(row)
# 	print result
# 	return render_template('index.html', results=result)


@app.route('/donor', methods=['GET', 'POST'])
def donor():

	# flash (recipient)
	# return render_template('donor.html')
	donorinfo = []
	donor = db.engine.execute("select * from tbl_donor D where people_profile_id = %s limit 1",(session['id']))
	for row in donor:
		donorinfo .append(row)
	print donorinfo
	# select from table tbl_recipient where id = recipeint

	if request.method == 'POST':
		donor_name = request.form.get('donor_name')
		people_profile_id = session['id']
		bloodCategoryId = request.form.get('bloodCategoryId')
		donor_phone = request.form.get('donor_phone')
		donor_email = request.form.get('donor_email')
		donor_address = request.form.get('donor_address')
		donor_age = request.form.get('donor_age')
		donor_gender = request.form.get('donor_gender')
		# recipeint_name = request.form.get('recipeint_name')
		# recipient_blood_type = request.form.get('recipient_blood_type')
		if not donorinfo :

			userDonor = d.DonorProfile(people_profile_id, donor_name, bloodCategoryId, donor_phone, donor_email, donor_address, donor_age, donor_gender )
			db.session.add(userDonor)
			db.session.commit()
		else:
			print('hi')


		return render_template('donor.html')


	elif request.method == 'GET':
			bloodCategoryL = b.BloodCategory.query.all()

			return render_template('donor.html', bloodCategoryList = bloodCategoryL)

@app.route('/donation/<recipient_id>')
def donation(recipient_id):
	if session['id']:
		r = db.session.query(d.DonorProfile).filter_by(people_profile_id = session['id']).first()
		donor_id = r.id
		#recipient_id = recipient_id
		check_record = db.session.query(o.DonorRecipient).filter_by(recipient_id = recipient_id,donor_id=donor_id).first()
		if check_record :
			flash("Already donated")

		else:
			recipient_donor = o.DonorRecipient(recipient_id, donor_id)
			db.session.add(recipient_donor)
			db.session.commit()
			flash("successfully donated")
		return redirect(url_for('index'))
		# print(recipient_donor)

		# if request.method = 'POST':


	else:
		return redirect(url_for('user'))
		endif

	return render_template('donation.html', recipient_id = recipient_id)


@app.route('/recipient_history')
def recipient_history():
	r_history = []
	history = db.engine.execute("select * from tbl_recipient R where people_profile_id = %s", (session['id']))
	for row in history :
		r_history.append(row)

	return render_template('recipient_history.html', r_history = r_history)



@app.route('/donor_history')
def donor_history():
	d_history = []
	r = db.session.query(d.DonorProfile).filter_by(people_profile_id = session['id']).first()
	history = db.engine.execute("select r.*,rd.id,rd.posted_date from tbl_donor d JOIN tbl_recipient_donor rd ON d.id = rd.donor_id JOIN tbl_recipient r  ON r.id = rd.recipient_id where d.id = %s", (r.id))
	for row in history :
		d_history.append(row)
		print(d_history)
	return render_template('donor_history.html', d_history = d_history)

@app.route('/recipient_status_update/<recipient_id>')
def recipient_status_update(recipient_id):
	status = request.args.get('status')

	donor = db.engine.execute("UPDATE tbl_recipient  SET status=%s where id = %s",(status,recipient_id))
	print status
	print recipient_id

	return redirect(url_for('dashboard'))


@app.route('/recipient_received_update/<recipient_id>')
def recipient_received_update(recipient_id):
	received = request.args.get('received')

	donor = db.engine.execute("UPDATE tbl_recipient  SET received=%s where id = %s",(received,recipient_id))
	print received
	print recipient_id

@app.route('/user_recipient_status_update/<recipient_id>')
def user_recipient_status_update(recipient_id):
	status = request.args.get('status')

	donor = db.engine.execute("UPDATE tbl_recipient  SET status=%s where id = %s AND people_profile_id =%s",(status,recipient_id, session['id']))
	print status
	print recipient_id

	return redirect(url_for('recipient_history'))


@app.route('/user_recipient_received_update/<recipient_id>')
def user_recipient_received_update(recipient_id):
	received = request.args.get('received')

	donor = db.engine.execute("UPDATE tbl_recipient  SET received=%s where id = %s AND people_profile_id = %s",(received,recipient_id, session['id']))
	print received
	print recipient_id


	return redirect(url_for('recipient_history'))















@app.route('/logout')
def logout():

  if 'email' not in session:
    return redirect(url_for('index'))

  session.pop('email', None)
  return redirect(url_for('index'))
