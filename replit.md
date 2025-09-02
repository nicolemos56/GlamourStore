# Overview

Nc Glamourstore is a Flask-based e-commerce web application for an online fashion store specializing in women's fashion, footwear, accessories, and beauty products. The application provides a complete shopping experience with product browsing, cart management, checkout process, and a comprehensive admin panel for managing products and orders.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Template Engine**: Jinja2 templates with Flask's built-in templating system
- **UI Framework**: Bootstrap 5 for responsive design and component styling
- **Design System**: Custom e-commerce theme with brand-specific color palette (primary green #5a7a5a and accent gold #d4af37)
- **Client-Side Enhancement**: Vanilla JavaScript for cart functionality, quantity controls, and visual feedback
- **Static Assets**: Organized CSS and JavaScript files with custom styling for enhanced user experience

## Backend Architecture
- **Web Framework**: Flask with modular route organization
- **ORM**: SQLAlchemy with declarative base for database operations
- **Authentication**: Flask-Login for admin panel access with secure password hashing
- **Session Management**: Flask's built-in session handling for cart persistence
- **File Upload**: Secure image upload system with file validation and unique naming
- **Admin Panel**: Complete administrative interface with product management, order tracking, and settings

## Database Architecture
- **Primary Database**: PostgreSQL for production (with SQLite fallback for development)
- **ORM Models**: User, Product, Order, OrderItem, Category, and BankDetails entities
- **Connection Management**: Pool recycling and pre-ping for reliable database connections
- **Data Initialization**: Automated default data seeding for categories, admin user, and sample products

## Cart and Session Management
- **Storage Method**: Server-side sessions for cart persistence across requests
- **Cart Operations**: Add, remove, update quantities, and clear cart functionality
- **Session Initialization**: Middleware ensures cart availability on all requests
- **State Persistence**: Cart data maintained throughout user browsing session

## Product Catalog System
- **Product Management**: Database-driven product catalog with admin CRUD operations
- **Image Handling**: Support for both URL-based and uploaded image storage
- **Category System**: Hierarchical product categorization with filtering capabilities
- **Search Functionality**: Text-based product search with category filtering
- **Pagination**: Configurable products per page with navigation controls

## Admin Management System
- **Authentication**: Secure login system with password hashing
- **Dashboard**: Statistics overview with product and order metrics
- **Product Management**: Full CRUD operations with image upload support
- **Order Management**: Order status tracking and customer information management
- **Settings Panel**: Bank details configuration for payment information

# External Dependencies

## Core Framework Dependencies
- **Flask**: Web application framework with SQLAlchemy integration
- **Flask-Login**: User session management for admin authentication
- **Werkzeug**: WSGI utilities including ProxyFix for deployment and secure filename handling

## Database and ORM
- **SQLAlchemy**: Object-relational mapping with declarative base
- **PostgreSQL**: Primary production database (with SQLite development fallback)
- **Database Drivers**: Appropriate drivers for PostgreSQL connectivity

## Frontend Libraries
- **Bootstrap 5**: CSS framework for responsive design and UI components
- **Font Awesome 6**: Icon library for enhanced visual interface
- **Custom Theme**: Brand-specific styling with green and gold color scheme

## File Handling
- **Werkzeug File Upload**: Secure file upload handling with validation
- **Image Processing**: File type validation for supported formats (PNG, JPG, JPEG, GIF, WebP)
- **Static File Serving**: Flask's built-in static file handling for uploaded images

## Development and Deployment
- **Environment Configuration**: Environment variable support for database URLs and secrets
- **Logging**: Python's built-in logging for debugging and monitoring
- **WSGI Middleware**: ProxyFix for proper header handling in production deployments