# Iowa Vodka Sales Application
## Table of Contents:

1. [Presentation Slides](https://github.com/leahnagy/liquor_predictor/blob/main/slides_liquor_app.pdf)
2. [Exploratory Data Analysis]()
3. [Sales Forecasting with Facebook Prophet]()
4. [Dash App Code]()

## Check Out the Application
[Iowa Vodka Sales App](https://leahs-liquor-app.herokuapp.com)

## Abstract
The goal of this project was to create an insightful web/mobile application based on historical data of Iowa Vodka sales that can inform producers, retailers and Iowa's Alcoholic Beverages Division about past and future sales trends. I worked with data provided by Iowa.gov to extract past sales information and created future sales forecasting using Facebook Prophet. Using Dash and Heroku, key insights are available in a user-friendly application.


## Data
After filtering the data to include only Vodka products sold from 01/01/2018 - 08/01/2022 in the state of Iowa, there were 2,825,713 sales transactions with 24 features. Some of the features included product description, manufacturer, sales(USD), sales(Liters), and bottle size. The data was directly downloaded from a CSV file from [data.iowa.gov](https://dev.socrata.com/foundry/data.iowa.gov/m3tr-qhgy) where you can also import the data via the Socrata API. 

## Data Pipeline
<img width="1327" alt="Screen Shot 2022-09-06 at 12 28 29 PM" src="https://user-images.githubusercontent.com/89696586/188687988-d48cd538-2f11-4acd-bb92-dc661f3e3593.png">


## Tools
- SQLite, Numpy and Pandas for data manipulation and EDA
- Plotly for interactive visualizations
- Facebook Prophet for future sales forecasting
- Dash to create the application
- Heroku to deploy app globally

## Communication
In addition to the slides and visuals presented, this project will be embedded on my GitHub site along with an article describing the steps of the project in detail on my personal blog. 

