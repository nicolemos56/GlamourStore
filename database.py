from app import db
from models import User, Product, Order, OrderItem, Category
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
        
        db.session.commit()
        print("Default data initialized successfully!")
        
    except Exception as e:
        print(f"Error initializing default data: {e}")
        db.session.rollback()

def get_products():
    """Get all products from database"""
    try:
        products = Product.query.order_by(Product.created_at.desc()).all()
        return [
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
            for p in products
        ]
    except Exception as e:
        print(f"Error getting products: {e}")
        return []

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
        
        # Get total sales
        total_sales = db.session.query(func.coalesce(func.sum(Order.total_amount), 0)).filter(
            Order.status != 'cancelled'
        ).scalar()
        
        # Get recent orders
        recent_orders_query = Order.query.order_by(Order.created_at.desc()).limit(5).all()
        recent_orders = [
            {
                'id': o.id,
                'customer_name': o.customer_name,
                'total_amount': float(o.total_amount),
                'status': o.status,
                'created_at': o.created_at
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