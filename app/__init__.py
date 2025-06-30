# app/__init__.py

import os 
from flask import Flask

def create_app():
    """
    Fungsi pabrik untuk membuat instance aplikasi Flask.
    """
    # Membuat instance aplikasi Flask
    # instance_relative_config=True memberi tahu Flask bahwa file konfigurasi
    # bersifat relatif terhadap folder instance.
    app = Flask(__name__, instance_relative_config=True)

    # Memastikan folder instance ada
    # app.instance_path akan otomatis dibuat di level yang sama dengan folder app/
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Mengimpor dan mendaftarkan Blueprint dari file routes
    with app.app_context():
        from . import routes

        # Daftarkan Blueprint untuk halaman utama (tanpa prefix URL)
        app.register_blueprint(routes.main_bp)
        
        # Daftarkan Blueprint untuk API (dengan prefix URL /api)
        # Semua rute di dalam api_bp akan diawali dengan /api
        # Contoh: /expenses -> /api/expenses
        app.register_blueprint(routes.api_bp)

    return app