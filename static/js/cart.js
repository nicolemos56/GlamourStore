// Cart functionality for Nc Glamourstore

document.addEventListener('DOMContentLoaded', function() {
    // Initialize cart functionality
    initializeCart();
    
    // Add smooth scrolling to checkout button
    const checkoutBtn = document.querySelector('a[href*="checkout"]');
    if (checkoutBtn) {
        checkoutBtn.addEventListener('click', function(e) {
            // Add a slight delay for better UX
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 150);
        });
    }
    
    // Add quantity change animations
    const quantitySelects = document.querySelectorAll('select[name="quantity"]');
    quantitySelects.forEach(select => {
        select.addEventListener('change', function() {
            this.style.backgroundColor = '#e7f3ff';
            setTimeout(() => {
                this.style.backgroundColor = '';
            }, 300);
        });
    });
    
    // Add product card hover effects
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    // Add to cart button animation
    const addToCartBtns = document.querySelectorAll('button[type="submit"]');
    addToCartBtns.forEach(btn => {
        if (btn.textContent.includes('Adicionar')) {
            btn.addEventListener('click', function(e) {
                // Visual feedback
                const originalText = this.innerHTML;
                this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Adicionando...';
                this.disabled = true;
                
                // Re-enable after form submission
                setTimeout(() => {
                    this.innerHTML = originalText;
                    this.disabled = false;
                }, 1000);
            });
        }
    });
    
    // Search input enhancement
    const searchInput = document.querySelector('input[name="search"]');
    if (searchInput) {
        searchInput.addEventListener('focus', function() {
            this.parentElement.style.boxShadow = '0 0 0 0.2rem rgba(111, 66, 193, 0.25)';
        });
        
        searchInput.addEventListener('blur', function() {
            this.parentElement.style.boxShadow = '';
        });
    }
    
    // Category link animations
    const categoryLinks = document.querySelectorAll('.list-group-item');
    categoryLinks.forEach(link => {
        link.addEventListener('click', function() {
            // Add loading state
            if (!this.classList.contains('active')) {
                const icon = document.createElement('i');
                icon.className = 'fas fa-spinner fa-spin ms-2';
                this.appendChild(icon);
            }
        });
    });
});

function initializeCart() {
    // Cart counter animation
    const cartCounter = document.querySelector('.cart-widget');
    if (cartCounter) {
        // Add pulse animation when cart is updated
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'childList') {
                    cartCounter.style.animation = 'pulse 0.5s ease-in-out';
                    setTimeout(() => {
                        cartCounter.style.animation = '';
                    }, 500);
                }
            });
        });
        
        observer.observe(cartCounter, { childList: true, subtree: true });
    }
    
    // Clear cart confirmation
    const clearCartBtn = document.querySelector('button[onclick*="confirm"]');
    if (clearCartBtn) {
        clearCartBtn.addEventListener('click', function(e) {
            if (!confirm('Tem certeza que deseja limpar todo o carrinho?')) {
                e.preventDefault();
            }
        });
    }
}

// Utility function for formatting currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('pt-AO', {
        style: 'currency',
        currency: 'AOA',
        minimumFractionDigits: 2
    }).format(amount);
}

// Function to show success messages
function showSuccessMessage(message) {
    const alert = document.createElement('div');
    alert.className = 'alert alert-success alert-dismissible fade show position-fixed';
    alert.style.top = '20px';
    alert.style.right = '20px';
    alert.style.zIndex = '9999';
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alert);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        if (alert.parentNode) {
            alert.parentNode.removeChild(alert);
        }
    }, 3000);
}

// Smooth scroll to top function
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Add CSS animation keyframes dynamically
const style = document.createElement('style');
style.textContent = `
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
`;
document.head.appendChild(style);
