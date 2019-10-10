FROM ubuntu:18.04
WORKDIR /flask_server
COPY . /flask_server
RUN apt-get update
RUN apt-get install -y python3-pip
RUN apt-get install -y python-dev default-libmysqlclient-dev
RUN apt-get install -y python3-dev 
RUN cd mysqlclient-python 
RUN pip3 install -r requirements.txt
RUN cd mysqlclient-python && python3 setup.py install
EXPOSE 80
CMD ["python3","main.py"]