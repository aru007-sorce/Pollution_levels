from datetime import datetime
from sqlalchemy import create_engine
import os
import pandas as pd
import requests
from dotenv import load_dotenv
load_dotenv()


DB_URL = os.getenv("DB_URL","postgresql://postgres:1234@localhost:5432/airquality")


def generate_summary(db_url):
    engine = create_engine(db_url)
    df = pd.read_sql("SELECT * FROM airindex_long;", engine)

    # Ensure 'date' is datetime
    df["date"] = pd.to_datetime(df["date"])

    # Daily average
    #filtered_df = df[df["parameter"] == "PM2.5"]
    daily_summary = (
        df.groupby(["city", "date", "parameter", "category"])
        .agg({"value": "mean"})
        .reset_index()
    )
    daily_summary.to_csv("daily_summary.csv", index=False)

    # Weekly high/low/avg
    df["week"] = df["date"].dt.strftime("%Y-%W")

    weekly_summary = (
        df.groupby(["city", "parameter", "category", "week"])
        .agg({"value": ["min", "max", "mean"]})
        .reset_index()
    )
    weekly_summary.columns = [
        "city",
        "parameter",
        "category",
        "week",
        "min",
        "max",
        "avg",
    ]
    weekly_summary.to_csv("weekly_summary.csv", index=False)

    return "Summaries successfully generated!"


print(generate_summary(DB_URL))
