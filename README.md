# Data Engineering Project
## Iowa Vodka Sales Application
Created By: Leah Nagy

### Table of Contents:
1. [Presentation Slides](https://github.com/leahnagy/liquor_predictor/blob/main/slides_liquor_app.pdf)
2. [Exploratory Data Analysis]()
3. [Sales Forecasting with Facebook Prophet]()
4. [Dash App Code]()
5. [Experience the Application](https://leahs-liquor-app.herokuapp.com)

### Project Overview
This project aimed to deliver an intuitive web/mobile application that elucidates historical trends and future projections of Iowa's Vodka sales. This tool serves to provide valuable insights for producers, retailers, and the Iowa Alcoholic Beverages Division. The application was developed based on data sourced from Iowa.gov, with Facebook's Prophet used for forecasting future sales. The application was built using Dash and deployed on Heroku for global accessibility.

### Dataset
The dataset consists of 2,825,713 sales transactions pertaining to Vodka products sold in the state of Iowa from January 1, 2018, to August 1, 2022. Each transaction comes with 24 features such as product description, manufacturer, sales in USD, sales in liters, and bottle size. The data was obtained directly from data.iowa.gov via a CSV file. Alternatively, it can also be imported through the Socrata API.

### Data Pipeline
The following is a snapshot of the data pipeline used for this project:<img width="1327" alt="Screen Shot 2022-09-06 at 12 28 29 PM" src="https://user-images.githubusercontent.com/89696586/188687988-d48cd538-2f11-4acd-bb92-dc661f3e3593.png">


### Tools Utilized
- Data manipulation and exploratory data analysis (EDA): SQLite, Numpy, and Pandas
Interactive visualizations: Plotly
Future sales forecasting: Facebook Prophet
Application development: Dash
Application deployment: Heroku

