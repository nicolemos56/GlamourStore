import sqlite3
import hashlib
from flask_login import UserMixin
from app import DATABASE_PATH

class AdminUser(UserMixin):
    def __init__(self, id, username, email, password_hash):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash

    @staticmethod
    def get(user_id):
        """Get user by ID"""
        try:
            connection = sqlite3.connect(DATABASE_PATH)
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM admin_users WHERE id = ?", (user_id,))
            user_data = cursor.fetchone()
            if user_data:
                return AdminUser(
                    user_data['id'],
                    user_data['username'],
                    user_data['email'],
                    user_data['password_hash']
                )
        except Exception as e:
            print(f"Error getting user: {e}")
        finally:
            if 'connection' in locals():
                connection.close()
        return None

    @staticmethod
    def get_by_username(username):
        """Get user by username"""
        try:
            connection = sqlite3.connect(DATABASE_PATH)
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM admin_users WHERE username = ?", (username,))
            user_data = cursor.fetchone()
            if user_data:
                return AdminUser(
                    user_data['id'],
                    user_data['username'],
                    user_data['email'],
                    user_data['password_hash']
                )
        except Exception as e:
            print(f"Error getting user by username: {e}")
        finally:
            if 'connection' in locals():
                connection.close()
        return None

    def check_password(self, password):
        """Check if provided password matches the hash"""
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()

def get_db_connection():
    """Get database connection"""
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection

def init_database():
    """Initialize database tables"""
    try:
        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()
        
        # Create admin_users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admin_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create products table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                category TEXT NOT NULL,
                image_url TEXT,
                description TEXT,
                stock_quantity INTEGER DEFAULT 0,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create orders table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                customer_phone TEXT NOT NULL,
                customer_email TEXT NOT NULL,
                customer_nif TEXT,
                delivery_method TEXT NOT NULL CHECK(delivery_method IN ('pickup', 'home_delivery')),
                payment_method TEXT NOT NULL,
                total_amount REAL NOT NULL,
                status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled')),
                delivery_address TEXT,
                observations TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create order_items table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                product_name TEXT NOT NULL,
                product_price REAL NOT NULL,
                quantity INTEGER NOT NULL,
                subtotal REAL NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
            )
        """)
        
        # Create categories table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Insert default categories
        categories = [
            'Acessórios', 'Bolsas', 'Calçados Femininos', 'Calçados Infantis',
            'Cosméticos', 'Produtos e acessórios de cabelo', 'Roupas Femininas'
        ]
        
        for category in categories:
            cursor.execute("""
                INSERT OR IGNORE INTO categories (name) VALUES (?)
            """, (category,))
        
        # Insert default admin user (username: admin, password: admin123)
        admin_password_hash = hashlib.sha256('admin123'.encode()).hexdigest()
        cursor.execute("""
            INSERT OR IGNORE INTO admin_users (username, email, password_hash) 
            VALUES (?, ?, ?)
        """, ('admin', 'admin@ncglamourstore.com', admin_password_hash))
        
        connection.commit()
        print("Database initialized successfully!")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        if 'connection' in locals():
            connection.close()

def get_products():
    """Get all products from database"""
    try:
        connection = sqlite3.connect(DATABASE_PATH)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("""
            SELECT p.*, c.name as category_name 
            FROM products p 
            LEFT JOIN categories c ON p.category = c.name 
            ORDER BY p.created_at DESC
        """)
        products = cursor.fetchall()
        return [dict(row) for row in products]
    except Exception as e:
        print(f"Error getting products: {e}")
        return []
    finally:
        if 'connection' in locals():
            connection.close()

def get_orders():
    """Get all orders from database"""
    try:
        connection = sqlite3.connect(DATABASE_PATH)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("""
            SELECT o.*, 
                   COUNT(oi.id) as total_items,
                   GROUP_CONCAT(oi.quantity || 'x ' || oi.product_name, ', ') as items_summary
            FROM orders o 
            LEFT JOIN order_items oi ON o.id = oi.order_id 
            GROUP BY o.id 
            ORDER BY o.created_at DESC
        """)
        orders = cursor.fetchall()
        return [dict(row) for row in orders]
    except Exception as e:
        print(f"Error getting orders: {e}")
        return []
    finally:
        if 'connection' in locals():
            connection.close()

def get_categories():
    """Get all categories from database"""
    try:
        connection = sqlite3.connect(DATABASE_PATH)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM categories ORDER BY name")
        categories = cursor.fetchall()
        return [dict(row) for row in categories]
    except Exception as e:
        print(f"Error getting categories: {e}")
        return []
    finally:
        if 'connection' in locals():
            connection.close()

def add_product(name, price, category, image_url="", description="", stock_quantity=0):
    """Add a new product to database"""
    try:
        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO products (name, price, category, image_url, description, stock_quantity)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, price, category, image_url, description, stock_quantity))
        connection.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"Error adding product: {e}")
        return None
    finally:
        if 'connection' in locals():
            connection.close()

def update_product(product_id, name, price, category, image_url="", description="", stock_quantity=0, is_active=True):
    """Update a product in database"""
    try:
        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE products 
            SET name=?, price=?, category=?, image_url=?, description=?, stock_quantity=?, is_active=?, updated_at=CURRENT_TIMESTAMP
            WHERE id=?
        """, (name, price, category, image_url, description, stock_quantity, is_active, product_id))
        connection.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error updating product: {e}")
        return False
    finally:
        if 'connection' in locals():
            connection.close()

def delete_product(product_id):
    """Delete a product from database"""
    try:
        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
        connection.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error deleting product: {e}")
        return False
    finally:
        if 'connection' in locals():
            connection.close()

def get_product_by_id(product_id):
    """Get a specific product by ID"""
    try:
        connection = sqlite3.connect(DATABASE_PATH)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM products WHERE id=?", (product_id,))
        product = cursor.fetchone()
        return dict(product) if product else None
    except Exception as e:
        print(f"Error getting product: {e}")
        return None
    finally:
        if 'connection' in locals():
            connection.close()

def update_order_status(order_id, status):
    """Update order status"""
    try:
        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE orders 
            SET status=?, updated_at=CURRENT_TIMESTAMP
            WHERE id=?
        """, (status, order_id))
        connection.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error updating order status: {e}")
        return False
    finally:
        if 'connection' in locals():
            connection.close()

def get_dashboard_stats():
    """Get dashboard statistics"""
    try:
        connection = sqlite3.connect(DATABASE_PATH)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        
        # Get total products
        cursor.execute("SELECT COUNT(*) as count FROM products WHERE is_active=1")
        total_products = cursor.fetchone()['count']
        
        # Get total orders
        cursor.execute("SELECT COUNT(*) as count FROM orders")
        total_orders = cursor.fetchone()['count']
        
        # Get pending orders
        cursor.execute("SELECT COUNT(*) as count FROM orders WHERE status='pending'")
        pending_orders = cursor.fetchone()['count']
        
        # Get total sales
        cursor.execute("SELECT COALESCE(SUM(total_amount), 0) as total FROM orders WHERE status NOT IN ('cancelled')")
        total_sales = cursor.fetchone()['total']
        
        # Get recent orders
        cursor.execute("""
            SELECT * FROM orders 
            ORDER BY created_at DESC 
            LIMIT 5
        """)
        recent_orders = [dict(row) for row in cursor.fetchall()]
        
        return {
            'total_products': total_products,
            'total_orders': total_orders,
            'pending_orders': pending_orders,
            'total_sales': total_sales,
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
    finally:
        if 'connection' in locals():
            connection.close()