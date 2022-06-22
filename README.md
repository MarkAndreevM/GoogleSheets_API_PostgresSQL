# WIP!<br> GoogleSheets_API_PostgreSQL
Essence of the project:
<br>Data request via API in GoogleSheets tables. Synchronizing Google Spreadsheets in PostgreSQL

## Start Project:
1. Get google api json key ([URL](https://cloud.google.com/docs/authentication/getting-started)) and put into ./config_project and rename -> `keys.json`
<br> 
<br>
     - Go to the Google APIs Console.
     - Create a new project.
     - Click Enable API. Search for and enable the Google Drive API.
     - Create credentials for a Web Server to access Application Data.
     - Name the service account and grant it a Project Role of Editor.
     - Download the JSON file.
     - Copy the JSON file to put into ./config_project and rename it to `keys.json`
     - Create a new google sheet
     - Share the sheet with the email in your GoogleSheets table <br> <br>

2. Rename `your_config.py` to `config.py` and past your <br> <br>
3. Copy the GoogleSheets ID in the format `1zWDJZ_DQG79EazUb-jrRSLxq7orM58TZmVrr1TZq_SF` and put into ./config_project/config.py to the variable SAMPLE_SPREADSHEET_ID <br> <br>
4. Install `requirements.txt` <br> <br>
5. Start the project `main.py`


### <center>link to my spreadsheet:</center>

`https://docs.google.com/spreadsheets/d/1zWDJZ_SQG89EazUb-jrRALxq8orM58RZmVrr1TZq_PE/edit#gid=0`
