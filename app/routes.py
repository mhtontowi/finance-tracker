# app/routes.py

from flask import Blueprint, render_template, request, jsonify
from . import models # Import modul models dari paket yang sama

# Membuat Blueprint untuk rute utama (halaman web)
main_bp = Blueprint('main', __name__)

# Membuat Blueprint untuk API, dengan prefix URL /api
api_bp = Blueprint('api', __name__, url_prefix='/api')


# --- Route Halaman Utama ---
@main_bp.route('/')
def index():
    return render_template('index.html')


# --- Routes untuk API Pengeluaran ---

@api_bp.route('/expenses', methods=['GET', 'POST'])
def handle_expenses():
    if request.method == 'POST':
        data = request.get_json()
        item = data.get('item')
        price = data.get('price')
        category = data.get('category')

        if not all([item, price, category]):
            return jsonify({'error': 'Missing data'}), 400

        new_expense = models.add_expense(item, price, category)

        if new_expense is None:
            return jsonify({'error': 'Invalid price format'}), 400
        
        return jsonify(new_expense), 201

    elif request.method == 'GET':
        all_expenses = models.get_all_expenses()
        chart_data = models.calculate_category_totals()
        
        return jsonify({
            "expenses": all_expenses,
            "chart_data": chart_data
        })


@api_bp.route('/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    success = models.delete_expense_by_id(expense_id)
    
    if not success:
        return jsonify({'error': 'Expense not found'}), 404

    return jsonify({'success': True, 'message': f'Expense with id {expense_id} deleted.'}), 200