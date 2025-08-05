from flask import render_template, request, session, redirect, url_for, jsonify
from app import app

# Product data with stock photos
PRODUCTS = [
    {
        'id': 1,
        'name': 'Fantasy de Britney Spears',
        'price': 45000.00,
        'category': 'Cosméticos',
        'image': 'https://pixabay.com/get/gefaf048b1f878a0e65affe528390150aaefe0c361c9c54c94c450739e718f2995df2127b9d3c1675078e7840063be28dd9d25c8eb1e4af8a0a9524b47bb6f0e1_1280.jpg'
    },
    {
        'id': 2,
        'name': 'Água de colônia Oásis de ameixa',
        'price': 4000.00,
        'category': 'Cosméticos',
        'image': 'https://pixabay.com/get/g12ed2de27b4afee2361dbc3a1c7adbcb6ae45deac44faf20944cfde05af6351a0479e046e518db5a17ee8979165671acb21abee193079b97dab8c41355a1096d_1280.jpg'
    },
    {
        'id': 3,
        'name': 'Bota Salto',
        'price': 10000.00,
        'category': 'Calçados Femininos',
        'image': 'https://pixabay.com/get/g91f05702c486a4ab8bcf66241bd5a671d926f3e538f9a3a75b5d248979d6a9926e81f06d71fd71742d3ba4c607cc5e8dabf48d6820896f949e9d5e7c823ce8a9_1280.jpg'
    },
    {
        'id': 4,
        'name': 'Calça Leggings Jeans',
        'price': 10300.00,
        'category': 'Roupas Femininas',
        'image': 'https://pixabay.com/get/ge0415c4d9242983351b03f65c39b4cb2bacfa9229f42cc599c46b5bae682aa8d6c9e0a41c857665a1668492ce5c6c02561e4599f0784d0097930c1949eab191d_1280.jpg'
    },
    {
        'id': 5,
        'name': 'Calça Simples Jeans',
        'price': 10000.00,
        'category': 'Roupas Femininas',
        'image': 'https://pixabay.com/get/g4af863c0324c6979d1d940810387c5c89447f4000cef6172ddbfd4644a12a4096fc22d39deacc929b1666b9f1eb3e1f9cb2456f01e45bdd23d040d26d9e26de8_1280.jpg'
    },
    {
        'id': 6,
        'name': 'Calção Listrado',
        'price': 3800.00,
        'category': 'Roupas Femininas',
        'image': 'https://pixabay.com/get/g100d30f0f8140957b5a5d3c11953304918db529f9d970ed8f68fb20e63b2f1ededf42a77f5a6d2b5f1cdd593e7d61d905eda3ed2c8d718bc11718c649b43cbbe_1280.jpg'
    },
    {
        'id': 7,
        'name': 'Calça Cintura Subida Flare',
        'price': 15960.00,
        'category': 'Roupas Femininas',
        'image': 'https://pixabay.com/get/gd87698a8ed6225d5a046e574e2fe37ca8f72c9f1b260488a828b320e3c8894c9fe8670f0926ac122e3e5aff88596179698a92b7d799d178a469c2edacb4363b4_1280.jpg'
    },
    {
        'id': 8,
        'name': 'Calças Estampadas',
        'price': 14500.00,
        'category': 'Roupas Femininas',
        'image': 'https://pixabay.com/get/gffc3586a88cab25aad556492e8006c3fc0ea306ea4501ec34fd61383229500c9dc16b61473b4ef750fa01f3553b1a04801bbd11c757e42c42d2bb7cd8f64a3cd_1280.jpg'
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
    
    # Filter products based on search and category
    filtered_products = PRODUCTS
    
    if search_query:
        filtered_products = [p for p in filtered_products if search_query in p['name'].lower()]
    
    if category_filter:
        filtered_products = [p for p in filtered_products if p['category'] == category_filter]
    
    # Calculate cart totals
    cart_total = 0
    cart_count = 0
    for product_id, quantity in session.get('cart', {}).items():
        product = next((p for p in PRODUCTS if p['id'] == int(product_id)), None)
        if product:
            cart_total += product['price'] * quantity
            cart_count += quantity
    
    return render_template('index.html', 
                         products=filtered_products,
                         categories=CATEGORIES,
                         cart_total=cart_total,
                         cart_count=cart_count,
                         current_search=request.args.get('search', ''),
                         current_category=category_filter)

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
