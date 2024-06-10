from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import google.auth
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from cachetools import cached, TTLCache

app = Flask(__name__)
CORS(app)  # Thêm dòng này để kích hoạt CORS

# Thay đổi đường dẫn tới file credentials.json của bạn
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\kiet.trantuan\Downloads\fifth-mechanism-425310-s9-90916a180c9b.json"

# ID của Google Sheets và range bạn muốn truy cập
SPREADSHEET_ID = '1KXsc1e_2RvKWFpezsaGlyCzHyZO5DG0GYAiA4t-Nwjw'
RANGE_NAME = 'Sheet1!A:K'

# Thiết lập bộ nhớ đệm TTL 5 phút
cache = TTLCache(maxsize=100, ttl=300)

@cached(cache)
def get_imei_list():
    credentials, _ = google.auth.default()
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()

    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])
    return [row[0] for row in values]  # Lấy cột đầu tiên (IMEI)

@app.route('/check_imei', methods=['POST'])
def check_imei():
    data = request.json
    imei = data.get('imei')
    print(f"Received IMEI: {imei}")

    imei_list = get_imei_list()
    print(f"IMEI List: {imei_list}")

    if imei in imei_list:
        return jsonify({"message": "IMEI đã được đăng ký"}), 200
    else:
        return jsonify({"message": "IMEI chưa được đăng ký"}), 404

if __name__ == '__main__':
    app.run(debug=True)
