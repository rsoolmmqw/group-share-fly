from flask import Flask, request, jsonify, send_file, render_template_string
from flask_cors import CORS
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import os
import datetime
import json
from pathlib import Path

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Rsool1388Secret!'
app.config['UPLOAD_FOLDER'] = '/data/uploads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
CORS(app)

Path('/data/uploads').mkdir(parents=True, exist_ok=True)
Path('/data/db').mkdir(parents=True, exist_ok=True)

GROUP_PASSWORD = generate_password_hash("Rsool.1388")
FILES_DB = '/data/db/files.json'

def load_files():
    try:
        if os.path.exists(FILES_DB):
            with open(FILES_DB, 'r', encoding='utf-8') as f:
                return json.load(f)
    except:
        pass
    return []

def save_files(files):
    try:
        with open(FILES_DB, 'w', encoding='utf-8') as f:
            json.dump(files, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving: {e}")

@app.route('/')
def home():
    return render_template_string('''
<!DOCTYPE html>
<html dir="rtl" lang="fa">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>سرور گروه - Fly.io</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: Tahoma, Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 25px;
            padding: 60px 40px;
            box-shadow: 0 30px 80px rgba(0,0,0,0.5);
            text-align: center;
            max-width: 650px;
            width: 100%;
            animation: fadeIn 0.5s;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .logo {
            font-size: 6em;
            margin-bottom: 20px;
            animation: bounce 2s infinite;
        }
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
        h1 {
            color: #2d3748;
            font-size: 2.8em;
            margin-bottom: 15px;
            font-weight: bold;
        }
        .badge {
            background: linear-gradient(135deg, #4caf50, #45a049);
            color: white;
            padding: 20px 30px;
            border-radius: 15px;
            margin: 30px 0;
            font-size: 1.4em;
            font-weight: bold;
            box-shadow: 0 10px 30px rgba(76, 175, 80, 0.4);
        }
        .info-box {
            background: #f7fafc;
            padding: 30px;
            border-radius: 15px;
            margin: 25px 0;
            border: 2px solid #e2e8f0;
        }
        .info-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px 0;
            border-bottom: 1px solid #e2e8f0;
        }
        .info-row:last-child { border-bottom: none; }
        .info-label {
            font-weight: bold;
            color: #4a5568;
            font-size: 1.1em;
        }
        .info-value {
            background: #2d3748;
            color: #4caf50;
            padding: 10px 20px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            font-size: 1.1em;
            font-weight: bold;
        }
        .footer {
            margin-top: 40px;
            padding-top: 30px;
            border-top: 2px solid #e2e8f0;
            color: #718096;
            font-size: 1em;
        }
        .tag {
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 8px 15px;
            border-radius: 20px;
            margin: 5px;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">🚀</div>
        <h1>سرور با موفقیت فعال شد!</h1>
        <div class="badge">✅ آماده دریافت درخواست</div>
        
        <div class="info-box">
            <div class="info-row">
                <span class="info-label">🔐 رمز گروه:</span>
                <span class="info-value">Rsool.1388</span>
            </div>
            <div class="info-row">
                <span class="info-label">📁 فایل‌های ذخیره شده:</span>
                <span class="info-value">''' + str(len(load_files())) + ''' فایل</span>
            </div>
            <div class="info-row">
                <span class="info-label">⚡ وضعیت:</span>
                <span class="info-value" style="color: #4caf50;">آنلاین</span>
            </div>
            <div class="info-row">
                <span class="info-label">🌐 پلتفرم:</span>
                <span class="info-value">Fly.io Cloud</span>
            </div>
        </div>

        <div style="margin: 30px 0;">
            <span class="tag">🔒 امن</span>
            <span class="tag">⚡ سریع</span>
            <span class="tag">💾 دائمی</span>
            <span class="tag">🌍 گلوبال</span>
        </div>

        <div class="footer">
            این آدرس را در اپلیکیشن موبایل خود وارد کنید<br>
            <small style="color: #a0aec0;">Powered by Fly.io • Made with ❤️</small>
        </div>
    </div>
</body>
</html>
    ''')

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data.get('username', '')
        password = data.get('password', '')
        
        if check_password_hash(GROUP_PASSWORD, password):
            return jsonify({
                'success': True,
                'username': username,
                'message': f'خوش آمدید {username}! 🎉'
            })
        return jsonify({'success': False, 'message': '❌ رمز اشتباه است!'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'فایلی انتخاب نشده'}), 400
        
        file = request.files['file']
        username = request.form.get('username', 'ناشناس')
        
        if file and file.filename:
            filename = secure_filename(file.filename)
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            unique_filename = f"{timestamp}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(filepath)
            
            file_info = {
                'id': timestamp,
                'original_name': file.filename,
                'filename': unique_filename,
                'uploader': username,
                'date': datetime.datetime.now().strftime('%Y/%m/%d'),
                'time': datetime.datetime.now().strftime('%H:%M:%S'),
                'size': os.path.getsize(filepath),
                'type': file.content_type or 'unknown'
            }
            
            files = load_files()
            files.append(file_info)
            save_files(files)
            
            return jsonify({'success': True, 'message': '✅ آپلود موفق!', 'file': file_info})
        
        return jsonify({'success': False, 'error': 'خطا در آپلود'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/files', methods=['GET'])
def get_files():
    try:
        files = load_files()
        return jsonify({'success': True, 'files': files, 'count': len(files)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/download/<filename>')
def download_file(filename):
    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(filepath):
            return send_file(filepath, as_attachment=True)
        return jsonify({'error': 'فایل یافت نشد'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/delete/<file_id>', methods=['DELETE'])
def delete_file(file_id):
    try:
        files = load_files()
        updated = [f for f in files if f['id'] != file_id]
        
        if len(updated) < len(files):
            for f in files:
                if f['id'] == file_id:
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], f['filename'])
                    if os.path.exists(filepath):
                        os.remove(filepath)
            save_files(updated)
            return jsonify({'success': True, 'message': 'حذف شد'})
        return jsonify({'success': False, 'message': 'یافت نشد'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'files': len(load_files())}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
