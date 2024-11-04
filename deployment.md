## Deploy your app

Deployment allows you to transfer your project from your local environment to hosting it publicly for other people to view and enjoy.
Make your code repo ready for deployment

#### Gitpod

In settings:
Set DEBUG = False

Make sure everything is migrated.
You can use commands in terminal as:
python3 manage.py showmigrations
python3 manage.py migrate  

Commit and push code to GitHub

Log in to Heroku and check your config vars
If you still have collectstatic, you need to delete that and make sure you use aws.
![deployconfigvars](static/images/Readme_img/deployconfigvars.png)

For manual deploy in Heroku, you click Deploy Branch 
![deploybransch](static/images/Readme_img/deploybransch.png)

You can also deploy from terminal in Gitpod with command:
Heroku git push heroku main

In Heroku go to your app, click on activity to check if it has finished deploying

Open app to view the live site

Any data that you have added to your SQLite database will not transfer to the new one.

