# assignment-fraud
This is fraud detection app, there are two endpoints; one is creating a person and second one is matching a given person searching for database.This app is created with Django, using postgres as database and memcached as cache server.

**Table Of Content**

[TOC]

#### Requirements

- Docker;
- Postman;
- Docker compose;
- Permission given to the entrypoint.sh;



#### How to run the system
go inside the directory
```
cd ./assignment-fraud
```
after that if needed give permission to the entrypoint.sh file. If on linux system permission can be given with:
```
chmod 777 ./entrypoint.sh
```
After the permision is given to the folder. There is one more step and then it is done. Run the docker containers:
```
docker compose up -d
```
after this the server will be up in couple of minutes

#### How To Access To The App and Admin Panel
You can access the web app using this your local url with port 8000. It will give you page not found error. Because this app is only for endpoints. below url is an example of how to access the apps admin panel:
```
localhost:8000/admin/
```
After this you need to login as an admin user. By default admin username and password is :
```
username: admin
password: admin
```
On the left side you can see the Matcher rules configs, person data matchers and person datas. Lets start with Matcher rules config.

In Matcher rules config you can see there are 5 different rules and their values. You can change the values by opening up the one you want to change and then change and save it. Even though you can add new rules, those newly added rules will not be applied. That functionality is not implemented yet.

In person data matchers you can see the logs. When you run the matcher endpoint it will run the matcher pipeline and create a match status. If the status is 100 then that means that person trying to trick the system for fraud. If you want to see why they have those scores, you can click the see details on the left side and you can see the log and why they have that score.

In person datas section, you can see the person data stored in the database

#### Security
right now if you are not a user you cannot run the endpoints. By default everyone can create a user and thus run these endpoints afterwards but it can be changed so that only admin or specific permission can run these endpoints. This will be a hard change but the sake of the testing it is like this. If needed if can be added to the endpoints. You can check how to do it inside "/fraudapp/views.py" then in "CreateUserAPIView" class.

#### Endpoints Directory

    fraudapp/
        Auth/
            Login Token Generator // creates bearer token 
            Create New User // creates new user
        Utilities/
            Get All Persons Data // returns all persons data stored in the database
            Add New Person Data // add new person to the database
            Match Person Data // matches given person data with the data in database



#### Endpoints and Postman Collection
As given above the directory I will go over them and make sure that it is clear and you will understand the flow. First of all you need to click the 'fraudapp' collection and set the url variables to your need. by default it is 'localhost:8000'.

##### 	Create new user
with this endpoint you can create a normal user. key parameters is:
- username
- password
- name
- email

after the user creation you need to get a login token.
##### Login Token Generator
this endpoint gives you refresh and access tokens. and need 2 key parameters:
- username
- password
after getting you access token, please copy that. Then, click the "fraudapp" collection and paste it to the token field inside Authorization tab. Type should be bearer token. Access token will be alive for 50 minutes for the sake of the testing. Generally it will be around 5 minutes or so.

##### Get All Persons Data
This request does not need a parameter and returns all the persons data in the database. But you can only use this request if you are an admin user. This request is cached for 2 minutes using memcached

##### Add New Person Data
this request will add a person to the database. Key parameters:
- first_name
- last_name

optional parameters:
- date_of_birth
- id_number

##### Match Person Data
this request will check if the given user in the request is trying to trick the system and returns a score according to the given information. key parameters:
- first_name
- last_name

optional parameters:
- date_of_birth
- id_number



