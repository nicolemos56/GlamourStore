from flask import render_template, request, session, redirect, url_for, jsonify, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from app import app, allowed_file, db
from database import get_dashboard_stats, get_products, get_orders, get_categories, add_product, update_product, delete_product, get_product_by_id, update_order_status, delete_order, get_bank_details, update_bank_details
from models import User, Product, Order, OrderItem
import os
import uuid

# Product data with stock photos - Expanded catalog
PRODUCTS = [
    # Cosméticos
    {
        'id': 1,
        'name': 'Fantasy de Britney Spears',
        'price': 45000.00,
        'category': 'Cosméticos',
        'image': 'https://cdn.pixabay.com/photo/2020/05/18/16/17/social-media-5187243_960_720.png'
    },
    {
        'id': 2,
        'name': 'Água de colônia Oásis de ameixa',
        'price': 4000.00,
        'category': 'Cosméticos',
        'image': 'https://cdn.pixabay.com/photo/2017/09/07/08/54/money-2724241_960_720.jpg'
    },
    {
        'id': 3,
        'name': 'Batom Matte Vermelho',
        'price': 8500.00,
        'category': 'Cosméticos',
        'image': 'https://cdn.pixabay.com/photo/2016/11/29/12/51/makeup-1869435_960_720.jpg'
    },
    {
        'id': 4,
        'name': 'Base Líquida Natural',
        'price': 12000.00,
        'category': 'Cosméticos',
        'image': 'https://cdn.pixabay.com/photo/2016/03/26/22/22/lipstick-1281570_960_720.jpg'
    },
    {
        'id': 5,
        'name': 'Máscara de Cílios Volume',
        'price': 15000.00,
        'category': 'Cosméticos',
        'image': 'https://cdn.pixabay.com/photo/2017/07/31/22/05/makeup-2561516_960_720.jpg'
    },
    
    # Calçados Femininos
    {
        'id': 6,
        'name': 'Bota Salto',
        'price': 10000.00,
        'category': 'Calçados Femininos',
        'image': 'https://cdn.pixabay.com/photo/2017/08/01/11/48/woman-2564660_960_720.jpg'
    },
    {
        'id': 7,
        'name': 'Sandália Elegante',
        'price': 8500.00,
        'category': 'Calçados Femininos',
        'image': 'https://cdn.pixabay.com/photo/2016/06/03/17/35/shoes-1433925_960_720.jpg'
    },
    {
        'id': 8,
        'name': 'Tênis Casual Branco',
        'price': 12500.00,
        'category': 'Calçados Femininos',
        'image': 'https://cdn.pixabay.com/photo/2016/11/19/18/06/feet-1840619_960_720.jpg'
    },
    {
        'id': 9,
        'name': 'Sapato Social Feminino',
        'price': 14000.00,
        'category': 'Calçados Femininos',
        'image': 'https://cdn.pixabay.com/photo/2017/08/01/11/48/woman-2564660_960_720.jpg'
    },
    
    # Roupas Femininas
    {
        'id': 10,
        'name': 'Calça Leggings Jeans',
        'price': 10300.00,
        'category': 'Roupas Femininas',
        'image': 'https://cdn.pixabay.com/photo/2017/08/01/08/29/people-2563491_960_720.jpg'
    },
    {
        'id': 11,
        'name': 'Calça Simples Jeans',
        'price': 10000.00,
        'category': 'Roupas Femininas',
        'image': 'https://cdn.pixabay.com/photo/2016/11/29/13/14/attractive-1869761_960_720.jpg'
    },
    {
        'id': 12,
        'name': 'Calção Listrado',
        'price': 3800.00,
        'category': 'Roupas Femininas',
        'image': 'https://cdn.pixabay.com/photo/2017/08/01/08/29/people-2563491_960_720.jpg'
    },
    {
        'id': 13,
        'name': 'Calça Cintura Subida Flare',
        'price': 15960.00,
        'category': 'Roupas Femininas',
        'image': 'https://cdn.pixabay.com/photo/2016/11/29/13/14/attractive-1869761_960_720.jpg'
    },
    {
        'id': 14,
        'name': 'Calças Estampadas',
        'price': 14500.00,
        'category': 'Roupas Femininas',
        'image': 'https://cdn.pixabay.com/photo/2017/08/01/08/29/people-2563491_960_720.jpg'
    },
    {
        'id': 15,
        'name': 'Vestido Casual Verão',
        'price': 18000.00,
        'category': 'Roupas Femininas',
        'image': 'https://cdn.pixabay.com/photo/2016/11/29/13/14/attractive-1869761_960_720.jpg'
    },
    {
        'id': 16,
        'name': 'Blusa Social Feminina',
        'price': 12500.00,
        'category': 'Roupas Femininas',
        'image': 'https://cdn.pixabay.com/photo/2017/08/01/08/29/people-2563491_960_720.jpg'
    },
    
    # Bolsas
    {
        'id': 17,
        'name': 'Bolsa de Mão Couro',
        'price': 25000.00,
        'category': 'Bolsas',
        'image': 'https://cdn.pixabay.com/photo/2016/11/29/12/45/bag-1869682_960_720.jpg'
    },
    {
        'id': 18,
        'name': 'Carteira Feminina Elegante',
        'price': 8500.00,
        'category': 'Bolsas',
        'image': 'https://cdn.pixabay.com/photo/2017/08/01/11/48/woman-2564660_960_720.jpg'
    },
    {
        'id': 19,
        'name': 'Mochila Casual Urbana',
        'price': 15000.00,
        'category': 'Bolsas',
        'image': 'https://cdn.pixabay.com/photo/2016/11/29/12/45/bag-1869682_960_720.jpg'
    },
    {
        'id': 20,
        'name': 'Bolsa Tiracolo Moderna',
        'price': 18500.00,
        'category': 'Bolsas',
        'image': 'https://cdn.pixabay.com/photo/2017/08/01/11/48/woman-2564660_960_720.jpg'
    },
    
    # Acessórios
    {
        'id': 21,
        'name': 'Colar Dourado Delicado',
        'price': 12000.00,
        'category': 'Acessórios',
        'image': 'https://cdn.pixabay.com/photo/2017/08/01/11/48/woman-2564660_960_720.jpg'
    },
    {
        'id': 22,
        'name': 'Brincos Pérola Clássicos',
        'price': 15500.00,
        'category': 'Acessórios',
        'image': 'https://cdn.pixabay.com/photo/2016/11/29/12/51/makeup-1869435_960_720.jpg'
    },
    {
        'id': 23,
        'name': 'Relógio Feminino Elegante',
        'price': 35000.00,
        'category': 'Acessórios',
        'image': 'https://cdn.pixabay.com/photo/2017/08/01/11/48/woman-2564660_960_720.jpg'
    },
    {
        'id': 24,
        'name': 'Óculos de Sol Fashion',
        'price': 22000.00,
        'category': 'Acessórios',
        'image': 'https://cdn.pixabay.com/photo/2016/11/29/12/51/makeup-1869435_960_720.jpg'
    },
    
    # Calçados Infantis
    {
        'id': 25,
        'name': 'Tênis Infantil Colorido',
        'price': 8500.00,
        'category': 'Calçados Infantis',
        'image': 'https://cdn.pixabay.com/photo/2016/06/03/17/35/shoes-1433925_960_720.jpg'
    },
    {
        'id': 26,
        'name': 'Sandália Infantil Confortável',
        'price': 6500.00,
        'category': 'Calçados Infantis',
        'image': 'https://cdn.pixabay.com/photo/2016/11/19/18/06/feet-1840619_960_720.jpg'
    },
    {
        'id': 27,
        'name': 'Sapatinho de Bebê',
        'price': 4500.00,
        'category': 'Calçados Infantis',
        'image': 'https://cdn.pixabay.com/photo/2016/06/03/17/35/shoes-1433925_960_720.jpg'
    },
    
    # Produtos e acessórios de cabelo
    {
        'id': 28,
        'name': 'Shampoo Nutritivo 500ml',
        'price': 9500.00,
        'category': 'Produtos e acessórios de cabelo',
        'image': 'https://cdn.pixabay.com/photo/2017/09/07/08/54/money-2724241_960_720.jpg'
    },
    {
        'id': 29,
        'name': 'Condicionador Hidratante',
        'price': 8500.00,
        'category': 'Produtos e acessórios de cabelo',
        'image': 'https://cdn.pixabay.com/photo/2020/05/18/16/17/social-media-5187243_960_720.png'
    },
    {
        'id': 30,
        'name': 'Escova de Cabelo Premium',
        'price': 12000.00,
        'category': 'Produtos e acessórios de cabelo',
        'image': 'https://cdn.pixabay.com/photo/2017/09/07/08/54/money-2724241_960_720.jpg'
    },
    {
        'id': 31,
        'name': 'Presilhas Decorativas Kit',
        'price': 5500.00,
        'category': 'Produtos e acessórios de cabelo',
        'image': 'https://cdn.pixabay.com/photo/2020/05/18/16/17/social-media-5187243_960_720.png'
    },
    {
        'id': 32,
        'name': 'Óleo Capilar Reparador',
        'price': 15500.00,
        'category': 'Produtos e acessórios de cabelo',
        'image': 'https://cdn.pixabay.com/photo/2017/09/07/08/54/money-2724241_960_720.jpg'
    }
]

