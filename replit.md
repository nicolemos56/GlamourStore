# Overview

Nc Glamourstore is a Flask-based e-commerce web application for an online store specializing in women's fashion and beauty products. The application provides a catalog browsing experience with shopping cart functionality, featuring products across categories like cosmetics, women's clothing, and footwear. The system uses session-based cart management and includes search and filtering capabilities for product discovery.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Template Engine**: Jinja2 templates with Flask's built-in templating
- **UI Framework**: Bootstrap 5 for responsive design and component styling
- **Static Assets**: Separate CSS and JavaScript files for custom styling and cart functionality
- **Client-Side Enhancement**: Vanilla JavaScript for interactive cart features and visual feedback

## Backend Architecture
- **Web Framework**: Flask with minimal configuration for rapid development
- **Session Management**: Flask's built-in session handling with server-side cart storage
- **Application Structure**: Simple modular design with separated routes and main application files
- **Data Storage**: In-memory product catalog using Python dictionaries (no persistent database)

## Cart Management
- **Storage Method**: Server-side sessions for cart persistence across requests
- **Cart Operations**: Add, remove, update quantities, and clear entire cart functionality
- **State Management**: Session initialization middleware ensures cart availability on all requests

## Product Catalog
- **Data Structure**: Static product definitions with hardcoded inventory
- **Product Attributes**: ID, name, price, category, and external image URLs
- **Image Hosting**: External stock photos from Pixabay for product imagery
- **Categories**: Dynamic category extraction from product data for filtering

## Search and Filtering
- **Search Implementation**: Server-side text matching against product names
- **Category Filtering**: URL parameter-based category selection
- **Combined Filtering**: Support for simultaneous search and category filtering

# External Dependencies

## Frontend Libraries
- **Bootstrap 5**: CSS framework for responsive design and UI components
- **Font Awesome 6**: Icon library for user interface elements

## Image Services
- **Pixabay**: External image hosting service for product photography

## Python Packages
- **Flask**: Core web framework for application structure
- **Werkzeug**: WSGI utilities including ProxyFix middleware for deployment

## Development Tools
- **Python Logging**: Built-in logging module for debugging and monitoring
- **Flask Debug Mode**: Development server with hot reloading capabilities

## Deployment Considerations
- **ProxyFix Middleware**: Configured for deployment behind reverse proxies
- **Environment Variables**: Session secret key configuration for production security
- **Static File Serving**: Flask's built-in static file handling for CSS and JavaScript assets