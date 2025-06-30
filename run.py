# run.py

from app import create_app
import os # Diperlukan untuk __init__.py

# Membuat instance aplikasi menggunakan fungsi pabrik
app = create_app()

# Menjalankan Aplikasi
# Blok ini akan dieksekusi hanya jika file ini dijalankan secara langsung
if __name__ == '__main__':
    # Menjalankan server Flask dalam mode debug
    app.run(debug=True)