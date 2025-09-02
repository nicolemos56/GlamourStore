from app import db
from models import User, Product, Order, OrderItem, Category, BankDetails
from sqlalchemy import func

def init_default_data():
    """Initialize default data for the application"""
    try:
        # Insert default categories
        categories = [
            'Acessórios', 'Bolsas', 'Calçados Femininos', 'Calçados Infantis',
            'Cosméticos', 'Produtos e acessórios de cabelo', 'Roupas Femininas'
        ]
        
        for category_name in categories:
            if not Category.query.filter_by(name=category_name).first():
                category = Category(name=category_name)
                db.session.add(category)
        
        # Insert default admin user (username: admin, password: admin123)
        if not User.query.filter_by(username='admin').first():
            admin_user = User(
                username='admin',
                email='admin@ncglamourstore.com'
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
        
        # Add default products if none exist
        if Product.query.count() == 0:
            default_products = [
                # Cosméticos
                {
                    'name': 'Fantasy de Britney Spears',
                    'price': 45000.00,
                    'category': 'Cosméticos',
                    'description': 'Perfume feminino Fantasy de Britney Spears, fragância doce e envolvente.',
                    'stock_quantity': 10
                },
                {
                    'name': 'Água de colônia Oásis de ameixa',
                    'price': 4000.00,
                    'category': 'Cosméticos',
                    'description': 'Água de colônia com fragrância fresca de ameixa.',
                    'stock_quantity': 25
                },
                {
                    'name': 'Batom Matte Vermelho',
                    'price': 8500.00,
                    'category': 'Cosméticos',
                    'description': 'Batom matte de longa duração na cor vermelho clássico.',
                    'stock_quantity': 15
                },
                {
                    'name': 'Base Líquida Natural',
                    'price': 12000.00,
                    'category': 'Cosméticos',
                    'description': 'Base líquida com cobertura natural e acabamento sedoso.',
                    'stock_quantity': 20
                },
                {
                    'name': 'Máscara de Cílios Volume',
                    'price': 15000.00,
                    'category': 'Cosméticos',
                    'description': 'Máscara para cílios que proporciona volume e alongamento.',
                    'stock_quantity': 18
                },
                
                # Calçados Femininos
                {
                    'name': 'Bota Salto',
                    'price': 10000.00,
                    'category': 'Calçados Femininos',
                    'description': 'Bota elegante com salto médio, ideal para ocasiões especiais.',
                    'stock_quantity': 12
                },
                {
                    'name': 'Sandália Elegante',
                    'price': 8500.00,
                    'category': 'Calçados Femininos',
                    'description': 'Sandália feminina elegante para eventos e festas.',
                    'stock_quantity': 15
                },
                {
                    'name': 'Tênis Casual Branco',
                    'price': 12500.00,
                    'category': 'Calçados Femininos',
                    'description': 'Tênis branco casual confortável para o dia a dia.',
                    'stock_quantity': 20
                },
                {
                    'name': 'Sapato Social Feminino',
                    'price': 14000.00,
                    'category': 'Calçados Femininos',
                    'description': 'Sapato social feminino para ambiente profissional.',
                    'stock_quantity': 10
                },
                
                # Roupas Femininas
                {
                    'name': 'Calça Leggings Jeans',
                    'price': 10300.00,
                    'category': 'Roupas Femininas',
                    'description': 'Calça leggings com design jeans, confortável e estilosa.',
                    'stock_quantity': 25
                },
                {
                    'name': 'Calça Simples Jeans',
                    'price': 10000.00,
                    'category': 'Roupas Femininas',
                    'description': 'Calça jeans clássica de corte simples e versátil.',
                    'stock_quantity': 30
                },
                {
                    'name': 'Calção Listrado',
                    'price': 3800.00,
                    'category': 'Roupas Femininas',
                    'description': 'Calção listrado leve e confortável para o verão.',
                    'stock_quantity': 22
                },
                {
                    'name': 'Calça Cintura Subida Flare',
                    'price': 15960.00,
                    'category': 'Roupas Femininas',
                    'description': 'Calça de cintura alta com corte flare, muito elegante.',
                    'stock_quantity': 18
                },
                {
                    'name': 'Calças Estampadas',
                    'price': 14500.00,
                    'category': 'Roupas Femininas',
                    'description': 'Calças com estampas modernas e coloridas.',
                    'stock_quantity': 16
                },
                {
                    'name': 'Vestido Casual Verão',
                    'price': 18000.00,
                    'category': 'Roupas Femininas',
                    'description': 'Vestido casual perfeito para os dias quentes de verão.',
                    'stock_quantity': 14
                },
                {
                    'name': 'Blusa Social Feminina',
                    'price': 12500.00,
                    'category': 'Roupas Femininas',
                    'description': 'Blusa social feminina para ambiente profissional.',
                    'stock_quantity': 20
                },
                
                # Bolsas
                {
                    'name': 'Bolsa de Mão Couro',
                    'price': 25000.00,
                    'category': 'Bolsas',
                    'description': 'Bolsa de mão em couro legítimo, elegante e durável.',
                    'stock_quantity': 8
                },
                {
                    'name': 'Carteira Feminina Elegante',
                    'price': 8500.00,
                    'category': 'Bolsas',
                    'description': 'Carteira feminina com design elegante e múltiplos compartimentos.',
                    'stock_quantity': 25
                },
                {
                    'name': 'Mochila Casual Urbana',
                    'price': 15000.00,
                    'category': 'Bolsas',
                    'description': 'Mochila urbana casual com design moderno.',
                    'stock_quantity': 12
                },
                {
                    'name': 'Bolsa Tiracolo Moderna',
                    'price': 18500.00,
                    'category': 'Bolsas',
                    'description': 'Bolsa tiracolo com design moderno e funcional.',
                    'stock_quantity': 15
                },
                
                # Acessórios
                {
                    'name': 'Colar Dourado Delicado',
                    'price': 12000.00,
                    'category': 'Acessórios',
                    'description': 'Colar dourado delicado para ocasiões especiais.',
                    'stock_quantity': 20
                },
                {
                    'name': 'Brincos Pérola Clássicos',
                    'price': 15500.00,
                    'category': 'Acessórios',
                    'description': 'Brincos de pérola clássicos e elegantes.',
                    'stock_quantity': 18
                },
                {
                    'name': 'Relógio Feminino Elegante',
                    'price': 35000.00,
                    'category': 'Acessórios',
                    'description': 'Relógio feminino elegante com pulseira de couro.',
                    'stock_quantity': 10
                },
                {
                    'name': 'Óculos de Sol Fashion',
                    'price': 22000.00,
                    'category': 'Acessórios',
                    'description': 'Óculos de sol com design fashion e proteção UV.',
                    'stock_quantity': 12
                },
                
                # Calçados Infantis
                {
                    'name': 'Tênis Infantil Colorido',
                    'price': 8500.00,
                    'category': 'Calçados Infantis',
                    'description': 'Tênis colorido e confortável para crianças.',
                    'stock_quantity': 20
                },
                {
                    'name': 'Sandália Infantil Confortável',
                    'price': 6500.00,
                    'category': 'Calçados Infantis',
                    'description': 'Sandália infantil confortável para uso diário.',
                    'stock_quantity': 25
                },
                {
                    'name': 'Sapatinho de Bebê',
                    'price': 4500.00,
                    'category': 'Calçados Infantis',
                    'description': 'Sapatinho macio e seguro para bebês.',
                    'stock_quantity': 30
                },
                
                # Produtos e acessórios de cabelo
                {
                    'name': 'Shampoo Nutritivo 500ml',
                    'price': 9500.00,
                    'category': 'Produtos e acessórios de cabelo',
                    'description': 'Shampoo nutritivo que fortalece e hidrata os cabelos.',
                    'stock_quantity': 40
                },
                {
                    'name': 'Condicionador Hidratante',
                    'price': 8500.00,
                    'category': 'Produtos e acessórios de cabelo',
                    'description': 'Condicionador hidratante para cabelos macios e sedosos.',
                    'stock_quantity': 35
                },
                {
                    'name': 'Escova de Cabelo Premium',
                    'price': 12000.00,
                    'category': 'Produtos e acessórios de cabelo',
                    'description': 'Escova de cabelo premium com cerdas naturais.',
                    'stock_quantity': 15
                },
                {
                    'name': 'Presilhas Decorativas Kit',
                    'price': 5500.00,
                    'category': 'Produtos e acessórios de cabelo',
                    'description': 'Kit com presilhas decorativas variadas para cabelos.',
                    'stock_quantity': 50
                },
                {
                    'name': 'Óleo Capilar Reparador',
                    'price': 15500.00,
                    'category': 'Produtos e acessórios de cabelo',
                    'description': 'Óleo capilar reparador para cabelos danificados.',
                    'stock_quantity': 20
                }
            ]
            
            for product_data in default_products:
                product = Product(**product_data)
                db.session.add(product)
        
        # Add default bank details if none exist
        if BankDetails.query.count() == 0:
            default_bank = BankDetails(
                bank_name='Banco Económico',
                iban='AO06 0058 0000 1234 5678 9012 3',
                account_number='123456789',
                account_holder='NC Glamour Store, Lda',
                nif='5417022456',
                is_active=True
            )
            db.session.add(default_bank)
        
        db.session.commit()
        print("Default data initialized successfully!")
        
    except Exception as e:
        print(f"Error initializing default data: {e}")
        db.session.rollback()

def get_products(page=1, per_page=10):
    """Get products from database with pagination"""
    try:
        products_pagination = Product.query.order_by(Product.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        products = [
            {
                'id': p.id,
                'name': p.name,
                'price': float(p.price),
                'category': p.category,
                'image_url': p.image_url,
                'description': p.description,
                'stock_quantity': p.stock_quantity,
                'is_active': p.is_active,
                'created_at': p.created_at,
                'updated_at': p.updated_at
            }
            for p in products_pagination.items
        ]
        
        return {
            'products': products,
            'pagination': {
                'page': products_pagination.page,
                'pages': products_pagination.pages,
                'per_page': products_pagination.per_page,
                'total': products_pagination.total,
                'has_prev': products_pagination.has_prev,
                'has_next': products_pagination.has_next,
                'prev_num': products_pagination.prev_num,
                'next_num': products_pagination.next_num
            }
        }
    except Exception as e:
        print(f"Error getting products: {e}")
        return {
            'products': [],
            'pagination': {
                'page': 1,
                'pages': 1,
                'per_page': per_page,
                'total': 0,
                'has_prev': False,
                'has_next': False,
                'prev_num': None,
                'next_num': None
            }
        }

def get_orders():
    """Get all orders from database"""
    try:
        orders = Order.query.order_by(Order.created_at.desc()).all()
        result = []
        for order in orders:
            total_items = len(order.items)
            items_summary = ', '.join([f"{item.quantity}x {item.product_name}" for item in order.items])
            
            result.append({
                'id': order.id,
                'customer_name': order.customer_name,
                'customer_phone': order.customer_phone,
                'customer_email': order.customer_email,
                'customer_nif': order.customer_nif,
                'delivery_method': order.delivery_method,
                'payment_method': order.payment_method,
                'total_amount': float(order.total_amount),
                'status': order.status,
                'delivery_address': order.delivery_address,
                'observations': order.observations,
                'created_at': order.created_at,
                'updated_at': order.updated_at,
                'total_items': total_items,
                'items_summary': items_summary
            })
        return result
    except Exception as e:
        print(f"Error getting orders: {e}")
        return []

def get_categories():
    """Get all categories from database"""
    try:
        categories = Category.query.order_by(Category.name).all()
        return [
            {
                'id': c.id,
                'name': c.name,
                'description': c.description,
                'is_active': c.is_active,
                'created_at': c.created_at
            }
            for c in categories
        ]
    except Exception as e:
        print(f"Error getting categories: {e}")
        return []

def add_product(name, price, category, image_url="", description="", stock_quantity=0):
    """Add a new product to database"""
    try:
        product = Product(
            name=name,
            price=price,
            category=category,
            image_url=image_url,
            description=description,
            stock_quantity=stock_quantity
        )
        db.session.add(product)
        db.session.commit()
        return product.id
    except Exception as e:
        print(f"Error adding product: {e}")
        db.session.rollback()
        return None

def update_product(product_id, name, price, category, image_url="", description="", stock_quantity=0, is_active=True):
    """Update a product in database"""
    try:
        product = Product.query.get(product_id)
        if product:
            product.name = name
            product.price = price
            product.category = category
            product.image_url = image_url
            product.description = description
            product.stock_quantity = stock_quantity
            product.is_active = is_active
            db.session.commit()
            return True
        return False
    except Exception as e:
        print(f"Error updating product: {e}")
        db.session.rollback()
        return False

def delete_product(product_id):
    """Delete a product from database"""
    try:
        product = Product.query.get(product_id)
        if product:
            db.session.delete(product)
            db.session.commit()
            return True
        return False
    except Exception as e:
        print(f"Error deleting product: {e}")
        db.session.rollback()
        return False

def get_product_by_id(product_id):
    """Get a specific product by ID"""
    try:
        product = Product.query.get(product_id)
        if product:
            return {
                'id': product.id,
                'name': product.name,
                'price': float(product.price),
                'category': product.category,
                'image_url': product.image_url,
                'description': product.description,
                'stock_quantity': product.stock_quantity,
                'is_active': product.is_active,
                'created_at': product.created_at,
                'updated_at': product.updated_at
            }
        return None
    except Exception as e:
        print(f"Error getting product: {e}")
        return None

def update_order_status(order_id, status):
    """Update order status"""
    try:
        order = Order.query.get(order_id)
        if order:
            order.status = status
            db.session.commit()
            return True
        return False
    except Exception as e:
        print(f"Error updating order status: {e}")
        db.session.rollback()
        return False

def get_dashboard_stats():
    """Get dashboard statistics"""
    try:
        # Get total products
        total_products = Product.query.filter_by(is_active=True).count()
        
        # Get total orders
        total_orders = Order.query.count()
        
        # Get pending orders
        pending_orders = Order.query.filter_by(status='pending').count()
        
        # Get total sales (only delivered orders)
        total_sales = db.session.query(func.coalesce(func.sum(Order.total_amount), 0)).filter(
            Order.status == 'delivered'
        ).scalar()
        
        # Get recent orders
        recent_orders_query = Order.query.order_by(Order.created_at.desc()).limit(5).all()
        recent_orders = [
            {
                'id': o.id,
                'customer_name': o.customer_name,
                'total_amount': float(o.total_amount),
                'status': o.status,
                'created_at': o.created_at.strftime('%Y-%m-%d') if o.created_at else 'N/A'
            }
            for o in recent_orders_query
        ]
        
        return {
            'total_products': total_products,
            'total_orders': total_orders,
            'pending_orders': pending_orders,
            'total_sales': float(total_sales) if total_sales else 0,
            'recent_orders': recent_orders
        }
    except Exception as e:
        print(f"Error getting dashboard stats: {e}")
        return {
            'total_products': 0,
            'total_orders': 0,
            'pending_orders': 0,
            'total_sales': 0,
            'recent_orders': []
        }

def get_bank_details():
    """Get active bank details"""
    try:
        bank_details = BankDetails.query.filter_by(is_active=True).first()
        if bank_details:
            return {
                'id': bank_details.id,
                'bank_name': bank_details.bank_name,
                'iban': bank_details.iban,
                'account_number': bank_details.account_number,
                'account_holder': bank_details.account_holder,
                'nif': bank_details.nif,
                'is_active': bank_details.is_active,
                'created_at': bank_details.created_at,
                'updated_at': bank_details.updated_at
            }
        return None
    except Exception as e:
        print(f"Error getting bank details: {e}")
        return None

def update_bank_details(bank_name, iban, account_number, account_holder, nif):
    """Update bank details"""
    try:
        # Get existing bank details or create new one
        bank_details = BankDetails.query.filter_by(is_active=True).first()
        if bank_details:
            bank_details.bank_name = bank_name
            bank_details.iban = iban
            bank_details.account_number = account_number
            bank_details.account_holder = account_holder
            bank_details.nif = nif
        else:
            bank_details = BankDetails(
                bank_name=bank_name,
                iban=iban,
                account_number=account_number,
                account_holder=account_holder,
                nif=nif,
                is_active=True
            )
            db.session.add(bank_details)
        
        db.session.commit()
        return True
    except Exception as e:
        print(f"Error updating bank details: {e}")
        db.session.rollback()
        return False