import os
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check-links', methods=['POST'])
def check_links():
    data = request.get_json()
    if not data or 'links' not in data:
        return jsonify({'error': 'Tidak ada link yang dikirim'}), 400
    
    raw_links = data['links']
    list_link = [line.strip() for line in raw_links.split('\n') if line.strip()]
    
    # OTOMATIS HAPUS DUPLIKAT (menjaga urutan link tetap rapi)
    link_unik = list(dict.fromkeys(list_link))
    
    total_awal = len(list_link)
    total_unik = len(link_unik)
    duplikat = total_awal - total_unik
    
    link_aktif = []
    link_error = []
    
    # Cek status link secara cepat menggunakan method HEAD
    for link in link_unik:
        try:
            respons = requests.head(link, timeout=5, allow_redirects=True)
            if respons.status_code < 400:
                link_aktif.append(link)
            else:
                link_error.append(f"{link} (Error: {respons.status_code})")
        except Exception:
            link_error.append(f"{link} (Koneksi Gagal/Timeout)")
    
    return jsonify({
        'stat_total_awal': total_awal,
        'stat_total_unik': total_unik,
        'stat_duplikat': duplikat,
        'link_aktif': link_aktif,
        'link_error': link_error
    })
