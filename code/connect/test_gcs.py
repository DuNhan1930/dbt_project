import os
from google.cloud import storage

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/dunhan/Downloads/service-account-key.json"

client = storage.Client()
buckets = list(client.list_buckets())

for bucket in buckets:
    print(bucket.name)
