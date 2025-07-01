FROM apache/airflow:latest

USER root

# Install Git
RUN apt-get update && \
    apt-get -y install git && \
    apt-get clean

# Switch back to airflow user
USER airflow

# Set working directory
WORKDIR /app

# Copy your app and requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py ./

# Set the default command
CMD ["python", "main.py"]
