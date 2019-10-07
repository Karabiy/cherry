def result_engine():
	return database_used+'://'+database_user+':'+database_user_password+'@'+database_ip_port+'/'+database_name





database_used = 'mysql+mysqldb'
database_user = 'vladik'
database_user_password = 'password'
database_ip_port = '172.17.0.2:3306'
database_name ='cherry'
#172.17.0.2/16
# mysql+mysqldb://flask_originally:123456@database_ip_port/cherry