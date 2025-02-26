# From : base images
FROM python:3.9.1  

# run command download the package into this image
RUN pip install pandas sqlalchemy psycopg2 

WORKDIR /app
COPY ingest_data.py ingest_data.py

# run docker pipline auto
ENTRYPOINT [ "python","ingest_data.py" ]