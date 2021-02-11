import shutil
import glob
import pymongo
import pandas as pd
import os

from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.hooks.http_hook import HttpHook

class ProcessAddressOperator(BaseOperator):

    ui_color = '#CC81DD'

    @apply_defaults
    def __init__(self,
                 table ='',
                 conn_id='',
                 scraped_folder='',
                 *args, **kwargs):

        super(ProcessAddressOperator, self).__init__(*args, **kwargs)
        self.table = table
        self.conn_id = conn_id
        self.scraped_folder=scraped_folder

    def execute(self, context):
        self.log.info("Extractin data from new files")
        self.extract_data_from_file()
        self.log.info("Clear processed files")
        self.delete_processed_files()
        self.log.info("Finish")

    def extract_data_from_file(self):

        post_data = []
        for filename in glob.iglob(self.scraped_folder +"new/" + '**/*.csv', recursive=True):
            df = pd.read_csv(filename)
            for index, row in df.iterrows():
                dictionar = {"lon": row["LON"], "lat": row["LAT"], "number": row["NUMBER"], "street": row["STREET"],
                             "unit": row["UNIT"], "city": row["CITY"], "district": row["DISTRICT"],
                             "region": row["REGION"], "postcode": row["POSTCODE"], "id": row["ID"], "hash": row["HASH"]}
                post_data.append(dictionar)

                if index % 10000 == 0:
                    self.save_data_to_mongo(post_data)
                    post_data.clear()
            if len(post_data) > 0:
                self.save_data_to_mongo(post_data)

        return None

    def save_data_to_mongo(self, data):

        self.log.info("Insert data to mongo")

        client = pymongo.MongoClient("mongodb://root:example@mongo:27017")
        db = client['spanish_address']
        posts = db.posts

        result = posts.insert_many(data)

        self.log.info("{} records have been inserted in mongodb".format(len(result.inserted_ids)))

        return None

    def delete_processed_files(self):

        location = self.scraped_folder +"new/"
        for entry in os.scandir(location):
            if os.path.isfile(os.path.join(location, entry)):
                os.remove(os.path.join(location, entry))
            else:
                shutil.rmtree(os.path.join(location, entry))

        return None