from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import json
from flask import Flask, request, jsonify
from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime
import google.auth
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseUpload
import io
from PIL import Image
# Google Sheets API setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_FILE = 'data-382620-a930fbe4097f.json'  # Replace with the actual path to your Service Account Key JSON file
spreadsheet_id = '1lD1BmlTbO7F-iaIOE1aPJuQ4A22jbjwRMhLvh8-_CVQ'  # Replace with the ID of your Google Sheet

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

sheets_service = build('sheets', 'v4', credentials=creds)
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

service = build('drive', 'v3', credentials=creds)

db=mysql.connector.connect(
        host='db4free.net',
        user='jyothikiran',
        password='jkiran@root',
        database='samplejyothikira',
        port='3306',
    )
nopes=['undefined','null','','',"",'Null','NaN',]
def validate(data):
    if data in nopes:
        return 'All'
    return data


def convert_jpg_to_pdf(img_stream, pdf_filename):
    img = Image.open(img_stream)
    pdf_stream = io.BytesIO()
    img.save(pdf_stream, "PDF",quality=100)
    return pdf_stream, pdf_filename


def convert_jpg_to_pdf(img_stream, pdf_filename):
    img = Image.open(img_stream)
    pdf_stream = io.BytesIO()
    img.save(pdf_stream, "PDF")
    return pdf_stream, pdf_filename
app = Flask(__name__)
CORS(app)
@app.route('/',methods=['GET'])
def check_user():
    mycursor=db.cursor()
    email=request.args.get('email')
    mycursor.execute("SELECT * FROM users WHERE email='"+email+"';")
    res=mycursor.fetchall()
    print(res)
    if len(res)>0:
        return jsonify({'result':list(res[0])})
    else:
        return jsonify({'result':False})
    
@app.route('/submit',methods=['POST'])
def add_data():
    mycursor=db.cursor()
    mycursor.execute("SELECT username from users;")
    fall=mycursor.fetchall()
    print(fall)
    if len(fall[0])>0:
        fall=fall[0]
    data=json.loads(request.data)
    if request.method=='POST':
        if data['uname'] in fall:
            return jsonify({'result':'nuname'})
        mycursor.execute("INSERT INTO users(username,email,role,branch,organization) VALUES('"+data['uname']+"','"+data['email']+"','"+data['role']+"','"+data['branch']+"','"+data['organization_name']+"');")
        db.commit()
        print(mycursor.fetchall())
    return jsonify({'result':True})

def append_to_google_sheet(spreadsheet_id, data):
    values = [data]
    body = {
        'values': values
    }

    range_ = 'main!A:K'

    sheets_service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=range_,
        valueInputOption='RAW',
        body=body
    ).execute()

@app.route('/upload', methods=['POST'])
def upload():
    print("Upload clicked")
    try:
        institute = request.form['institute']
        year = request.form['year']
        subject = request.form['subject']
        type_ = request.form['type']
        time = datetime.datetime.now().strftime("%Y-%m-%d")
        sem = request.form['sem']
        file = request.files['file']
        user=request.form['uname']
        role=request.form['role']
        verified=request.form['verified']
        branch=request.form['branch']


        if file.filename.lower().endswith(('jpg', 'jpeg','png')):
            pdf_filename = file.filename.rsplit('.', 1)[0] + '.pdf'
            pdf_stream, pdf_filename = convert_jpg_to_pdf(file, pdf_filename)
            media = MediaIoBaseUpload(pdf_stream, mimetype='application/pdf')
        else:
            media = MediaIoBaseUpload(io.BytesIO(file.read()), mimetype=file.content_type)
        
        # media = MediaIoBaseUpload(io.BytesIO(file.read()), mimetype=file.content_type)
        file_metadata = {
            'name': str(year)+' '+str(sem)+' '+str(branch)+' '+str(subject)+' '+str(year)+' '+str(type_)+' '+str(subject)+' '+str(institute)+'.pdf',
            'parents': ['1brGN4ddiI0W5-bEJ_soI0WoTiUu0zDCW']
        }

        uploaded_file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        data = [validate(institute), validate(year), validate(subject), validate(type_), validate(time), validate(sem), validate(uploaded_file['id']),validate(user),validate(role),validate(verified),validate(branch) ]
        append_to_google_sheet(spreadsheet_id, data)

        return jsonify({'message': 'File uploaded and data recorded successfully.with id: '+uploaded_file.get("id")}), 200
    except Exception as e:
        print('Error occurred:', e)
        return jsonify({'error': 'Error occurred during file upload and data recording.'}), 500
if __name__ == '__main__':
    app.run(3790)