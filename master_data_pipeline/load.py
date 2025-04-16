from google.cloud import bigquery
from google.oauth2 import service_account
# from config.settings import *
from extract import extract_data
from transform import transform_data

PROJECT_ID= "careful-granite-456318-r9" 
DATASET_ID= "db_Apache_Airflow"
TABLE_ID= "Sample_ETL_Dataset"
CREDENTIALS_PATH= "C:/Users/dhava/OneDrive/Documents/GitHub/DhavalUpadhyay-MyFirstProject/config/service_account.json"

def create_dataset_if_not_exists(client, dataset_id):
    try:
        client.get_dataset(dataset_id)
        print(f"Dataset {dataset_id} aslready exists")
    except Exception:
        dataset= bigquery.Dataset(dataset_id)
        dataset.location= "US"
        client.create_dataset(dataset_id)
        print(f"Dataset {dataset_id} Created")

def create_table_if_not_exists(client, table_id, schema):
    try:
        client.get_table(table_id)
        print(f"table {table_id} already exists")
    except Exception:
        table= bigquery.Table(table_id, schema=schema)
        client.create_table(table)
        print(f"table {table_id} Created")

def load_to_bigquery(df, dataset_id, table_id, project_id):
    dataset_id= f"{project_id}.{dataset_id}"
    table_id= f"{dataset_id}.{table_id}"
    
    create_dataset_if_not_exists(client, dataset_id)
    
    schema= [
        bigquery.SchemaField("Name", "STRING"),
        bigquery.SchemaField("Capital", "STRING"),
        bigquery.SchemaField("Region", "STRING"),
        bigquery.SchemaField("Subregion", "STRING"),
        ]

    create_table_if_not_exists(client, table_id, schema)
    job= client.load_table_from_dataframe(df, table_id, job_config= bigquery.LoadJobConfig(write_disposition= "WRITE_TRUNCATE"))
    job.result()
    print(f"{job.output_rows} loaded to {table_id}")

credentials= service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)
client= bigquery.Client(credentials=credentials, project= PROJECT_ID)
project_id= PROJECT_ID
dataset_id= DATASET_ID
table_id=TABLE_ID
# extracted_data= extract_data()
transformed_df= transform_data(extract_data())
load_to_bigquery(transformed_df, dataset_id, table_id, project_id)