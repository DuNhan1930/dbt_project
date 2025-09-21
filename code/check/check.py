from google.oauth2 import service_account

creds = service_account.Credentials.from_service_account_file(
    "/home/dunhan/Downloads/my-python-app-key.json"
)

print("Service account:", creds.service_account_email)
