# app.py

# --- Komentar Awal ---
# Mengimpor library yang diperlukan.
# Flask: Kerangka kerja web utama untuk membangun server.
# render_template: Untuk menampilkan file HTML.
# request: Untuk mengakses data yang dikirim dari browser (misalnya, data form).
# jsonify: Untuk mengubah data Python (seperti dictionary) menjadi format JSON yang dapat dibaca oleh JavaScript.
from flask import Flask, render_template, request, jsonify

# Membuat instance aplikasi Flask.
app = Flask(__name__)

# --- Variabel Global untuk Menyimpan Data ---
# Variabel ini digunakan untuk menyimpan data selama server berjalan.
# PENTING: Data ini akan hilang jika server di-restart.
# Untuk aplikasi nyata, data seharusnya disimpan di database (seperti SQLite, PostgreSQL, dll).

# Digunakan sebagai ID unik untuk setiap pengeluaran baru.
expense_id_counter = 1 
# List (daftar) untuk menyimpan semua data pengeluaran.
expenses = [] 

# --- Route untuk Halaman Utama ---
# @app.route('/') mendefinisikan URL utama (misalnya, http://127.0.0.1:5000/).
# Saat pengguna membuka URL ini, fungsi index() akan dijalankan.
@app.route('/')
def index():
    # Mengirim file 'index.html' ke browser sebagai respons.
    return render_template('index.html')

# --- Route untuk API Pengeluaran ---
# Endpoint API untuk menangani semua permintaan terkait data pengeluaran.
# methods=['GET', 'POST'] berarti URL ini bisa merespons dua jenis permintaan:
# 1. GET: Untuk meminta/mengambil data.
# 2. POST: Untuk mengirim/membuat data baru.
@app.route('/api/expenses', methods=['GET', 'POST'])
def handle_expenses():
    # Menggunakan 'global' agar kita bisa mengubah variabel yang didefinisikan di luar fungsi ini.
    global expenses, expense_id_counter

    # --- Logika untuk Membuat Pengeluaran Baru (POST) ---
    if request.method == 'POST':
        # Mengambil data JSON yang dikirim dari JavaScript.
        data = request.get_json()
        item = data.get('item')
        price = data.get('price')
        category = data.get('category')

        # Validasi: Memastikan semua data yang diperlukan telah diisi.
        if not all([item, price, category]):
            return jsonify({'error': 'Missing data'}), 400 # 400 = Bad Request
        
        # Validasi: Memastikan harga adalah angka.
        try:
            price = float(price)
        except ValueError:
            return jsonify({'error': 'Invalid price format'}), 400

        # Membuat dictionary baru untuk menyimpan data pengeluaran.
        expense = {
            'id': expense_id_counter, 
            'item': item, 
            'price': price, 
            'category': category
        }
        # Menambahkan pengeluaran baru ke dalam list 'expenses'.
        expenses.append(expense)
        # Menambah counter ID agar ID berikutnya unik.
        expense_id_counter += 1
        # Mengirim kembali data pengeluaran yang baru dibuat sebagai konfirmasi.
        return jsonify(expense), 201 # 201 = Created

    # --- Logika untuk Mengambil Semua Data Pengeluaran (GET) ---
    elif request.method == 'GET':
        # Menghitung total pengeluaran per kategori untuk chart/grafik.
        category_totals = {}
        for expense in expenses:
            category = expense['category']
            price = expense['price']
            # Jika kategori sudah ada, tambahkan nilainya. Jika belum, buat baru.
            category_totals[category] = category_totals.get(category, 0) + price

        # Menyiapkan data dalam format yang dibutuhkan oleh Chart.js.
        chart_data = {
            "labels": list(category_totals.keys()),   # Nama kategori
            "values": list(category_totals.values())  # Total pengeluaran per kategori
        }
        
        # Mengirim semua data yang diperlukan ke frontend.
        return jsonify({
            "expenses": expenses,       # Daftar semua pengeluaran
            "chart_data": chart_data    # Data untuk grafik
        })

# --- Route untuk Menghapus Pengeluaran ---
# Endpoint API untuk menghapus satu pengeluaran berdasarkan ID-nya.
# <int:expense_id> adalah parameter dinamis, artinya URL-nya akan seperti /api/expenses/1, /api/expenses/2, dst.
@app.route('/api/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    global expenses
    
    # Mencatat jumlah pengeluaran sebelum dihapus.
    original_length = len(expenses)
    # Membuat list baru yang berisi semua pengeluaran KECUALI yang ID-nya cocok dengan expense_id.
    expenses = [expense for expense in expenses if expense['id'] != expense_id]
    
    # Jika panjang list tidak berubah, berarti pengeluaran dengan ID tersebut tidak ditemukan.
    if len(expenses) == original_length:
        return jsonify({'error': 'Expense not found'}), 404 # 404 = Not Found

    # Mengirim pesan sukses jika penghapusan berhasil.
    return jsonify({'success': True, 'message': f'Expense with id {expense_id} deleted.'}), 200 # 200 = OK


# --- Menjalankan Aplikasi ---
# Blok ini akan dieksekusi hanya jika file ini dijalankan secara langsung (bukan diimpor).
if __name__ == '__main__':
    # Menjalankan server Flask dalam mode debug (memudahkan development).
    app.run(debug=True)