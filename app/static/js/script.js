/* static/js/script.js */

// --- Variabel Global ---
// Variabel untuk menyimpan objek chart, agar kita bisa menghancurkannya (destroy) sebelum menggambar yang baru.
let categoryChart = null;

// --- Fungsi untuk Menambah Pengeluaran Baru ---
// Fungsi ini dipanggil saat tombol "Tambah" diklik.
async function addExpense() {
    // Mengambil nilai dari setiap input field.
    const item = document.getElementById('item').value;
    const price = document.getElementById('price').value;
    const category = document.getElementById('category').value;

    // Validasi sederhana di sisi klien: pastikan semua field terisi.
    if (!item || !price || !category) {
        alert('Mohon isi semua field.');
        return;
    }
    
    // Validasi tambahan: pastikan harga adalah angka.
    if (isNaN(parseFloat(price))) {
        alert('Input harga tidak valid. Mohon masukkan angka.');
        return;
    }

    try {
        // Mengirim data ke server menggunakan Fetch API dengan method 'POST'.
        const response = await fetch('/api/expenses', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            // Mengubah objek JavaScript menjadi string JSON untuk dikirim.
            body: JSON.stringify({ item, price, category }),
        });

        // Jika server merespons dengan sukses (status 201 Created).
        if (response.ok) {
            // Kosongkan kembali input fields.
            document.getElementById('item').value = '';
            document.getElementById('price').value = '';
            document.getElementById('category').value = '';
            // Panggil fetchData() untuk memperbarui tampilan dengan data terbaru.
            fetchData();
        } else {
            // Jika ada error dari server, tampilkan pesannya.
            const errorData = await response.json();
            alert('Error: ' + errorData.error);
        }
    } catch (error) {
        // Menangani error jika koneksi ke server gagal.
        console.error('Gagal menambahkan pengeluaran:', error);
        alert('Terjadi kesalahan. Silakan coba lagi.');
    }
}

// --- Fungsi untuk Mengambil Semua Data dari Server ---
// Fungsi ini adalah pusat untuk menyinkronkan data dari server ke tampilan.
async function fetchData() {
    try {
        // Mengirim permintaan 'GET' ke server untuk mendapatkan semua data.
        const response = await fetch('/api/expenses');
        const data = await response.json();
        
        // Memanggil fungsi-fungsi untuk memperbarui setiap bagian dari UI.
        updateTable(data.expenses);
        updateChart(data.chart_data);
        updateTotalExpense(data.expenses);
    } catch (error) {
        console.error('Gagal mengambil data:', error);
    }
}

// --- Fungsi untuk Memperbarui Tabel ---
function updateTable(expenses) {
    const tableBody = document.getElementById('expense-table-body');
    tableBody.innerHTML = ''; // Kosongkan tabel sebelum diisi ulang.

    // Loop melalui setiap data pengeluaran dan buat baris tabel baru.
    expenses.forEach(exp => {
        // EDIT: Menggunakan toLocaleString('id-ID') untuk format angka yang lebih baik (misal: 5000 -> 5.000).
        const formattedPrice = exp.price.toLocaleString('id-ID');
        const row = `
            <tr>
                <td>${exp.item}</td>
                <td>${formattedPrice}</td>
                <td>${exp.category}</td>
                <td>
                    <!-- Tombol hapus dengan atribut 'data-id' untuk menyimpan ID pengeluaran. -->
                    <button class="delete-btn" data-id="${exp.id}">Delete</button>
                </td>
            </tr>`;
        tableBody.innerHTML += row; // Tambahkan baris baru ke tabel.
    });
}

// --- Fungsi untuk Memperbarui Grafik ---
function updateChart(chartData) {
    const ctx = document.getElementById('category-chart').getContext('2d');
    
    // Jika sudah ada chart, hancurkan dulu sebelum membuat yang baru.
    // Ini penting untuk mencegah chart tumpang tindih dan error.
    if (categoryChart) {
        categoryChart.destroy();
    }

    // Membuat objek chart baru menggunakan Chart.js.
    categoryChart = new Chart(ctx, {
        type: 'doughnut', // Jenis grafik
        data: {
            labels: chartData.labels, // Label dari server (nama kategori)
            datasets: [{
                label: 'Pengeluaran',
                data: chartData.values, // Nilai dari server (total per kategori)
                backgroundColor: [ // Warna-warni untuk setiap kategori
                    'rgba(255, 99, 132, 0.7)', 'rgba(54, 162, 235, 0.7)',
                    'rgba(255, 206, 86, 0.7)', 'rgba(75, 192, 192, 0.7)',
                    'rgba(153, 102, 255, 0.7)', 'rgba(255, 159, 64, 0.7)'
                ],
                borderWidth: 1
            }]
        },
        options: { // Opsi tambahan untuk kustomisasi
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: { display: true, text: 'Pengeluaran per Kategori' }
            }
        }
    });
}

// --- Fungsi untuk Menghapus Pengeluaran ---
async function deleteExpense(expenseId) {
    // Tampilkan dialog konfirmasi sebelum menghapus.
    if (!confirm('Apakah Anda yakin ingin menghapus item ini?')) {
        return;
    }

    try {
        // Kirim permintaan 'DELETE' ke URL spesifik untuk pengeluaran yang akan dihapus.
        const response = await fetch(`/api/expenses/${expenseId}`, {
            method: 'DELETE',
        });

        if (response.ok) {
            fetchData(); // Jika berhasil, perbarui tampilan.
        } else {
            const errorData = await response.json();
            alert('Error: ' + errorData.error);
        }
    } catch (error) {
        console.error('Gagal menghapus pengeluaran:', error);
        alert('Terjadi kesalahan saat menghapus pengeluaran.');
    }
}

// --- Fungsi untuk Memperbarui Total Pengeluaran ---
function updateTotalExpense(expenses) {
    // Menjumlahkan semua harga dari list pengeluaran.
    const total = expenses.reduce((sum, expense) => sum + expense.price, 0);
    const totalDisplay = document.getElementById('total-expense-display');
    // EDIT: Menggunakan toLocaleString untuk format angka yang konsisten.
    totalDisplay.textContent = `(Total: Rp ${total.toLocaleString('id-ID')})`;
}

// --- Event Listeners (Pendengar Aksi Pengguna) ---

// Menjalankan fungsi addExpense saat tombol 'add-btn' diklik.
document.getElementById('add-btn').addEventListener('click', addExpense);

// Menggunakan 'event delegation' untuk tombol hapus.
// Listener ini dipasang di 'tbody', bukan di setiap tombol.
// Ini lebih efisien dan berfungsi bahkan untuk tombol yang baru dibuat.
const tableBody = document.getElementById('expense-table-body');
tableBody.addEventListener('click', (event) => {
    // Cek apakah elemen yang diklik memiliki class 'delete-btn'.
    if (event.target.classList.contains('delete-btn')) {
        // Ambil ID dari atribut 'data-id'.
        const expenseId = event.target.dataset.id;
        deleteExpense(expenseId);
    }
});

// Memanggil fetchData() saat halaman selesai dimuat untuk menampilkan data awal.
window.onload = fetchData;