CATEGORIES = [
    'Acessórios',
    'Bolsas', 
    'Calçados Femininos',
    'Calçados Infantis',
    'Cosméticos',
    'Produtos e acessórios de cabelo',
    'Roupas Femininas'
]

@app.route('/')
def index():
    search_query = request.args.get('search', '').lower()
    category_filter = request.args.get('category', '')
    page = request.args.get('page', 1, type=int)
    per_page = 8  # 8 products per page
    
    # Get products from database
    all_products_data = get_products(page=1, per_page=1000)  # Get all products for homepage
    db_products = all_products_data['products']
    
    # Convert database products to match PRODUCTS format for compatibility
    filtered_products = []
    for p in db_products:
        if p['is_active']:  # Only show active products
            product = {
                'id': p['id'],
                'name': p['name'],
                'price': p['price'],
                'category': p['category'],
                'image': p['image_url'] if p['image_url'] else 'https://via.placeholder.com/300x250?text=Sem+Imagem',
                'stock_quantity': p['stock_quantity']
            }
            filtered_products.append(product)
    
    # Apply search filter
    if search_query:
        filtered_products = [p for p in filtered_products if search_query in p['name'].lower()]
    
    # Apply category filter
    if category_filter:
        filtered_products = [p for p in filtered_products if p['category'] == category_filter]
    
    # Pagination
    total_products = len(filtered_products)
    total_pages = (total_products + per_page - 1) // per_page
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    paginated_products = filtered_products[start_index:end_index]
    
    # Calculate cart totals and prepare cart items
    cart_total = 0
    cart_count = 0
    cart_items = []
    for product_id, quantity in session.get('cart', {}).items():
        # Get product from database
        db_product = get_product_by_id(int(product_id))
        if db_product and db_product['is_active']:
            product = {
                'id': db_product['id'],
                'name': db_product['name'],
                'price': db_product['price'],
                'category': db_product['category'],
                'image': db_product['image_url'] if db_product['image_url'] else 'https://via.placeholder.com/300x250?text=Sem+Imagem'
            }
            cart_total += product['price'] * quantity
            cart_count += quantity
            cart_items.append({
                'product': product,
                'quantity': quantity
            })
    
    return render_template('index.html', 
                         products=paginated_products,
                         categories=CATEGORIES,
                         cart_total=cart_total,
                         cart_count=cart_count,
                         cart_items=cart_items,
                         current_search=request.args.get('search', ''),
                         current_category=category_filter,
                         current_page=page,
                         total_pages=total_pages,
                         total_products=total_products)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 1))
    
    if 'cart' not in session:
        session['cart'] = {}
    
    if product_id in session['cart']:
        session['cart'][product_id] += quantity
    else:
        session['cart'][product_id] = quantity
    
    session.modified = True
    
    # If it's an AJAX request, return JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Calculate new cart totals
        cart_total = 0
        cart_count = 0
        for pid, qty in session.get('cart', {}).items():
            db_product = get_product_by_id(int(pid))
            if db_product and db_product['is_active']:
                cart_total += db_product['price'] * qty
                cart_count += qty
        
        return jsonify({
            'success': True,
            'cart_total': cart_total,
            'cart_count': cart_count,
            'message': f'Produto adicionado ao carrinho!'
        })
    
    return redirect(url_for('index'))

