# capstone-API
This is Algoritma's Python for Data Analysis Capstone Project. This project aims to create a simple API to fetch data from 'chinook.db'. 

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
- Deploy to Heroku
- Build API Documentation
- Implements data wrangling

___
We have deployed a simple example on : https://api-capstone.herokuapp.com
Here's the list of its endpoints: 

1. /emp, method = GET
Static Endpoint, returning all data of employee. 

2. /media/<md_id>, method = GET
Dynamic Endpoint, returning total sales from country base on media type
    
3. /media/<md_id>, method = GET
Dynamic Endpoint, returning total sales base on country

If you want to try it, you can access (copy-paste it) : 
- https://api-capstone.herokuapp.com

