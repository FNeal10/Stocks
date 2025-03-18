from azure.storage.blob import BlobClient, BlobServiceClient, ContainerClient
from dotenv import load_dotenv
import os
import pandas as pd
from io import BytesIO

load_dotenv()

service_client = BlobServiceClient.from_connection_string(os.getenv("AZURE_CONNECTION_STRING"))
container_client = service_client.get_container_client(os.getenv("CONTAINER_NAME"))

def get_urls():
   
   blob_name = f"stocks_list.csv"
   blob_client = container_client.get_blob_client(blob=blob_name)
   data = blob_client.download_blob()
   
   blob_data = data.readall()
   df = pd.read_csv(BytesIO(blob_data))

   return df

    