@app.route('/update_cart_quantity', methods=['POST'])
def update_cart_quantity():
    data = request.get_json()
    product_id = str(data.get('product_id'))
    action = data.get('action')
    
    if 'cart' not in session:
        session['cart'] = {}
    
    if product_id in session['cart']:
        if action == 'increase':
            session['cart'][product_id] += 1
        elif action == 'decrease':
            session['cart'][product_id] -= 1
            if session['cart'][product_id] <= 0:
                del session['cart'][product_id]
        elif action == 'remove':
            del session['cart'][product_id]
    
    session.modified = True
    
    # Calculate new cart totals
    cart_total = 0
    cart_count = 0
    cart_items = []
    
    for pid, qty in session.get('cart', {}).items():
        db_product = get_product_by_id(int(pid))
        if db_product and db_product['is_active']:
            item_total = db_product['price'] * qty
            cart_total += item_total
            cart_count += qty
            cart_items.append({
                'id': db_product['id'],
                'name': db_product['name'],
                'price': db_product['price'],
                'quantity': qty,
                'total': item_total
            })
    
    return jsonify({
        'success': True,
        'cart_total': cart_total,
        'cart_count': cart_count,
        'cart_items': cart_items
    })

@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    session['cart'] = {}
    session.modified = True
    
    # If it's an AJAX request, return JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            'success': True,
            'message': 'Carrinho limpo com sucesso!'
        })
    
    return redirect(url_for('index'))

