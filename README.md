# airflow-flask-pipeline
Demo pipeline with Airflow, PostgreSQL, MongoDB, and Rest API to consume the data  with Flask


## Description
In this project I've used as a datasource Openaddresses.io. In Airflow is defined a DAG  called Spanish Address and in it we have 2 operators.  
- `address_source_list` first will read from PostgreSql the table `data_feed` the first set  that need to be proccessed and it will download the zip file, store it on `scraped_files/download_zip` folder and after that  unzip it to `scraped_files/new` folder. 
- `process_address` will read the folder `scraped_files/new` and search for `csv` files and each file is stored on pandas dataframe which is iterated row by row and each 10000 records are sent it to MongoDb. After all  the records are stored the folder `scraped_files/new` is cleared in order to perseve storage space.

There is also a Flask Rest API build that read data from MongoDb.  
The endpoint /search accept as input a json for example if we put `{"street": "RU BARTOLOME COSSIO"}` it will search in database all the records relate to the street RU BARTOLOME COSSIO and it will return a json as a response.