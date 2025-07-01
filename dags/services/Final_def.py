import pandas as pd
import requests
from sqlalchemy import create_engine
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

 
# Configration

city = [
    "New York",
    "London",
    "Paris",
    "Singapore",
    "Beijing",
    "Los Angeles",
    "Dubai",
    "Mumbai",
    "Hyderabad",
    "Ahmedabad",
    "Pune",
    "Delhi",
]
params_template = {}
URL_WEB = "https://api.ambeedata.com/latest/by-city"
DB_URL = os.getenv("DB_URL")
api_key = os.getenv("API_KEY")
headers = {"x-api-key": api_key}


# Extraction
def fetch_weather_data(city):
    params = params_template.copy()
    params.update({"city": city})
    response = requests.get(URL_WEB, params=params, headers=headers)
    response.raise_for_status()
    return response.json()


# Transformation
def transform_weather_data(raw_data):
    stations = raw_data.get("stations")
    if not stations:  # Check if 'stations' key exists and is not empty
        return None  # Return None if no station data

    # Assuming there's always at least one station if 'stations' is not empty
    stations_data = dict(stations[0])

    flat_dict = {}

    for key, value in stations_data.items():
        if isinstance(value, dict):
            flat_dict.update(value)  # Merge inner dictionary
        else:
            flat_dict[key] = value

    df = pd.DataFrame([flat_dict])
    df["updatedAt"] = pd.to_datetime(df["updatedAt"])
    df["updatedAt"] = df["updatedAt"].dt.date
    # Removed redundant concat here
    df.drop(
        columns=[
            "state",
            "division",
            "lat",
            "lng",
            "placeName",
            "postalCode",
            "pollutant",
            "concentration",
            "countryCode",
        ],
        inplace=True,
    )

    # Melt the DataFrame

    long_df = pd.melt(
        df,  # used the combined dataframe
        id_vars=["city", "AQI", "updatedAt", "category"],
        value_vars=["CO", "NO2", "OZONE", "PM10", "PM25", "SO2"],
        var_name="Parameter",
        value_name="Value",
    )

    # Rename columns
    long_df = long_df.rename(columns={"updatedAt": "date"})

    # Return the melted DataFrame as it seems this is the desired format for loading
    return long_df


# Loading
def load_to_postgres(df, db_url):
    engine = create_engine(db_url)
    with engine.connect() as conn:
        df.columns = df.columns.str.lower()
        # Ensure the table name is consistent with the melted DataFrame structure
        df.to_sql("airindex_long", con=conn, if_exists="append", index=False)


# ETL Pipeline
def run_etl():

    final_data_list = (
        []
    )  # Renamed to avoid confusion with the final concatenated DataFrame
    for i in city:
        try:
            pollution_data = fetch_weather_data(i)
            df = transform_weather_data(pollution_data)

            if df is not None:  # Check if transformation returned a DataFrame
                print(f"Successfully processed data for {i}:")
                final_data_list.append(df)
            else:
                print(f"No station data found for {i}.")

        except requests.exceptions.HTTPError as e:
            print(f"Error fetching data for {i}: {e}")
        except Exception as e:
            # Catch any other potential errors during transformation or processing
            print(f"An unexpected error occurred for {i}: {e}")

    # Check if any data was collected before attempting concatenation
    if final_data_list:
        final_df = pd.concat(final_data_list, ignore_index=True)
        print(f"Loading data into PostgreSQL...")
        load_to_postgres(final_df, DB_URL)
        print("ETL completed successfully.")
    else:
        print(
            "No data was successfully processed for any city. ETL completed with no data loaded."
        )
