import os

import pandas as pd
from dotenv import load_dotenv, find_dotenv
from influxdb_client import InfluxDBClient
from influxdb_client.client.query_api import QueryApi
from influxdb_client.client.write_api import SYNCHRONOUS, WriteApi
from influxdb_client.domain.bucket import Bucket

environment_file:str = find_dotenv(f'.env.{os.getenv("ENVIRONMENT", "development")}')
load_dotenv(environment_file)

base_data = pd.read_csv("air-pollution.csv", header = 0, sep = ",")
base_data["Date"] = base_data["Year"].apply(lambda year: f"{year}-12-31")

# Rename columns to be more speaking
base_data.rename(columns = {"Nitrogen oxide (NOx)": "Nitrogen oxide"}, inplace = True)
base_data.rename(columns = {"Sulphur dioxide (SO₂) emissions": "Sulphur dioxide"}, inplace = True)
base_data.rename(columns = {"Carbon monoxide (CO) emissions": "Carbon monoxide"}, inplace = True)
base_data.rename(columns = {"Organic carbon (OC) emissions": "Organic carbon"}, inplace = True)
base_data.rename(columns = {"Non-methane volatile organic compounds (NMVOC) emissions": "Non-methane volatile organic compounds"}, inplace = True)
base_data.rename(columns = {"Black carbon (BC) emissions": "Black carbon"}, inplace = True)
base_data.rename(columns = {"Ammonia (NH₃) emissions": "Ammonia"}, inplace = True)

# Code is missing for e.g. 'South America' so use Entity column for now
base_data.drop(columns = ["Code"], inplace = True)

ix_host = os.getenv("influx.host")
ix_username = os.getenv("influx.username")
ix_password = os.getenv("influx.password")
ix_token = os.getenv("influx.token")
ix_org = os.getenv("influx.org")
ix_bucket = os.getenv("influx.bucket", "air-pollution")

with (InfluxDBClient(url = ix_host, token = ix_token, org = ix_org, debug = True) as client):
  write_api: WriteApi = client.write_api(write_options = SYNCHRONOUS)
  query_api: QueryApi = client.query_api()
  buckets_api = client.buckets_api()

  bucket:Bucket = buckets_api.find_bucket_by_name(ix_bucket)

  if bucket is not None:
    buckets_api.delete_bucket(bucket.id)

  buckets_api.create_bucket(bucket_name = ix_bucket, org = ix_org)

  for measurement in ["Nitrogen oxide", "Sulphur dioxide", "Carbon monoxide", "Organic carbon", "Non-methane volatile organic compounds", "Black carbon", "Ammonia"]:
    data:pd.DataFrame = base_data[["Entity", "Year", "Date", measurement]].copy()

    result = write_api.write(
      ix_bucket,
      record = data,
      data_frame_timestamp_column = "Date",
      data_frame_measurement_name = f"Air Pollution Sensor",
      data_frame_tag_columns = ["Entity", "Year"]
    )