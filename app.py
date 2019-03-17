from flask import Flask,render_template,request,jsonify,redirect,session, flash, url_for
from werkzeug import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL
from forms import RegisterForm, LoginForm, BookReco
import codecs,json,decimal,MySQLdb.cursors
import recSys
from flask_wtf import CSRFProtect


app=Flask(__name__)
app.secret_key = 'Copyright @ SWATI S BHAT,SWATHI S BHAT'
csrf = CSRFProtect()
csrf.init_app(app)

#database 
mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mysql'
app.config['MYSQL_DB'] = 'recsys'
app.config['MYSQL_HOST'] = 'localhost'
mysql.init_app(app)


def decimal_default(obj):
	if(isinstance(obj,decimal.Decimal)):
		return float(obj)

	raise TypeError


@app.route('/',methods=['GET','POST'])
def home():
	form = BookReco(request.form)
	if request.method=='GET':
		if session.get('user'):
			return render_template('home.html',form=form, user=session['user'])
		else:
			return render_template('home.html', form=form)

	book_like=form.book.data
	res=recSys.recommend(book_like)
	if session.get('user'):
		return render_template('home.html',form=form, user=session['user'],response=res)
	else:
		return render_template('home.html', form=form, response=res)

	
@app.route('/autocomplete',methods=['GET'])
def autoComplete():
	book_list = codecs.open('books.json', 'r', encoding='utf-8').read()
	array=json.loads(book_list)
	return jsonify(result=array)

@app.route('/register', methods=['GET','POST'])
def register():
	
	form = RegisterForm(request.form)
	if request.method=='POST':
		
		if form.validate():
			try:
				conn = mysql.connection
				cursor = conn.cursor()
				hashed_password = generate_password_hash(form.password.data)
				cursor.callproc('createUser',(form.firstname.data,form.lastname.data,form.username.data,form.dob.data,form.country.data,form.email.data,hashed_password))
				data = cursor.fetchall()

				if len(data) is 0:
					
					conn.commit()
					cursor.close()
					flash('Registration successful. Please login to continue.', 'success')
					return redirect(url_for('login'))
				else:
					cursor.close()
					flash(str(data[0]),'danger')
					return render_template('register.html',form=form)
			

			except Exception as e:
				flash(str(e),'danger')
				return render_template('register.html',form=form)

	
	return render_template('register.html', form=form)

@app.route('/login',methods=['GET','POST'])
def login():
	form = LoginForm(request.form)
	if request.method=='POST':
		if form.validate():
			try:
				
				con=mysql.connection
				cursor=con.cursor()
				cursor.callproc('validateLogin',(form.email.data,))
				data=cursor.fetchall()
				if len(data) > 0:
					if check_password_hash(str(data[0][2]),form.password.data):
						session['user'] = data[0][0]
						return redirect(url_for('show_filters'))
					else:	
						flash('Incorrect Password','danger')
						return render_template('login.html', form=form) 
				else:
					flash(str(data[0]),'danger')
					return render_template('login.html', form=form) 
			except Exception as e:
				flash(str(e),'danger')
				return render_template('login.html',form=form)

			
	return render_template('login.html', form=form)

@app.route('/signout')
def signout():
    session.pop('user',None)
    return redirect('/')

@app.route('/filters')
def show_filters():
	if session.get('user'):
		return render_template('filters.html',user=session['user'])
	else:
		flash('Unauthorized access. Please login to continue.','danger')
		return render_template('filters.html')

@app.route('/load_data')
def load_data():
	conn=mysql.connection
	cursor=conn.cursor(MySQLdb.cursors.DictCursor)
	query2="select bookID,ISBN13,title,authors,original_Publication_Year,average_Rating,ratings_Count from books where goodreads_Book_ID not in (select goodreads_Book_ID from toRead where userID={});".format(session['user'])
	cursor.execute(query2)
	data=cursor.fetchall()
	data=json.dumps(data,default=decimal_default)
	
	return data

@csrf.exempt
@app.route('/add_to_read',methods=['POST'])
def add_to_read():
	try:
		conn=mysql.connection
		cursor=conn.cursor()
		book_id=request.json['book_id']
		query="select goodreads_Book_ID from books where bookID={};".format(book_id)
		cursor.execute(query)
		data=cursor.fetchall()
		goodreadsBookID=data[0][0]
		user_id=session.get('user')
		query="INSERT INTO toRead VALUES ({},{})".format(user_id,goodreadsBookID)
		cursor.execute(query)
		conn.commit()
		return json.dumps(query)#jsonify({'result':'success'})
	except Exception as e:
		return json.dumps(e)


@app.route('/profile')
def user_profile():
	if session.get('user'):		
		return render_template('profile.html',user=session['user'])
	else:
		flash('Unauthorized access. Please login to continue.','danger')
		return render_template('profile.html')



@app.route('/load_profile_data')
def load_profile_data():
	conn=mysql.connection
	cursor=conn.cursor(MySQLdb.cursors.DictCursor)
	query="SELECT bookID,title,authors from books where goodreads_Book_ID in (select goodreads_Book_ID from toRead where userID={});".format(session['user'])
	cursor.execute(query)
	data=cursor.fetchall()
	data=json.dumps(data,default=decimal_default)
	return data

@csrf.exempt
@app.route('/add_read',methods=['POST'])
def add_read():
	conn=mysql.connection
	cursor=conn.cursor()
	book_id=request.json['book_id']
	query="select goodreads_Book_ID from books where bookID={};".format(book_id)
	cursor.execute(query)
	data=cursor.fetchall()
	goodreadsBookID=data[0][0]
	user_id=session.get('user')
	post = request.args.get('post', 0, type=str)
	query="INSERT INTO has_read VALUES ({},{})".format(user_id,goodreadsBookID)
	cursor.execute(query)
	conn.commit()
	query2="DELETE FROM toRead where userID={} and goodreads_Book_ID={};".format(user_id,goodreadsBookID)
	cursor.execute(query2)
	conn.commit()
	return json.dumps(query2)

if __name__ == '__main__':
	app.run()
