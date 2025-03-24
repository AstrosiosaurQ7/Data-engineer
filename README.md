# Data-engineer
Data engineer project and practice
💭 DE zoom camp week 1
 🎥Ingesting NY Taxi Data to Postgres WORKFLOW
🥨 cd /d/BrownUniversity/DE_camp/01-exe
🥨 docker volume create vol-pgdata
🥨 docker run -it \
-e POSTGRES_DB=ny_taxi \
-e POSTGRES_USER=postgres \
-e POSTGRES_PASSWORD=postgres \
-v vol-pgdata:/var/lib/postgresql/data \
-p 5432:5432 \
--name pgdatabase \
postgres:17-alpine
🥨 python -m pgcli -h localhost -U postgres -d ny_taxi

-------------------------------notes---------------------------------
📒 postgres:17-alpine is an official image, so it can be run directly without the need to build a new image.
🚀 You can think of docker build as:
📦 Packaging a new image from a Dockerfile → 🏗️ Saved locally → 🔥 Can be run with docker run!

📒 vol-pgdata is just a volume name and can be changed to any other name. Its purpose is to persist PostgreSQL data (even if the container stops or is deleted, the volume remains).
Volume Management Commands :
1. docker volume ls
2. docker volume create my_pg_data
3. docker volume rm my_pg_data
4. docker volume inspect <VOLUME_NAME>
5. docker volume prune (⚠Remove all unused volumes)
🥭 Docker Volume can be understood as a locally stored database, but essentially, it is a persistent storage mechanism that exists independently of the container lifecycle.

🎥Load the data into PostgreSQL with Pandas

🥨 pd.io.sql.get_schema(df, con=engine) does not directly create a table in PostgreSQL. It only generates the CREATE TABLE statement but does not execute it. The con=engine ensures the generated SQL is compatible with PostgreSQL syntax.

🥨 pd.to_datetime(arg, errors='raise', format=None, unit=None, utc=False)
 This function is used to convert data to the datetime64 type for time series data processing.
⚠️ Error handling: Values that cannot be converted become NaT → SQL does not recognize NaT, so it needs to be converted to None (SQL NULL) or NaN.

🥨 engine = create_engine('postgresql://postgres:postgres@localhost:5432/ny_taxi')
📌 This connects to the Docker PostgreSQL database using the localhost:5432 port mapping to find the pgdatabase container.

🧀 SELECT COUNT(1) FROM yellow_taxi_data
 How SQL count(1) works:
 For each row, SQL only counts non-NULL values. Since 1 is a constant and can never be NULL, every row will be counted.
📌 COUNT(column_name) counts the number of non-NULL values in the specified column, only counting rows where column_name is not NULL.

📒 Postgres prompt command: pg shell commands
\dt → View the database.
\d yellow_taxi_data → Describe the table.

----------------------------Notes------------------------------
🎆 【When a container is paused and needs to be restarted】
1. Check container status with docker ps👉If the container is running → Connect to the PostgreSQL database directly:
python -m pgcli -h localhost -U postgres -d ny_taxi
2. If the STATUS is "Exited", you need to start the container: 
docker start <container_name_or_id>
3. In Git Bash, how to enter the container:
winpty docker exec -it pgdatabase //bin/sh
