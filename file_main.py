from flask import Flask, render_template, Response, request, redirect, send_from_directory, url_for
from data import User, Post, Student, Disciplines, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
import os



app = Flask(__name__)
app.config["SECRET_KEY"] = 'gay'
login_manager = LoginManager()
login_manager.login_view ='login'
login_manager.init_app(app)
file_path = '/home/vlados/kurs/files'
app.config['UPLOAD_FOLDER'] = file_path

class LoginForm(FlaskForm):
	username = StringField('username')
	password = PasswordField('password')
	submit = SubmitField('submit')



@login_manager.unauthorized_handler
@app.route('/login', methods = ['POST','GET'])
def login():
	form = LoginForm()
	if request.method == 'POST':
		x = session.query(User).filter(User.nickname == form.username.data).first()
		if(x and x.password_check(form.password.data)):
			login_user(x)
			return redirect('title')
		else:
			return redirect('login')
	return render_template('authorization.html')

@app.route('/')
@app.route('/title')
def title():
	return render_template('title.html',session = session, Post = Post, User = User, current_user = current_user)


@app.route('/post', methods = ['POST','GET'])
@login_required
def to_post():
	if request.method == 'POST':
		session.add(Post(request.form['text'],current_user))
		session.commit()
		return redirect('title')
	return render_template('post.html')


@app.route('/materials')
@login_required
def materials():
	return render_template('usefull_things.html', session = session, Disciplines = Disciplines)


@app.route('/materials/upload', methods = ['POST','GET'])
@login_required
def materials_upload():
	if request.method =='POST':
		print(request.files)
		f = request.files['filename']
		f.save(os.path.join(app.config['UPLOAD_FOLDER'],f.filename))
		return "file saved success"
	return render_template('upload.html')


@app.route('/download/<filename>')
@login_required
def download(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'],filename)


@app.route('/group_list',methods = ['GET'])
@login_required
def group():
	return render_template('group_list.html', session = session, Student = Student, current_user = current_user)


@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect('login')


@login_manager.user_loader
def load_user(id):
	return session.query(User).filter(User.id == id).first()

app.run(debug = True)
