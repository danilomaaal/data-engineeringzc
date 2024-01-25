import os
import argparse
import pandas as pd
from sqlalchemy import create_engine
from time import time

def main():
    
    parser = argparse.ArgumentParser(description='Ingest data from any given url')
    
    parser.add_argument('--user', help='the user name for postgres')
    parser.add_argument('--password', help='password for accesing postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--database', help='database name for postgres')
    parser.add_argument('--table-name', help='name of the table to process')
    parser.add_argument('--url', help='url of the file')
    
    args = parser.parse_args()

    # get data 
    os.system('mkdir data')
    os.system(f'wget {args.url} --directory-prefix data/')
    zippedfile = os.popen('find -name "*.gz"').read()
    print(f'location is: {zippedfile}')
    os.system(f'gzip -d {zippedfile}')
    csv_file = os.popen('find -name "*.csv"').read().strip()

    engine = create_engine(f'postgresql://{args.user}:{args.password}@{args.host}:{args.port}/{args.database}')

    chunk = pd.read_csv(csv_file, iterator=True, chunksize=100000)
    data = next(chunk)
    
    data['tpep_pickup_datetime'] = pd.to_datetime(data['tpep_pickup_datetime'])
    data['tpep_dropoff_datetime'] = pd.to_datetime(data['tpep_dropoff_datetime'])
    # create table
    data.head(n=0).to_sql(name=args.table_name, con=engine, if_exists='replace')

    data.to_sql(name=args.table_name, con=engine, if_exists='append')
    
    
    while True:
        start = time()
        data = next(chunk)
        
        data['tpep_pickup_datetime'] = pd.to_datetime(data['tpep_pickup_datetime'])
        data['tpep_dropoff_datetime'] = pd.to_datetime(data['tpep_dropoff_datetime'])

        data.to_sql(name=args.table_name, con=engine, if_exists='append')
        end = time()
        print('Appended another chunk: took %.3f seconds.' % (end-start))



if __name__ == '__main__':
    main()