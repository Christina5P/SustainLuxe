Make your code repo ready for deployment
Set DEBUG = False
Commit and push code to GitHub
Navigate to Heroku and login
From Heroku dashboard, create a new app
Select region
Giv you app a unique name
Navigate to settings tab and click reveal config vars. Add Following config vars:
For Security & Authentication
SECRET_KEY
For Database
DATABASE_URL
For Stripe
STRIPE_PUBLIC_KEY
STRIPE_SECRET_KEY
STRIPE_WH_SECRET
For AWS
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
USE_AWS
For EMAIL
EMAIL_HOST_PASS
EMAIL_HOST_USER
Click on deploy tab and connect to github
Search for repo and click on the one you want to deploy
Scroll down to manual deploy
Select (main) branch
Click Deploy Branch
Open app to view the live site


Forking the GitHub Repository
Forking the GitHub repository allows you to create a duplicate repository in order to make changes without affecting the original.

Log in to GitHub and go to the Island Bees GitHub repository
Click on Fork (top right) to fork the repository
Give the fork a name and description if you wish and click "Create Fork"
You can now open the repository in your IDE of choice e.g. GitPod
Once in your IDE you can install the project requirements from the requirements.txt file using the command pip3 install -r requirements.txt
Making a Local Clone
A local clone allows you to create a copy of the project to work on locally on your own computer in your code editor of choice (e.g. VS Code)

Log in to GitHub and go to the Island Bees GitHub repository
Click on "Code"
To clone using HTTPS copy the provided link on the HTTPS tab
Open your own terminal for your coding environment (making sure you have Git installed)
Set your current directory to the location you want to store your new clone
Type git clone, followed by the copied link you copied from GitHub e.g. git clone https://github.com/emmahewson/island-bees.git
Press Enter to create your local clone of the project
Set up your local development environment
Install the project requirements from the requirements.txt file in the project using the command pip3 install -r requirements.txt
Create your own env.py file containing all the required environment variables
You are now ready to start working on your own clone of the project - enjoy!
For more details and information go to GitHub's useful guide to cloning repositories

Deploying Your App
Deployment allows you to transfer your project from your local environment or IDE to hosting it publicly for other people to view and enjoy. There are certain steps you will need to take to do this and they are detailed below. These instructions are based on using an IDE like GitPod and having followed the instructions for Forking the repository above, especially installing the requirements. For users wishing to deploy from a local clone different steps may be required which will depend on your local development environment.

Setting up a Database
When working on the app in GitPod a local database (sqlite) is used which will not be available on the deployed app. You will need to set up a separate database for the deployed site.

