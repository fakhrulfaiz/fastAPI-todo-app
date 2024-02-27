import json
from fastapi import FastAPI
# Assuming your JSON file is named report_contacts.json

app = FastAPI()
file_path = "report_contacts.json"
DATA = []
# Open and read the JSON file
with open(file_path, 'r') as file:
    # Load JSON data into the DATA variable
    DATA = json.load(file)

@app.get("/contacts")
async def get_all_report_contacts():
    return DATA



