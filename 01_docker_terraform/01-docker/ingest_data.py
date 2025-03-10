import os
import argparse
from time import time
import pandas as pd
from sqlalchemy import create_engine


def main(params):
    user = params.user
    password = params.password
    host = params.host 
    port = params.port 
    db = params.db
    table_name = params.table_name
    url = params.url

    # the backup files are gzipped, and it's important to keep the correct extension
    # for pandas to be able to open the file
    # if url.endswith('.csv.gz'):
    #     csv_name = 'output.csv.gz'
    # else:
    #     csv_name = 'output.csv'
    csv_name = 'output.csv'
    os.system(f"wget {url} -O {csv_name}")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # read the data into chunk
    # df_iter = pd.read_csv('yellow_tripdata_2021-01.csv', iterator=True, chunksize=100000)
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)
    df = next(df_iter)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime,errors='coerce')
    df['tpep_pickup_datetime'] = df['tpep_pickup_datetime'].where(df['tpep_pickup_datetime'].notna(), None)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime,errors='coerce')
    df['tpep_dropoff_datetime'] = df['tpep_dropoff_datetime'].where(df['tpep_dropoff_datetime'].notna(), None)

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    i = 0
    while i <= 8 :
        t_start = time()
        df = next(df_iter)
        
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime,errors='coerce')
        df['tpep_pickup_datetime'] = df['tpep_pickup_datetime'].where(df['tpep_pickup_datetime'].notna(), None)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime,errors='coerce')
        df['tpep_dropoff_datetime'] = df['tpep_dropoff_datetime'].where(df['tpep_dropoff_datetime'].notna(), None)
        
        df.to_sql(name=table_name, con=engine, if_exists='append')
        i += 1
        
        t_end = time()
        print('inserted another chunk...%.3f second' %(t_end - t_start))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')
    parser.add_argument('--table_name', required=True, help='name of the table where we will write the results to')
    parser.add_argument('--url', required=True, help='url of the csv file')

    args = parser.parse_args()
    print(args)
    main(args)




