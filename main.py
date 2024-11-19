from flask import Flask, request, jsonify
from docx2pdf import convert
import os
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return 'generate pdf by devnolife'

@app.route('/convert', methods=['POST'])
def convert_file():
    if 'file' not in request.files:
        return jsonify({'error': 'Tidak ada file yang dikirim'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Tidak ada file yang dipilih'}), 400
    if file:
        temp_filename = file.filename
        upload_folder = './uploads'
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, temp_filename)
        file.save(file_path)
        
        output_folder = './outputs'
        os.makedirs(output_folder, exist_ok=True)
        output_filename = os.path.splitext(temp_filename)[0] + '.pdf'
        output_path = os.path.join(output_folder, output_filename)
        try:
            
            convert(file_path, output_path)
        except Exception as e:
            os.remove(file_path)
            return jsonify({'error': 'Konversi gagal', 'message': str(e)}), 500
        
        url = "https://storage.superapps.if.unismuh.ac.id"
        payload = {'fileName': output_filename}
        files = {
            'file': (output_filename, open(output_path, 'rb'), 'application/pdf')
        }
        try:
            response = requests.post(url, data=payload, files=files)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            os.remove(file_path)
            os.remove(output_path)
            return jsonify({'error': 'Gagal mengirim file ke server penyimpanan', 'message': str(e)}), 500
        finally:
            files['file'][1].close()
        
        os.remove(file_path)
        os.remove(output_path)
        
        return response.text, response.status_code, response.headers.items()
    else:
        return jsonify({'error': 'Kesalahan dalam memproses file'}), 400

if __name__ == '__main__':
    app.run(debug=True , port=6000)
