## Dockerized ticket note Flask application

## Introduction

This is a small Flask ticket note app that I use for personal usage and have now dockerized. The application is developed with the Python Flask framework, a Mysql database, and an HTML input page. There's also a phpmyadmin for listing database inputs. 

The strcuture of project is as follows

![a](https://user-images.githubusercontent.com/65948438/163019339-cc8e98a3-3300-4a4e-96a5-c558f8e4dd7d.png)

Then I made a docker image and used the docker compose tool to make containers.

## Prerequisites
  - Docker installed on your server.
  - Docker Compose installed on your server.

## Explanation
1. app.py
```sh
from flask import Flask, request, render_template, redirect, url_for
from db import add_text, get_data

app = Flask(__name__,template_folder='templates')
@app.route("/")
def getList():
    all_text = get_data()
    return render_template('index.html')

@app.route("/add_text", methods=["POST", "GET"])
def AddText():
    if request.method == "POST":
        ticket_data = request.form["textv"]
        #saving all the values to db
        add_new = add_text(ticket_data)
        return redirect(url_for('getList'))
    else:
        return render_template('index.html')
if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
```

This app.py file will handle HTTP requests. Inside it, you’ll import the Flask object, and other objects like render_template, redirect and url_for to create a function that returns an HTTP response. 

In the preceding code block, you first import the Flask object from the flask package. You then use it to create your Flask application instance with the name app. You pass the special variable __name__ that holds the name of the current Python module. It’s used to tell the instance where it’s located—you need this because Flask sets up some paths behind the scenes. Also we need to specify the path directorty which containing our html file.

Once you create the app instance, you use it to handle incoming web requests and send responses to the user. @app.route is a decorator that turns a regular Python function into a Flask view function, which converts the function’s return value into an HTTP response to be displayed by an HTTP client, such as a web browser. You pass the value '/' to @app.route() to signify that this function will respond to web requests for the URL /, which is the main URL.

Flask provides a render_template() helper function that allows use of the Jinja template engine. This will make managing HTML much easier by writing your HTML code in .html files as well as using logic in your HTML code. You’ll use these HTML files, (templates) to build all of your application pages, such as the main page.

2. db.py
```sh
import pymysql
#database connection
connection = pymysql.connect(host="db", user="<mysql username>", passwd="<mysql user password>", database="TicketsList")
cursor = connection.cursor()
#inserting data to db
def add_text(ticket_data):
    cursor.execute("INSERT INTO TICKETS_DATA(TICKET_ID,TICKET_DATE) VALUES (%s, DEFAULT)",(ticket_data))
    connection.commit()
    return 1

def get_data():
    cursor.execute("SELECT TICKET_ID, DATE(TICKET_DATE) FROM TICKETS_DATA ORDER BY TICKET_DATE DESC")
    rows = cursor.fetchall()    
```
Next is to configure the database settings for establishing the communication between flask and database. 

We're using pymysql module to connect our app to the mysql database. PyMySQL is a module for connecting to a MySQL database server from Python. 

To interact with DB tables with we're using something called 'cursor'. Cursor thus provides a means for Flask to interact with the database tables. It can scan the database for data, execute SQL queries, and delete table records. Because MySQL is not an auto-commit DB, we must manually commit, i.e. save the changes/actions performed by the cursor execute on the DB.

When the user submits the data, the cursor inserts it into the MySQL DB.

3. index.html
```sh
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Ticket List</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
       
        <style> 
            input[type=text] {
              width: 10%;
              padding: 12px 20px;
              margin: 8px 0;
              box-sizing: border-box;
              border: 2px solid rgb(4, 146, 241);
              border-radius: 4px;
            }
            input[type=submit] {
              background-color: rgb(4, 146, 241);
              border: 1px solid rgb(4, 5, 5);
              color: white;
              padding: 6px 7px;
              text-decoration: none;
              margin: 4px 2px;
              box-sizing: border-box;
              border-radius: 2px;
              cursor: pointer;
            }

            </style>    
    </head>
    <body>
  
        <form action="/add_text" method="post">
            <label for="textv">Ticket ID:</label><br>
            <input type="text" id="textv" name="textv" value=""><br>
            <input type="submit" value="Submit">
       </form>
       <br><br><hr>

</body>
```
We're creating a html page that contains a form to input values for users with some css codes.

4. database.sql
```sh
6. CREATE DATABASE TicketsList;
USE TicketsList;
DROP TABLE IF EXISTS `TICKETS_DATA`;
CREATE TABLE `TICKETS_DATA` (
  `TICKET_ID` int(11) NOT NULL AUTO_INCREMENT,
  `TICKET_DATE` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`TICKET_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=10330929 DEFAULT CHARSET=utf8mb4;
```
Now we need a sql file which containe SQL queries to create database that we need to restore it to docker container while creating.

5. Dockerfile
```sh
FROM python:3.9-alpine3.14
ENV FLASK_PATH /flaskapp
ENV FLASK_USER flaskuser
RUN adduser -h $FLASK_PATH -s /bin/sh -D $FLASK_USER
WORKDIR $FLASK_PATH
COPY . .
RUN chown -R $FLASK_USER:$FLASK_USER $FLASK_PATH
RUN pip install -r requirements.txt
USER $FLASK_USER
CMD ["app.py"]
ENTRYPOINT ["python3"]
```
The important part of your app is to create a Dockerfile for building your application. 

6. requirements.txt
```sh
Flask
Flask-MySQL
PyMySQL
mysql-connector
```
You need dependencies Flask, mysql-connector, Flask-MySQL and PyMySQ in File requirements.txt


7. docker-compose.yml
```sh
version: "3"
services:
  app:
    build: ./app
    links:
      - db
    networks:
      - backend 
    ports:
      - "80:5000"

  db:
    image: mariadb:10.5
    networks:
      - backend 
    environment:
      MYSQL_ROOT_PASSWORD: root@123
    volumes:
      - ./database:/docker-entrypoint-initdb.d/
  phpmyadmin:
    image: phpmyadmin:latest
    environment:
      PMA_HOST: db
      PMA_USER: <db user>
      PMA_PASSWORD: <db user password>
    ports:
      - "8080:80"     
    networks:
      - backend    

networks:
  backend:
```

Now the final part is to create docker compose file under the project’s. The docker compose file name is docker-compose.yml/yaml and the formatting must be consistent otherwise build will be failed.

I am using three services, one is a container that exposes the Flask app, another one contains the database (db) and the last one is phpmyadmin to access and manage our database.

build: specifies the directory that contains the Dockerfile containing the instructions for building this service

links: links this service to another container. This will also allow you to use the name of the service instead of having to find the ip of the database container, and express a dependency which will determine the order of start up of the container

ports: mapping of ports from container to host so that this port can be exposed to the outside world for accessing the app URL.

image: similar to the FROM instruction in the Dockerfile. Instead of writing a new Dockerfile, I am using an existing image from a repository. It’s important to specify the version. If your installed mysql client is not of the same version problems may occur.

environment: add environment variables. The specified variable is required for this image, and as its name suggests, configures the password for the root user of MySQL in this container.

Now let’s run the dockerized app by executing the following command:

```sh
$ docker-compose up -d
```
The result, after running the Flask app

![6](https://user-images.githubusercontent.com/65948438/163344485-f192d588-1e10-4e97-9b5c-58115d8592d8.png)

That is all. I'm attaching the final result of front end below:

![4](https://user-images.githubusercontent.com/65948438/163345906-3491024b-a5b4-48ae-8f74-ff243fada35e.png)

![5](https://user-images.githubusercontent.com/65948438/163345929-b7e3a7eb-3022-4b99-a742-ecf399d3fbf0.png)


# Conclusion
You have Deployed Flask-MySQL app with docker-compose. Thank you for reading the page!

Have fun dockerizing!


