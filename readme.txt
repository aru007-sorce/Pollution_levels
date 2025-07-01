# Air Index Pipeline

This project is an ETL pipeline that fetches  air quality data for a particular day for selected cities using the (https://api.ambeedata.com/latest/by-city) EXtract, transforms, and loads it into a PostgreSQL database.

# You need to generate your personal API KEY from the website and use it in the project as they provide free trial for the limited time per key
## 🧰 Technologies Used
- Python
- Apache Airflow
- Pandas
- Requests
- SQLAlchemy
- PostgreSQL (via Docker Setup)
- Docker & Docker Compose

## 📁  Project final Structure here

```
pollution_levels/
├── final_def.py                # ETL script and All functions
|-- main.py
|-- report.py               # Generate Weekly and Daily Reports 
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker build for ETL script
├── docker-compose.yml      # Docker setup for ETL + PostgreSQL
└── .env                    # Environment variables

```

## Setup Project

Set up a virtual environment (using latest Python 3 + `venv` module):

```shell
# for root directory
python -m venv .venv
```

## Development

Install project dependencies:

```shell
# for root directory
source .venv/bin/activate   # for windows use Scripts in place of bin
pip install -r requirements.txt
```



Start essential services:

```shell
# docker compose up --build -d For first time build
docker compose up -d
```



This will:
- Start a PostgreSQL container (`user: postgres`, `password: 1234`, `db: airquality`)
- Run the ETL pipeline container (waits for PostgreSQL to be ready and loads data)

### 4. Re-run the ETL Job

You can run the ETL manually anytime by:

```
docker-compose run --rm etl
```

### 5. Connect to the PostgreSQL Database

You can connect using any PostgreSQL client:

```
Host: localhost
Port: 5432
User: postgres
Password: 1234
Database: airquality                                               
```

Or use `psql`:
 
```
docker exec -it <postgres_container_id> bpsql -U user -d weatherd
```

### 6. Schedule the ETL Job (Optional)

You can add cron-like scheduling by modifying the Docker command:

```
command: ["sh", "-c", "while true; do python etl.py; sleep 3600; done"]
```

Alternatively, integrate with Apache Airflow for advanced scheduling.

---

## 🧪 Sample Query

```sql
SELECT * FROM weather ORDER BY time DESC LIMIT 10;
```

---

## ✅ Supported Cities

-New York
-London
-Paris
-Singapore
-Beijing
-Los Angeles
-Dubai
-Mumbai
-Hyderabad
-Ahmedabad 
-Pune
-Delhi

Modify the `CITY` List in `final.py` to add more.

---

Before committing/pushing code, run below commands to format code:

```shell
# format *.{json,yml} etc.
npx prettier . --write

# format python code
black .
```
