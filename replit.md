# Overview

Nc Glamourstore é uma aplicação web de e-commerce baseada em Flask para uma loja online especializada em moda feminina, calçados, acessórios e produtos de beleza. A aplicação oferece uma experiência completa de navegação no catálogo com funcionalidade de carrinho de compras, incluindo produtos em categorias como cosméticos, roupas femininas, calçados, bolsas e acessórios. O sistema usa gerenciamento de carrinho baseado em sessões, inclui busca e filtragem por categoria, paginação de produtos, e processo de finalização de compra com formulário de dados pessoais.

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
- **Data Structure**: Expanded static product catalog with 32 products across all categories
- **Product Attributes**: ID, name, price, category, and external image URLs
- **Image Hosting**: External stock photos from Pixabay for product imagery
- **Categories**: Complete category coverage - Acessórios, Bolsas, Calçados Femininos, Calçados Infantis, Cosméticos, Produtos e acessórios de cabelo, Roupas Femininas
- **Pagination**: 8 products per page with navigation controls

## Search and Filtering
- **Search Implementation**: Server-side text matching against product names
- **Category Filtering**: URL parameter-based category selection with scrollable category list
- **Combined Filtering**: Support for simultaneous search and category filtering
- **Pagination**: Smart pagination with ellipsis for large page counts

## User Interface Enhancements
- **Quantity Selection**: Interactive +/- buttons for product quantity selection instead of dropdown
- **Checkout Process**: Two-page checkout flow - summary page and detailed finalizar page
- **Finalizar Page**: Complete order form with delivery method, payment options, personal data, and order summary
- **Footer**: Contact information including address, phone, email, and social links
- **Responsive Design**: Mobile-optimized layout with Bootstrap 5 components

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