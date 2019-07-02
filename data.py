from sqlalchemy import create_engine,Table, Column, Integer, String, ForeignKey, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.pool import QueuePool
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import os

engine = create_engine('mysql+mysqldb://root:123456@localhost:3306/cherry', echo = False, poolclass = QueuePool)
Session = sessionmaker(bind = engine)
Base = declarative_base()
session = Session()
class User(UserMixin,Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key=True, autoincrement = True)
	nickname = Column(String(20), unique = True, nullable = False)
	password = Column(String(100), nullable = False)
	activity = Column(Integer)

	post = relationship('Post', back_populates = 'user', cascade = "all, delete, delete-orphan")

	def __init__(self, nickname, password, activity = 0):
		self.nickname = nickname
		self.password = generate_password_hash(password)
		self.activity = activity
	def __repr__(self):
		return self.nickname  
	def password_check(self, password):
		return check_password_hash(self.password, password)

class Post(Base):
	__tablename__ = 'post'

	post_id = Column(Integer, primary_key = True)
	post_data = Column(String(255), nullable = False)
	nickname = Column(String(20), ForeignKey('user.nickname'), nullable = False)


	user = relationship("User", order_by = User.id, back_populates = 'post')

	def __init__(self, post_data, User):
		self.post_data = post_data
		self.nickname = User.nickname
		User.activity += 1

	def __repr__(self):
		return self.post_data + '@ by ' +self.nickname

class Student(Base):
	__tablename__ = 'student'

	id = Column(Integer, primary_key=True, autoincrement = True)
	name = Column(String(30), nullable = False)
	surname = Column(String(30), nullable = False)
	group = Column(String(30), nullable = False)
	math = Column(Integer)
	nature = Column(Integer)
	programming = Column(Integer)

	def __init__(self, name, surname, group, math = 0, nature = 0, programming = 0):
		self.name = name
		self.surname = surname
		self.group = group
		self.math = math
		self.nature = nature
		self.programming = programming
 
	def __repr__(self):
		return self.name + ' '  + self.surname


class Disciplines(Base):
	__tablename__ = 'disciplines'

	id = Column(Integer, primary_key = True, autoincrement = True)
	discipline = Column(String(30), nullable = True, unique = True)
	name = Column(String(30), nullable = False, unique = True)
	path = Column(String(70), nullable = False, unique = True )

	def __init__(self, discipline, name, path = '/home/vlados/kurs/files'):
		self.discipline = discipline
		self.name = name
		self.path = os.path.join(path + '/' + discipline, name)

	def __repr__(self):
		return self.discipline + ' : ' + self.name

#session.add(User('hueta', 'lolkek'))
#session.commit()
#session.close()
#print((session.execute(text("SELECT nickname FROM user")).first()).nickname) - works
#print((tuple(('gay',)) in (session.execute(text("SELECT nickname FROM user")).fetchall()))) 
#print(((session.query(User.nickname).filter_by(nickname = 'gay').all().nickname)))
#print(type('sar'))
'''
username = 'gay',
password = 'gay',
if (username + password) in (session.execute(text("SELECT nickname, password FROM user"))).fetchall():
	print('hello')
else:
	print(username + password)
	print(session.execute(text("SELECT nickname, password FROM user")).fetchall())
'''
#update
#Base.metadata.create_all(engine)
'''
Session = sessionmaker(bind = engine)
session = Session()
session.commit()
'''
#print(str(session.dirty()) + ' ' + 'DIRTY THIGS WAS MADE ' )