@app.route('/get_cart_items')
def get_cart_items():
    cart_items = []
    for product_id, quantity in session.get('cart', {}).items():
        db_product = get_product_by_id(int(product_id))
        if db_product and db_product['is_active']:
            cart_items.append({
                'id': db_product['id'],
                'name': db_product['name'],
                'price': db_product['price'],
                'quantity': quantity,
                'total': db_product['price'] * quantity
            })
    
    return jsonify({
        'success': True,
        'cart_items': cart_items
    })

@app.route('/checkout')
def checkout():
    # Check if cart is empty
    if not session.get('cart') or len(session.get('cart', {})) == 0:
        flash('Seu carrinho está vazio. Adicione produtos antes de continuar.', 'warning')
        return redirect(url_for('products'))
    
    cart_items = []
    cart_total = 0
    
    for product_id, quantity in session.get('cart', {}).items():
        db_product = get_product_by_id(int(product_id))
        if db_product and db_product['is_active']:
            product = {
                'id': db_product['id'],
                'name': db_product['name'],
                'price': db_product['price'],
                'category': db_product['category'],
                'image': db_product['image_url'] if db_product['image_url'] else 'https://via.placeholder.com/300x250?text=Sem+Imagem'
            }
            item_total = product['price'] * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total': item_total
            })
            cart_total += item_total
    
    # Double check if cart is still empty after processing
    if not cart_items:
        flash('Nenhum produto válido encontrado no carrinho.', 'error')
        return redirect(url_for('products'))
    
    return render_template('checkout.html', cart_items=cart_items, cart_total=cart_total)

@app.route('/finalizar')
def finalizar():
    # Check if cart is empty
    if not session.get('cart') or len(session.get('cart', {})) == 0:
        flash('Seu carrinho está vazio. Adicione produtos antes de finalizar a compra.', 'warning')
        return redirect(url_for('products'))
    
    cart_items = []
    cart_total = 0
    cart_count = 0
    
    for product_id, quantity in session.get('cart', {}).items():
        db_product = get_product_by_id(int(product_id))
        if db_product and db_product['is_active']:
            product = {
                'id': db_product['id'],
                'name': db_product['name'],
                'price': db_product['price'],
                'category': db_product['category'],
                'image': db_product['image_url'] if db_product['image_url'] else 'https://via.placeholder.com/300x250?text=Sem+Imagem'
            }
            item_total = product['price'] * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total': item_total
            })
            cart_total += item_total
            cart_count += quantity
    
    # Double check if cart is still empty after processing
    if not cart_items:
        flash('Nenhum produto válido encontrado no carrinho.', 'error')
        return redirect(url_for('products'))
    
    # Get bank details for payment information
    bank_details = get_bank_details()
    
    return render_template('finalizar.html', cart_items=cart_items, cart_total=cart_total, cart_count=cart_count, bank_details=bank_details)

