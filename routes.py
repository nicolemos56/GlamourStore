from flask import render_template, request, session, redirect, url_for, jsonify, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from app import app, allowed_file, db
from database import get_dashboard_stats, get_products, get_orders, get_categories, add_product, update_product, delete_product, get_product_by_id, update_order_status, get_bank_details, update_bank_details
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
    db_products = get_products()
    
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
    
    return render_template('checkout.html', cart_items=cart_items, cart_total=cart_total)

@app.route('/finalizar')
def finalizar():
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
    
    # Get bank details for payment information
    bank_details = get_bank_details()
    
    return render_template('finalizar.html', cart_items=cart_items, cart_total=cart_total, bank_details=bank_details)

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

@app.route('/admin')
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    stats = get_dashboard_stats()
    return render_template('admin/dashboard.html', stats=stats)

@app.route('/admin/products')
@login_required
def admin_products():
    products = get_products()
    categories = get_categories()
    return render_template('admin/products.html', products=products, categories=categories)

@app.route('/admin/products/add', methods=['GET', 'POST'])
@login_required
def admin_add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        category = request.form['category']
        description = request.form['description']
        stock_quantity = int(request.form['stock_quantity'])
        
        # Handle image upload
        image_url = ''
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '' and allowed_file(file.filename):
                # Create unique filename
                filename = str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1].lower()
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                image_url = f'/static/images/products/{filename}'
        
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
        name = request.form['name']
        price = float(request.form['price'])
        category = request.form['category']
        description = request.form['description']
        stock_quantity = int(request.form['stock_quantity'])
        is_active = 'is_active' in request.form
        
        # Handle image upload
        image_url = product['image_url']  # Keep existing image by default
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '' and allowed_file(file.filename):
                # Delete old image if exists
                if image_url and image_url.startswith('/static/images/products/'):
                    old_filepath = image_url[1:]  # Remove leading slash
                    if os.path.exists(old_filepath):
                        os.remove(old_filepath)
                
                # Create unique filename
                filename = str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1].lower()
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                image_url = f'/static/images/products/{filename}'
        
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
    orders = get_orders()
    return render_template('admin/orders.html', orders=orders)

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
