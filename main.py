from datetime import datetime
import pandas as pd
from dags.services.Final_def import run_etl
from sqlalchemy import create_engine



if __name__ == "__main__":
    run_etl()
