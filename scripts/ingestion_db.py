import pandas as pd 
import os
from sqlalchemy import create_engine
import logging
import time

os.mkdir('logs')

logging.basicConfig(
    filename="logs/ingestion_db.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

engine=create_engine('sqlite:///inventory.db')

def ingest_db(chunk, table_name, engine, if_exists_mode):
    '''this function will ingest the dataframe into database table'''
    chunk.to_sql(table_name, con=engine, if_exists=if_exists_mode, index=False)

def load_raw_data():
    '''this function will load the CSVs as dataframe and ingest into db'''
    chunk_size = 1000000  # or 100000 depending on your system
    start = time.time()
    for file in os.listdir('data'):
        if file.endswith('.csv'):
            table_name = file[:-4]
            first_chunk = True
            for chunk in pd.read_csv('data/' + file, chunksize=chunk_size):
                logging.info(f'Ingesting {file} in db')
                if first_chunk:
                    ingest_db(chunk, table_name, engine, 'replace')
                    first_chunk = False
                else:
                    ingest_db(chunk, table_name, engine, 'append')
    end = time.time()
    total_time = (end - start) / 60
    logging.info('--------------Ingestion Complete--------------')
    logging.info(f'\nTotal Time Taken: {total_time} minutes')

if __name__=='__main__':
    load_raw_data()