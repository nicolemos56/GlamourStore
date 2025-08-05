from flask import render_template, request, session, redirect, url_for, jsonify
from app import app

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
    
    # Filter products based on search and category
    filtered_products = PRODUCTS
    
    if search_query:
        filtered_products = [p for p in filtered_products if search_query in p['name'].lower()]
    
    if category_filter:
        filtered_products = [p for p in filtered_products if p['category'] == category_filter]
    
    # Pagination
    total_products = len(filtered_products)
    total_pages = (total_products + per_page - 1) // per_page
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    paginated_products = filtered_products[start_index:end_index]
    
    # Calculate cart totals
    cart_total = 0
    cart_count = 0
    for product_id, quantity in session.get('cart', {}).items():
        product = next((p for p in PRODUCTS if p['id'] == int(product_id)), None)
        if product:
            cart_total += product['price'] * quantity
            cart_count += quantity
    
    return render_template('index.html', 
                         products=paginated_products,
                         categories=CATEGORIES,
                         cart_total=cart_total,
                         cart_count=cart_count,
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
    return redirect(url_for('index'))

@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    session['cart'] = {}
    session.modified = True
    return redirect(url_for('index'))

@app.route('/checkout')
def checkout():
    cart_items = []
    cart_total = 0
    
    for product_id, quantity in session.get('cart', {}).items():
        product = next((p for p in PRODUCTS if p['id'] == int(product_id)), None)
        if product:
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
        product = next((p for p in PRODUCTS if p['id'] == int(product_id)), None)
        if product:
            item_total = product['price'] * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total': item_total
            })
            cart_total += item_total
    
    return render_template('finalizar.html', cart_items=cart_items, cart_total=cart_total)

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