Go to ElephantSQL and click on 'get a managed database'
Select 'Tiny Turtle'
Sign in using your GitHub account & authorise ElephantSQL to access your GitHub account
Set up a team and go through the login credential process or log in if you already have an account
Once you are logged in name your plan (usually the project name)
Select your nearest region
If you're happy click on 'create instance'
Go to your dashboard (click on the ElephantSQL logo) and click on the instance name
Copy the database URL... you will need this for the next steps
Set up Heroku & connecting your new Database
Go to Heroku and log in (or set up an account if you don't have one - please note you may incur charges for using Heroku)
Click on the 'New' button then 'create new app'
Name your app and select your nearest region
With your app set up go to the app's settings tab and under config variable click on 'reveal config variables' and add a new variable with the Key of DATABASE_URL and the value as the database URL that you copied from ElephantSQL
Back in GitPod go to settings.py and paste the following in to your DATABASE section to tell it to connect to the new database Note - do not push your code to GitHub whilst this value is in your settings.py, it is a secret value that must not be shared, we will remove it later
DATABASES = {
        'default': dj_database_url.parse(os.environ.get('your elephanySQL database url here'))
    }
In you GitPod terminal type python3 manage.py showmigrations to check you are connected to the new database, if you are you will see a list of migrations with no ticks next to them
Run the following command python3 manage.py migrate to migrate the database structure from your project to the new database
Any data that you have added to your SQLite database will not transfer to the new one. You will need to populate the site on the deployed app once it is up and running or using Fixtures (JSON files with all your database content) if you have them. You can find out more about Fixtures and how to use them in the Django documentation.
Create a superuser for your deployed site and new database (this will allow you to check if the database is working and access the site admin on the deployed site) using the following command in the terminal: python3 manage.py createsuperuser and set up login details for them following the instructions.
Go to the ElephanySQL site, click on your database, go to the browser tab and click on 'table queries' and select 'auth_user (public)' and click on execute, you should see your newly created user.
You now need to remove your new database settings from settings.py and set it up to know which version of the site you are on (development or live) to know which database to use. Go back to your GitPod dashboard, click on your avatar to go your your GitPod user settings and select 'variables'
Add a key of DEVELOPMENT and a value of True
Got to your settings.py file to the DATABASES section and replace what's there with the following code (this checks to see if there is a value called DEVELOPMENT in your environment variables - ie your development environment, rather than the deployed app and sets the database accordingly.)
if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
Now that you have removed your ElephantSQL database url from the settings.py file it is safe to push your code to GitHub again. Your deployed database is set up and GitPod knows which one to use for which version of the site.
Deploying to Heroku
Create a Procfile in your app in the root directory with the following content web: gunicorn island_bees.wsgi:application and a blank line at the end.
Log in to Heroku using the GitPod terminal using the command `Heroku login`` and enter your Heroku email and password
if you have 2 factor authentication set up you will need to use Heroku login -i followed by your email and your Heroku API key as the password which you can find in your account settings on Heroku
Temporarily disable Heroku from collecting static files during deployment using the command heroku config:set DISABLE_COLLECTSTATIC=1 --app heroku-app-name
Commit your changes to GitHub using git add ., git commit & git push in the terminal
Then to deploy your site to Heroku use the command git push Heroku main
Your site will now be deployed without any of the static files (CSS, JavaScript & Media files)
In Heroku go to your app, click on activity to check if it has finished deploying and once it has go to the settings tab
Scroll down to 'Domains' and copy the 'your app can be found at' URL
Back in GitPod go to settings.py and add your deployed site's URL to the ALLOWED_HOSTS list
git add ., git commit & git push again and then git push Heroku main to push your changes
Once the site has finished deploying you should be able to navigate to the deployed site's URL and see your site content, though it will be a little strange-looking without CSS & media files!
You now need to replace the Django secret key in your settings.py (if you included it there) with an environment variable to keep it safe. To do this you can use a Django secret key generator online e.g. djecrety, copy the key it provides.
Go to your Heroku app's dashboard, open settings and reveal config variables and add a new variable with a key of SECRET_KEY and a value of what you just copied.
In GitPod, if you have used your secret key in settings.py, go back to your GitPod dashboard, click on your avatar to go your your GitPod user settings and select 'variables'
Add a key of SECRET_KEY and a value of a different Django secret key from your online key generator (djecrety or similar)
In settings.py and change the SECRET_KEY to SECRET_KEY = os.environ.get('SECRET_KEY', '')
Below it change the value of DEBUG to the following DEBUG = 'DEVELOPMENT' in os.environ to dynamically change whether the app is in DEBUG mode depending on whether it is the development or deployed site
git add ., git commit & git push again and then git push Heroku main to push your changes
You can also tell Heroku to automatically deploy so you don't need to push changes to both GitHub and Heroku each time - you'll find this under the Deploy tab on your Heroku app.
Setting Up Your Static Files on Your Deployed Site using Amazon Web Services (AWS)
There are many options for storing your static files for a deployed site, below are the instructions for using Amazon Web Services as a cloud storage provider.

Create an AWS account here (Select a personal account for the account type). You will need to fill in your information and card details to set up an account
Once your account is set up and you're signed in search for s3 in the search bar
Click on 'create bucket' and name it to match your Heroku app, selecting your closest region and uncheck 'block all public access' then click on create bucket to set it up
Click on your new bucket name and go to the properties tab
Scroll to the bottom and click on the edit button by 'Static Website Hosting' and select 'enable', giving default values for the index and error documents (index.html & error.html) then click save changes.
Go to the permissions tab and copy the ARN value at the top.
Scroll down to the bucket policy section, select 'edit' and 'policy generator'
Select 'S3 bucket policy' from the dropdown
In principles put a * to allow all
Set the action to 'Get Object'
Paste the earlier ARN value in the ARN input
Click on 'add statement' then 'generate policy'
Copy the policy text that the generator creates
Back in your bucket settings (should still be open in another tab) paste the text in to the Bucket Policy empty text area then add a '/*' to the end of the resource value (which should have your bucket name in it) this will allow access to all the resources in the bucket and click save
Scroll down to the access control list and grant Read and Write access to Everyone (public access) by checking the boxes
Scroll down to the Cross-Origin Resource Sharing (CORS) section and paste in the following and save:
[
    {
        "AllowedHeaders": [
            "Authorization"
        ],
        "AllowedMethods": [
            "GET"
        ],
        "AllowedOrigins": [
            "*"
        ],
        "ExposeHeaders": []
    }
]
Go back to your AWS dashboard by clicking on the AWS logo at the top left and type in IAM in the search bar and select the IAM service
Click on the user groups tab and create a new group, with the name of your choice, ideally with your app name in it and create the group
Go to the policies tab and create a policy, go the JSON tab and search for the S3FullAccess policy and import it
Edit the policy to the following:
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "s3:*",
            "Resource": [
                "arn:aws:s3:::bucket-name",
                "arn:aws:s3:::bucket-name/*",
            ]
        }
    ]
}
Click on next and then review
Name the policy and give it a description and then create your policy
Go to the User Groups tab, select your group and go to permissions and click 'add permissions' then 'attach policy' selecting your newly created policy and clicking 'Attach policies'
Create a user for the group by going to the User tab and clicking 'create user'
Name your user (you don't need to select AWS Console access) click next and add your user to your group clicking next as required and 'create user'
Download and save the csv file with the user's credentials - this is important, you will not be able to access this information again
Back in GitPod go to your settings.py file and paste in the following code which tells the app to look for an environment variable called USE_AWS and if it's there to use the following settings to access the static files.
if 'USE_AWS' in os.environ:
    # Cache control
    AWS_S3_OBJECT_PARAMETERS = {
        'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
        'CacheControl': 'max-age=94608000',
    }

    # Bucket Config
    AWS_STORAGE_BUCKET_NAME = 'island-bees'
    AWS_S3_REGION_NAME = 'eu-west-2'
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
Set up the following config variables in Heroku using the information in the csv file that you downloaded:
AWS_ACCESS_KEY_ID: your access key value
AWS_SECRET_ACCESS_KEY: your secret access key value
USE_AWS: True
Remove COLLECTSTATIC from the config variables in Heroku
Back in GitPod create a file called custom_storages.py in the root directory and add the following:
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION


class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION

In settings.py add the following to tell it to look for the new storage classes we just created in custom_storages and to override the URLS for static and media files. Put this just below the AWS code from earlier within the if 'USE_AWS' in os.environ statement.
# Static and media files
STATICFILES_STORAGE = 'custom_storages.StaticStorage'
STATICFILES_LOCATION = 'static'
DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'
MEDIAFILES_LOCATION = 'media'

# Override static and media URLs in production
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATICFILES_LOCATION}/'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIAFILES_LOCATION}/'

You're nearly there! Save your settings.py then push to add/commit/push to GitHub (if you've set up automatic deploys you won't need to also push to Heroku)
Once the deployment has finished check your S3 bucket, there should be a static folder in there with your static files (CSS / JS folders with files inside) and the live site should now have its CSS styling and any JavaScript functionality.
Finally to add your media files (images & video) simply go back to AWS, create a new folder called 'media' in the same place as the new 'static' folder, click on the folder and drag and drop all your media files in to the browser window.
Click next and under manage public permissions select 'grant public access to these objects' and click upload
Your site should now contain all your images, videos, styling and JavaScript! Well done!
Setting up Stripe Payments on your deployed site
Log in to Stripe, click on the developers tab and API keys copy the API key and set them in Heroku as config variables in the following:
STRIPE_PUBLIC_KEY: Stripe publishable key goes here
STRIPE_SECRET_KEY: Stripe secret key goes here
Back in Stripe set up a new webhook for your deployed site by clicking on webhooks, click on 'add endpoint' and paste in your deployed site's URL setting it to listen for all events.
Click on your newly set up webhook and click on 'Signing Secret' at the top to reveal the secret value. Copy it and set it as a new config variable in Heroku:
STRIPE_WH_SECRET: Signing secret from new webhook.