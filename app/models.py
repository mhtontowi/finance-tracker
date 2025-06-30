# app/models.py

# --- Lapisan Data (Model) ---
# Variabel ini digunakan untuk menyimpan data selama server berjalan.
# PENTING: Data ini akan hilang jika server di-restart.

# Digunakan sebagai ID unik untuk setiap pengeluaran baru.
expense_id_counter = 1 
# List (daftar) untuk menyimpan semua data pengeluaran.
expenses = [] 

def get_all_expenses():
    """Mengembalikan semua data pengeluaran."""
    return expenses

def add_expense(item, price, category):
    """Menambahkan pengeluaran baru dan mengembalikan dictionary-nya."""
    global expense_id_counter
    
    try:
        price = float(price)
    except (ValueError, TypeError):
        # Mengembalikan None jika harga tidak valid untuk ditangani oleh route
        return None

    expense = {
        'id': expense_id_counter, 
        'item': item, 
        'price': price, 
        'category': category
    }
    expenses.append(expense)
    expense_id_counter += 1
    return expense

def delete_expense_by_id(expense_id):
    """Menghapus pengeluaran berdasarkan ID. Mengembalikan True jika berhasil, False jika tidak ditemukan."""
    global expenses
    original_length = len(expenses)
    expenses = [expense for expense in expenses if expense['id'] != expense_id]
    # Mengembalikan True jika ada item yang dihapus
    return len(expenses) < original_length

def calculate_category_totals():
    """Menghitung total pengeluaran per kategori untuk grafik."""
    category_totals = {}
    for expense in expenses:
        category = expense['category']
        price = expense['price']
        category_totals[category] = category_totals.get(category, 0) + price

    chart_data = {
        "labels": list(category_totals.keys()),
        "values": list(category_totals.values())
    }
    return chart_data