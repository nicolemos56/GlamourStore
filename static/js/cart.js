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
    
    // Quantity controls functionality
    const quantityBtns = document.querySelectorAll('.quantity-btn');
    quantityBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const action = this.getAttribute('data-action');
            const input = this.closest('.input-group').querySelector('.quantity-input');
            let currentValue = parseInt(input.value);
            
            if (action === 'increase' && currentValue < 10) {
                input.value = currentValue + 1;
            } else if (action === 'decrease' && currentValue > 1) {
                input.value = currentValue - 1;
            }
            
            // Add visual feedback
            input.style.backgroundColor = '#e7f3ff';
            setTimeout(() => {
                input.style.backgroundColor = '';
            }, 300);
        });
    });
    
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
    
    // Add to cart functionality with AJAX
    const addToCartForms = document.querySelectorAll('form[action*="add_to_cart"]');
    addToCartForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            
            // Visual feedback
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Adicionando...';
            submitBtn.disabled = true;
            
            // Send AJAX request
            fetch('/add_to_cart', {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    updateCartDisplay(data.cart_total, data.cart_count);
                    showSuccessMessage(data.message);
                    
                    // Get updated cart items via another request
                    fetch('/get_cart_items', {
                        method: 'GET',
                        headers: {
                            'X-Requested-With': 'XMLHttpRequest'
                        }
                    })
                    .then(response => response.json())
                    .then(cartData => {
                        updateCartItemsList(cartData.cart_items);
                    });
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showErrorMessage('Erro ao adicionar produto ao carrinho');
            })
            .finally(() => {
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            });
        });
    });
    
    // Cart quantity controls
    const cartQuantityBtns = document.querySelectorAll('.cart-quantity-btn');
    cartQuantityBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const action = this.getAttribute('data-action');
            const productId = this.getAttribute('data-product-id');
            
            updateCartQuantity(productId, action);
        });
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

// Function to update cart display
function updateCartDisplay(total, count) {
    const cartTotalElement = document.getElementById('cart-total');
    const cartCountElement = document.getElementById('cart-count');
    
    if (cartTotalElement) {
        cartTotalElement.textContent = new Intl.NumberFormat('pt-PT', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        }).format(total);
    }
    
    if (cartCountElement) {
        cartCountElement.textContent = count;
    }
    
    // Add animation to cart widget
    const cartWidget = document.querySelector('.cart-widget');
    if (cartWidget) {
        cartWidget.style.animation = 'pulse 0.5s ease-in-out';
        setTimeout(() => {
            cartWidget.style.animation = '';
        }, 500);
    }
}

// Function to update cart quantities
function updateCartQuantity(productId, action) {
    fetch('/update_cart_quantity', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({
            product_id: productId,
            action: action
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateCartDisplay(data.cart_total, data.cart_count);
            updateCartItemsList(data.cart_items);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showErrorMessage('Erro ao atualizar carrinho');
    });
}

// Function to update cart items list
function updateCartItemsList(cartItems) {
    const cartItemsList = document.getElementById('cart-items-list');
    if (!cartItemsList) return;
    
    cartItemsList.innerHTML = '';
    
    cartItems.forEach(item => {
        const cartItemDiv = document.createElement('div');
        cartItemDiv.className = 'cart-item mb-2 p-2 border rounded';
        cartItemDiv.setAttribute('data-product-id', item.id);
        
        cartItemDiv.innerHTML = `
            <div class="d-flex justify-content-between align-items-center">
                <div class="flex-grow-1">
                    <h6 class="mb-1 small">${item.name}</h6>
                    <small class="text-muted">${new Intl.NumberFormat('pt-PT', {
                        minimumFractionDigits: 2,
                        maximumFractionDigits: 2
                    }).format(item.price)} Kz cada</small>
                </div>
                <div class="quantity-controls d-flex align-items-center">
                    <button type="button" class="btn btn-outline-secondary btn-sm cart-quantity-btn" 
                            data-action="decrease" data-product-id="${item.id}">
                        <i class="fas fa-minus"></i>
                    </button>
                    <span class="mx-2 quantity-display">${item.quantity}</span>
                    <button type="button" class="btn btn-outline-secondary btn-sm cart-quantity-btn" 
                            data-action="increase" data-product-id="${item.id}">
                        <i class="fas fa-plus"></i>
                    </button>
                </div>
            </div>
        `;
        
        cartItemsList.appendChild(cartItemDiv);
    });
    
    // Re-attach event listeners to new buttons
    const newQuantityBtns = cartItemsList.querySelectorAll('.cart-quantity-btn');
    newQuantityBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const action = this.getAttribute('data-action');
            const productId = this.getAttribute('data-product-id');
            updateCartQuantity(productId, action);
        });
    });
}

// Function to clear cart
function clearCart() {
    if (!confirm('Tem certeza que deseja limpar todo o carrinho?')) {
        return;
    }
    
    fetch('/clear_cart', {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(() => {
        updateCartDisplay(0, 0);
        updateCartItemsList([]);
        showSuccessMessage('Carrinho limpo com sucesso!');
    })
    .catch(error => {
        console.error('Error:', error);
        showErrorMessage('Erro ao limpar carrinho');
    });
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

// Function to show error messages
function showErrorMessage(message) {
    const alert = document.createElement('div');
    alert.className = 'alert alert-danger alert-dismissible fade show position-fixed';
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
