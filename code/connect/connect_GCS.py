from google.cloud import storage

client = storage.Client()  # Không cần set GOOGLE_APPLICATION_CREDENTIALS

bucket = client.get_bucket('neat-throne-452007-h6')
blob = bucket.blob('countly/summary.json')
blob.upload_from_filename('/media/dunhan/Extreme SSD/Glamira_Data/summary.json')

print("Upload success")
