# opendoors

opendoors is a web application developed for Lake Forest High School that aims to facilitate connection between students and job shadowing opportunities provided by mentors.

##Installation

This program is currently configured to deploy to heroku. However, it can be installed as a flask application given a database source consistent with below and the prescence of the below environment variables.

#Database

This program can use both MySQL & PostgreSQL to host data. The respective drivers are

 1. MySQL - ```mysql+pymysql://```
 2. POSTGRES - ```postgres://```
 
 Example use for database URI ```mysql_pymysql://user:password...```

## Environment Variables

To use this program, Environment Variables must be present when the application is started
 1. ```DATABASE_URL``` - The database URI in the form driver://username:password@server:port/database. Please note that this program is currently configured to work with postgres and mysql databases through SQLAlchemy. Refrence drivers section above for formatting urls.
 2. ```MAIL_SERVER``` - The email server that the program will send emails from ex. ```smtp.google.com```
 3. ```MAIL_USERNAME``` - The email username or email that is used to log into the mail server ex. ```opendoors@gmail.com```
 4. ```MAIL_PASSWORD``` - The password that corresponds to ```MAIL_USERNAME```
 5. ```MAIL_PORT``` - The port that corresponds to the mail server
 6. ```MAIL_DEFAULT_SENDER``` - The email address that sends emails. Most often will match ```MAIL_USERNAME```
 7. ```ADMINISTRATOR_USERNAME``` - The username that will be used to login to the administrator login page
 8. ```ADMINISTRATOR_PASSWORD``` - The password that will be used to login to the administrator login page

Optional:
 1. ```RESET``` - If this environment varialbe is set to anything, will drop all data within the database, resetting the tables and resetting program configuration information
##Heroku

A Procfile has already been defined within the project

 1. Install Heroku CLI and create a heroku app for this application
 2. Add postgresql database addon to heroku application
 ```shell script
heroku addons:create heroku-postgresql:<your-tier-database>
```
 3. Set environment variables
 ```shell script
heroku config:set ENV_VAR=VAR
```
Note: Heroku will often configure ```DATABASE_URL```, however, you can get connection string from application page online as well
 4. Fork the project, then download contents to your folder
 
 5. Push the project to the app's heroku repository using git
 ```shell script
git push heroku master
```
 6. Open program in browser
```shell script
heroku open
```

Your application should now be live on heroku, which can be customized to your DNS
