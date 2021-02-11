import requests
import time
from zipfile import ZipFile

from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class AddressSourceListOperator(BaseOperator):

    ui_color = '#358140'
    _scraped_folder = '/usr/local/airflow/scraped_files/'
    @apply_defaults
    def __init__(self,
                 table ='',
                 conn_id='',
                 scraped_folder='',
                 *args, **kwargs):

        super(AddressSourceListOperator, self).__init__(*args, **kwargs)
        self.table = table
        self.conn_id = conn_id
        self.scraped_folder = scraped_folder

    def execute(self, context):
        self.log.info("=============================-----================")
        self.log.info("Initialize posgres hook")
        pg_hook = PostgresHook(postgres_conn_id=self.conn_id, schema='address')
        conn = pg_hook.get_conn()
        cur = conn.cursor()
        cur.execute("select * from public.data_feed limit 1")
        rows = cur.fetchall()
        for r in rows:
            self.log.info("---------------")
            self.log.info(r[1])
            file_name = self.download_file(r[1])
            self.unzip_file(file_name)
            self.log.info("---------------")
        self.log.info("=============================-----================")

        self.log.info("Copying data from S3 to Redshift")


    def download_file(self, url):

        file_name = str(time.time()) +".zip"
        r = requests.get(url, allow_redirects=True)
        open(self.scraped_folder +"download_zip/"+ file_name, 'wb').write(r.content)

        return file_name

    def unzip_file(self, file_name):

        zip_file = self.scraped_folder +"download_zip/"+ file_name

        with ZipFile(zip_file, 'r') as zip:
            self.log.info(zip.printdir())
            self.log.info('Extracting all the files now...')
            zip.extractall(self.scraped_folder +"/new/")
            self.log.info('Done!')