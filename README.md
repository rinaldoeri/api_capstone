# capstone-API
This is Algoritma's Python for Data Analysis Capstone Project. 
This project aims to create a simple API to fetch data from 'chinook.db'. 

we demand data to be accessible. And we create an API for anyone who are granted access to the data for collect them and get the information from data. 
In this capstone project, we create Flask Application as an API and deploy it to Heroku Web Hosting. 

You can check the rubrics as below
___
## Dependencies : 
- Pandas    (pip install pandas)
- Flask     (pip install flask)
- Gunicorn  (pip install gunicorn)

___
## Goal 
- Create Flask API App
- Implements data wrangling
- Build API Documentation
- Deploy to Heroku

___
We have deployed a simple example on : https://api-app-capstone.herokuapp.com/
Here's the list of its endpoints: 

1. /employee, method = GET
Static Endpoint, returning all data of employee. 

2. /media/<md_id>, method = GET
Dynamic Endpoint, returning total sales from country base on media type.
input md_id with one of the MediaTypeId as below :
- 1 (MPEG audio file)
- 2 (Protected AAC audio file)
- 3 (Protected MPEG-4 video file)
- 4 (Purchased AAC audio file)
- 5 (AAC audio file)
    
3. /country/<country_nm>, method = GET
Dynamic Endpoint, returning total sales base on country.
input country_nm with the country name

4. /albums, method = GET
Static Endpoint, returning total sales and mean of album.

5. /sales, method = GET
Static Endpoint, returning total sales of Sales Support Agent per-month period.

If you want to try it, you can access (copy-paste the link as below) : 
- https://api-app-capstone.herokuapp.com/employee
- https://api-app-capstone.herokuapp.com/media/3
- https://api-app-capstone.herokuapp.com/country/Germany
- https://api-app-capstone.herokuapp.com/albums
- https://api-app-capstone.herokuapp.com/sales


## Deploy Flask API to heroku App
For deploy the API App to heroku follow the step as below :
- go to https://www.heroku.com/ and login
- klik New -> klik Create new app
- Input App name (the app name must be unique)
- klik Create app

Now the heroku app has been created, 
the next step is connected the heroku app with github repository.
- Select Deploy
- In Deployment method, klik GitHub
- klik Search to find github repository and select it
- klik Deploy Branch

now the heroku app has been connected with github repository,
and the API is ready to run.