@app.route('/process_order', methods=['POST'])
def process_order():
    try:
        # Get form data
        customer_name = request.form.get('customer_name')
        customer_phone = request.form.get('customer_phone')
        customer_email = request.form.get('customer_email')
        customer_nif = request.form.get('customer_nif', '')
        delivery_method = request.form.get('delivery_method')
        payment_method = request.form.get('payment_method')
        delivery_address = request.form.get('delivery_address', '')
        observations = request.form.get('observations', '')
        
        # Validate required fields
        if not all([customer_name, customer_phone, customer_email, delivery_method, payment_method]):
            return jsonify({'success': False, 'message': 'Campos obrigatórios em falta'})
        
        # Validate email format
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, customer_email):
            return jsonify({'success': False, 'message': 'Formato de email inválido'})
        
        # Validate phone number (basic validation for Angola format)
        phone_clean = re.sub(r'[\s\-\(\)]', '', customer_phone)
        if not phone_clean.isdigit() or len(phone_clean) < 9:
            return jsonify({'success': False, 'message': 'Número de telefone inválido'})
        
        # Validate delivery method
        if delivery_method not in ['pickup', 'delivery']:
            return jsonify({'success': False, 'message': 'Método de entrega inválido'})
        
        # If delivery method is 'delivery', address is required
        if delivery_method == 'delivery' and not delivery_address.strip():
            return jsonify({'success': False, 'message': 'Endereço de entrega é obrigatório para entrega em casa'})
        
        # Validate customer name
        if len(customer_name.strip()) < 2:
            return jsonify({'success': False, 'message': 'Nome deve ter pelo menos 2 caracteres'})
        
        # Calculate cart total and get items
        cart_items = []
        cart_total = 0
        
        for product_id, quantity in session.get('cart', {}).items():
            db_product = get_product_by_id(int(product_id))
            if db_product and db_product['is_active']:
                item_total = db_product['price'] * quantity
                cart_items.append({
                    'product_id': db_product['id'],
                    'product_name': db_product['name'],
                    'product_price': db_product['price'],
                    'quantity': quantity,
                    'subtotal': item_total
                })
                cart_total += item_total
        
        if not cart_items:
            return jsonify({'success': False, 'message': 'Carrinho vazio'})
        
        # Create order
        order = Order(
            customer_name=customer_name,
            customer_phone=customer_phone,
            customer_email=customer_email,
            customer_nif=customer_nif,
            delivery_method=delivery_method,
            payment_method=payment_method,
            total_amount=cart_total,
            delivery_address=delivery_address,
            observations=observations,
            status='pending'
        )
        
        db.session.add(order)
        db.session.flush()  # Get the order ID
        
        # Create order items
        for item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item['product_id'],
                product_name=item['product_name'],
                product_price=item['product_price'],
                quantity=item['quantity'],
                subtotal=item['subtotal']
            )
            db.session.add(order_item)
        
        db.session.commit()
        
        # Clear cart
        session['cart'] = {}
        session.modified = True
        
        return jsonify({
            'success': True, 
            'message': 'Pedido criado com sucesso!',
            'order_id': order.id
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Erro ao processar pedido: {str(e)}'})

# ===== ADMIN PANEL ROUTES =====

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('admin_dashboard'))
        else:
            flash('Credenciais inválidas. Tente novamente.', 'error')
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    flash('Logout realizado com sucesso.', 'success')
    return redirect(url_for('admin_login'))

@app.route('/admin/change-password', methods=['GET', 'POST'])
@login_required
def admin_change_password():
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        # Verificar senha atual
        if not current_user.check_password(current_password):
            flash('Senha atual incorreta.', 'error')
            return render_template('admin/change_password.html')
        
        # Verificar se as novas senhas coincidem
        if new_password != confirm_password:
            flash('As novas senhas não coincidem.', 'error')
            return render_template('admin/change_password.html')
        
        # Verificar tamanho mínimo da senha
        if len(new_password) < 6:
            flash('A nova senha deve ter pelo menos 6 caracteres.', 'error')
            return render_template('admin/change_password.html')
        
        # Alterar senha
        current_user.set_password(new_password)
        db.session.commit()
        flash('Senha alterada com sucesso!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/change_password.html')

@app.route('/admin')
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    stats = get_dashboard_stats()
    return render_template('admin/dashboard.html', stats=stats)

@app.route('/admin/products')
@login_required
def admin_products():
    page = request.args.get('page', 1, type=int)
    products_data = get_products(page=page, per_page=10)
    categories = get_categories()
    return render_template('admin/products.html', 
                         products=products_data['products'], 
                         pagination=products_data['pagination'],
                         categories=categories)

@app.route('/admin/products/add', methods=['GET', 'POST'])
@login_required
def admin_add_product():
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name', '').strip()
        price_str = request.form.get('price', '')
        category = request.form.get('category', '').strip()
        description = request.form.get('description', '').strip()
        stock_quantity_str = request.form.get('stock_quantity', '')
        
        # Validate required fields
        if not all([name, price_str, category, stock_quantity_str]):
            flash('Todos os campos obrigatórios devem ser preenchidos.', 'error')
            categories = get_categories()
            return render_template('admin/add_product.html', categories=categories)
        
        # Validate name length
        if len(name) < 2 or len(name) > 100:
            flash('Nome do produto deve ter entre 2 e 100 caracteres.', 'error')
            categories = get_categories()
            return render_template('admin/add_product.html', categories=categories)
        
        # Validate and convert price
        try:
            price = float(price_str)
            if price <= 0:
                raise ValueError()
        except ValueError:
            flash('Preço deve ser um número positivo.', 'error')
            categories = get_categories()
            return render_template('admin/add_product.html', categories=categories)
        
        # Validate and convert stock quantity
        try:
            stock_quantity = int(stock_quantity_str)
            if stock_quantity < 0:
                raise ValueError()
        except ValueError:
            flash('Quantidade em estoque deve ser um número inteiro positivo.', 'error')
            categories = get_categories()
            return render_template('admin/add_product.html', categories=categories)
        
        # Validate category exists
        categories_list = get_categories()
        if category not in [cat['name'] for cat in categories_list]:
            flash('Categoria inválida.', 'error')
            categories = get_categories()
            return render_template('admin/add_product.html', categories=categories)
        
        # Handle image upload
        image_url = ''
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '' and allowed_file(file.filename):
                # Upload to Cloudinary
                from app import upload_to_cloudinary
                cloudinary_url = upload_to_cloudinary(file)
                if cloudinary_url:
                    image_url = cloudinary_url
                else:
                    flash('Erro no upload da imagem. Tente novamente.', 'error')
                    categories = get_categories()
                    return render_template('admin/add_product.html', categories=categories)
        
        product_id = add_product(name, price, category, image_url, description, stock_quantity)
        if product_id:
            flash('Produto adicionado com sucesso!', 'success')
            return redirect(url_for('admin_products'))
        else:
            flash('Erro ao adicionar produto.', 'error')
    
    categories = get_categories()
    return render_template('admin/add_product.html', categories=categories)

@app.route('/admin/products/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
def admin_edit_product(product_id):
    product = get_product_by_id(product_id)
    if not product:
        flash('Produto não encontrado.', 'error')
        return redirect(url_for('admin_products'))
    
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name', '').strip()
        price_str = request.form.get('price', '')
        category = request.form.get('category', '').strip()
        description = request.form.get('description', '').strip()
        stock_quantity_str = request.form.get('stock_quantity', '')
        is_active = 'is_active' in request.form
        
        # Validate required fields
        if not all([name, price_str, category, stock_quantity_str]):
            flash('Todos os campos obrigatórios devem ser preenchidos.', 'error')
            categories = get_categories()
            return render_template('admin/edit_product.html', product=product, categories=categories)
        
        # Validate name length
        if len(name) < 2 or len(name) > 100:
            flash('Nome do produto deve ter entre 2 e 100 caracteres.', 'error')
            categories = get_categories()
            return render_template('admin/edit_product.html', product=product, categories=categories)
        
        # Validate and convert price
        try:
            price = float(price_str)
            if price <= 0:
                raise ValueError()
        except ValueError:
            flash('Preço deve ser um número positivo.', 'error')
            categories = get_categories()
            return render_template('admin/edit_product.html', product=product, categories=categories)
        
        # Validate and convert stock quantity
        try:
            stock_quantity = int(stock_quantity_str)
            if stock_quantity < 0:
                raise ValueError()
        except ValueError:
            flash('Quantidade em estoque deve ser um número inteiro positivo.', 'error')
            categories = get_categories()
            return render_template('admin/edit_product.html', product=product, categories=categories)
        
        # Validate category exists
        categories_list = get_categories()
        if category not in [cat['name'] for cat in categories_list]:
            flash('Categoria inválida.', 'error')
            categories = get_categories()
            return render_template('admin/edit_product.html', product=product, categories=categories)
        
        # Handle image upload
        image_url = product['image_url']  # Keep existing image by default
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '' and allowed_file(file.filename):
                # Upload to Cloudinary
                from app import upload_to_cloudinary
                cloudinary_url = upload_to_cloudinary(file)
                if cloudinary_url:
                    image_url = cloudinary_url
                    # Note: Old Cloudinary images are automatically managed
                else:
                    flash('Erro no upload da imagem. Tente novamente.', 'error')
                    categories = get_categories()
                    return render_template('admin/edit_product.html', product=product, categories=categories)
        
        if update_product(product_id, name, price, category, image_url, description, stock_quantity, is_active):
            flash('Produto atualizado com sucesso!', 'success')
            return redirect(url_for('admin_products'))
        else:
            flash('Erro ao atualizar produto.', 'error')
    
    categories = get_categories()
    return render_template('admin/edit_product.html', product=product, categories=categories)

@app.route('/admin/products/delete/<int:product_id>', methods=['POST'])
@login_required
def admin_delete_product(product_id):
    if delete_product(product_id):
        flash('Produto excluído com sucesso!', 'success')
    else:
        flash('Erro ao excluir produto.', 'error')
    return redirect(url_for('admin_products'))

@app.route('/admin/orders')
@login_required
def admin_orders():
    page = request.args.get('page', 1, type=int)
    orders_data = get_orders(page=page, per_page=10)
    return render_template('admin/orders.html', 
                         orders=orders_data['orders'], 
                         pagination=orders_data['pagination'])

@app.route('/admin/settings', methods=['GET', 'POST'])
@login_required
def admin_settings():
    if request.method == 'POST':
        bank_name = request.form['bank_name']
        iban = request.form['iban']
        account_number = request.form['account_number']
        account_holder = request.form['account_holder']
        nif = request.form['nif']
        
        if update_bank_details(bank_name, iban, account_number, account_holder, nif):
            flash('Dados bancários atualizados com sucesso!', 'success')
        else:
            flash('Erro ao atualizar dados bancários.', 'error')
        
        return redirect(url_for('admin_settings'))
    
    bank_details = get_bank_details()
    return render_template('admin/settings.html', bank_details=bank_details)

@app.route('/admin/orders/update_status/<int:order_id>', methods=['POST'])
@login_required
def admin_update_order_status(order_id):
    status = request.form['status']
    if update_order_status(order_id, status):
        flash('Status do pedido atualizado com sucesso!', 'success')
    else:
        flash('Erro ao atualizar status do pedido.', 'error')
    return redirect(url_for('admin_orders'))

@app.route('/admin/orders/delete/<int:order_id>', methods=['POST'])
@login_required
def admin_delete_order(order_id):
    if delete_order(order_id):
        flash('Pedido excluído com sucesso!', 'success')
    else:
        flash('Erro ao excluir pedido.', 'error')
    return redirect(url_for('admin_orders'))

@app.route('/update_cart', methods=['POST'])
def update_cart():
    product_id = request.form.get('product_id')
    action = request.form.get('action')
    
    if 'cart' not in session:
        session['cart'] = {}
    
    if product_id in session['cart']:
        if action == 'increase':
            session['cart'][product_id] += 1
        elif action == 'decrease':
            session['cart'][product_id] -= 1
            if session['cart'][product_id] <= 0:
                del session['cart'][product_id]
        elif action == 'remove':
            del session['cart'][product_id]
    
    session.modified = True
    return redirect(url_for('index'))
