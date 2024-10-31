# SustainLuxe - Shop luxurios and Sustainable

## Table of Contents

### [About](#about)

SustainLuxe is a second Hand Shop online for designer clothes.
You find a careful selection of clothes and accessories with quality made only by designers.
Second Hand market grows fast!
The reason for increased shopping in second Hand market is because of financial reason,
but the next as much is environmental reason and it has become a trendy way of shopping.
I will keep it luxury and financial giving, while I will be part of environmental participation.
Through my shop I will be a part of saving the word, through impact people to aknowledge the Second Hand effect 
and donate a part of the revenue to an important organisation to help environmental impact.

I think a lot of people is to busy to take their time for selling unused clothes, so my idea is to make it simple to sell, buy and collect revenues.

You are welcome to visit my store and get to know more!

Live web site: https://sustainluxe-b6e840083c68.herokuapp.com/

I have thinking of this idea for some years and in the meantime, the buissness of Second Hand is growing, so I´m happy to present this fictive busisness.
This is a Full-Stack project with Django.

### [Marketing research](#marketing-research) 

I started to make research to update me of this market and to investigate the footprint and Carbon effect of shopping behaviors.
[You can read more of my SEO and Marketing research here](seo_marketing_research.md)

I also made a SEO research to get strong SEO words to use for high ranking in Google.
Read more about SEO here(#seo_marketing_research.md)

### [Media](#media)
* https://stocksnap.io/
* https://www.istockphoto.com/
* https://www.alamy.com/stock-photo
* https://clossue.com/eu/blog
* http://almonds.ai  
* https://urbanswall.com/luuxly-com-your-destination-for-luxury-fashion-and-lifestyle/
* https://www.lifestyleasia.com/ind/style/fashion/second-hand-luxury-is-the-new-sustainable-trend/



### [Agile method](#agile-method) 

After research of other e-commerce and similar Second Hand Stores, I also brainstormed what I want to achieve and how to plan the project.

#### [Concept Chart](#static/images/Readme_img/concept_chart_sustainLuxe.png)
I created de a concept chart to have an idea to stick with.
I used Lucid chart to my concept chart and buisness model.

### [Buisness Model](#buisness_model)
The business operates on a C2C model (Consumer-to-Consumer) and revenue comes from administration fee and profit share of the selling price.
The emphasis is on the traffic to the e-commerce and it should feel more serious and luxury to buy from credible and attractive design store.
Focus is also to make people consious of Sustainable choices, Climate Controll and how to make resposible of their purposes without reduce the quality.
Key features is to sell used stuff easily and quick without own commitment needed.
I added a buisness process to formulate the different modules I will work on
![Buisness Process](#static/images/Readme_img/sustainlux_buisnessprocess.png)

#### [ERD](#erd)
I planned and skiss the models in [Google Drive ](https://drive.google.com/file/d/1SYwaMzGs6PuOuEuA6Yi4T2Q0p8dvmSvd/view?usp=sharing)
There are different modules since the product is for both selling and buying.
It got mixed up between Products app and Profiles app, since I had Product model in both but in different use.
Then I changed Product model in Profiles app to Sale model to separate them.

![Product Model](#static/images/Readme_img/Sustainluxe_productmodel.png)
![Order Model](#static/images/Readme_img/Sustainluxe_ordermodel.png)
![User Model](#static/images/Readme_img/sustainluxe_usermodel.png)


#### [User Stories](#user-stories)
I set up a project in Github https://github.com/users/Christina5P/projects/8/views/1?layout=board
In this the method are divided into  
- Milestones
![Milestones](#static/images/Readme_img/milestones.png)
  - EPICS
  In every milestone, there is divided in EPICS, for ex.
  ![EPICS](#static/images/Readme_img/epics.png)
    - User stories
    In EPICS, it is divided to userstories, for ex.
    ![Userstories](#static/images/Readme_img/userstories.png)
      - Tasks
      There could also be some tasks.


#### [wireframes](#wireframes)  

### [UX](#ux)
Goal to keep good UX principles regarding layout/colors/interaction
Responsive for different devices.

### [Design] (#design) 

- Logotype is created to simulate fun, but conscious and responsible shopping.  

- Font: Oswald 700

- Colors: 
  Logo, slogan #3c5c65
  Font #637c83
 ![colors](colors.png)

- Favicon

### [Features](#features) 

#### [Existing Features](#existing_featuers)

-Navbar
-Registration/Log in Page
-Profile Page
-Shopping page
-Category search
-Filter
-Product detail
-Shopping Bag
-Checkout 
-About us
-Customer service
-Product Management
- Footer
-Error page

#### [Future Features](#future_features)

### [Marketing](#marketing)

-Facebook
-Newsletter
-TikTok


### [Technologies Used](#technologies_used)

* GitHub
* GitPod
* Stripe

#### Languages:
-HTML
-CSS
-Python
-JS

#### Frameworks and libraries:
-Django
-MBD (Bootstrap)
-Psycopg2: the database driver used to connect to the database.
-Django-allauth: the authentication library used to create the user accounts.
-Django-crispy-forms: was used to control the rendering behavior of Django forms.
- Mailchimp

#### Databases:
SQLite: was used as a development database.
PostgreSQL: the database used to store all the data.
AWS Web Services


### [Testing](#testing)

#### [Validators](#validators)

- W3C Validator: was used to validate HTML5 code for the website.
Result:

- W3C CSS validator: was used to validate CSS code for the website.
Result:
- JShint: was used to validate JS code for the website.
Result:
- PEP8: was used to validate Python code for the
Result:

#### [Responsiveness](#responsiveness)

#### [Lighthouse](#lighthouse)

#### [Manual Testing](#manual_testing) 

### [Bug Report](#bugreport)

### [Deployment](#deployment) 

SustaineLuxe is host on GitHub and deployed on Heroku

### [Credits](#credits)

* https://app.logomaster.ai/ - help making a logotype
* https://www.colorhexa.com/ - Colorscheme
* https://climatepartnerimpact.com/get-involved/ - derivation to a project for donation
* http://lucid.app - Creating a concept Plan
* https://fontawesome.com/ -font awesome icons
* https://www.istockphoto.com/ -pictures
* https://pypi.org/project/psycopg2/ -tutoring psycopg2

* 
### [Acknowledgements](#acknowledgements)

- Tutoring, Q&A and criteria videos in slack channel project-potfolio-5-e-commerce
- Inapiration from others PP5 projects
- walk through Boutique Ado
- https://www.youtube.com/watch?v=hZYWtK2k1P8 -tutoring stripe payment
- https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax

- https://www.bigcommerce.com/articles/ecommerce/fashion-ecommerce/
- https://python.plainenglish.io/creating-a-django-e-commerce-product-filter-prototype-a8e7409453fc -creating filter tutoring
- https://stackoverflow.com/ - -creating filter tutoring
- https://dev.to/earthcomfy/django-user-profile-3hik -profile tutoring
- https://www.paleblueapps.com/rockandnull/django-user-profile/
- https://docs.djangoproject.com/en/5.1/howto/custom-management-commands/ - tutoring create accounts
- https://simpleisbetterthancomplex.com/tutorial/2018/08/27/how-to-create-custom-django-management-commands.html 
- https://www.youtube.com/watch?v=9X83BZ1cF7o - tutoring request cycle
- https://simpleisbetterthancomplex.com/tutorial/2018/08/27/how-to-create-custom-django-management-commands.html - tutoring manage commands
- https://groups.google.com/g/django-users/c/aSj3jGX2CLk -tutoring expire date
- https://stackoverflow.com/questions/49366010/how-to-set-an-expiry-date-for-an-object-in-django 
- https://django-simple-history.readthedocs.io/en/latest/ 
- https://medium.com/django-unleashed/mastering-the-art-of-django-simple-history-a-tutorial-for-medium-with-examples-c25196339130


