import os
import pandas as pd
from sqlalchemy import create_engine

# get current working directory
cwd = os.getcwd()

# path to csv files
measurements_path = os.path.join(cwd, 'hawaii_measurements.csv')
stations_path = os.path.join(cwd, 'hawaii_stations.csv')
# read csv files into pandas dataframes
measurements_df = pd.read_csv(measurements_path)
stations_df = pd.read_csv(stations_path)

# create sqlalchemy engine and save dataframes to sqlite
engine = create_engine('sqlite:///hawaii.sqlite')
measurements_df.to_sql('measurements', engine, if_exists='replace', index=False)
stations_df.to_sql('stations', engine, if_exists='replace', index=False)

# confirm data was added to sqlite
print(engine.execute("SELECT * FROM measurements LIMIT 5").fetchall())
print(engine.execute("SELECT * FROM stations LIMIT 5").fetchall())