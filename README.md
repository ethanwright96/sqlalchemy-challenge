# sqlalchemy-challenge

# Climate Analysis in Honolulu, Hawaii

![alt](https://github.com/ethanwright96/sqlalchemy-challenge/blob/main/SurfsUp/Results/monthly_precipitation_boxplot.png)

## Before You Begin
1. Create a new repository for this project called "sqlalchemy-challenge". Do not add this assignment to an existing repository.
2. Clone the new repository to your computer.
3. Inside your local Git repository, create a directory for this challenge, such as "SurfsUp".
4. Add the Jupyter notebook (climate_starter.ipynb) and app.py files to the "SurfsUp" directory. Also, add the "Resources" folder containing the data files.
5. Push the changes to GitHub or GitLab.

## Files
Download the following files for the project:
[Module 10 Challenge files](https://...link...)

## Part 1: Analyze and Explore the Climate Data
In this section, you will use Python and SQLAlchemy to perform a basic climate analysis and data exploration of the climate database. Follow these steps:

1. Use SQLAlchemy's `create_engine()` function to connect to the SQLite database.
2. Reflect the tables into classes using SQLAlchemy's `automap_base()` function. Save references to the classes named "station" and "measurement".
3. Create a session to link Python to the database. Remember to close the session at the end.
4. Perform a precipitation analysis by finding the most recent date and retrieving the previous 12 months of precipitation data.
5. Load the query results into a Pandas DataFrame, sort them by date, and plot the results.
6. Use Pandas to print the summary statistics for the precipitation data.
7. Perform a station analysis by calculating the total number of stations in the dataset and finding the most active stations.
8. Design a query to retrieve the previous 12 months of temperature observation (TOBS) data for the most active station. Plot the results as a histogram.
9. Close the session.

![alt](https://github.com/ethanwright96/sqlalchemy-challenge/blob/main/SurfsUp/Results/mean_daily_precipitation_plot.png)

## Part 2: Design Your Climate App
Now, design a Flask API based on the queries and analysis from the previous steps. Create the following routes using Flask:

- `/`: Homepage that lists all available routes.
- `/api/v1.0/precipitation`: Convert the last 12 months of precipitation analysis results to a JSON dictionary and return it.
- `/api/v1.0/stations`: Return a JSON list of stations from the dataset.
- `/api/v1.0/tobs`: Query the temperature observations of the most active station for the previous year and return them as a JSON list.
- `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`: Return a JSON list of minimum, average, and maximum temperatures for a specified start or start-end range.

*Note: Replace `<start>` and `<end>` in the routes with actual start and end dates.*

Remember to close your session at the end of the Jupyter notebook.
