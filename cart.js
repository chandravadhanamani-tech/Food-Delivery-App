/**
 * cart.js — FoodApp Cart JavaScript
 * Handles: Add to cart, update quantity, remove, clear cart via AJAX
 */

// Add to cart (called from menu page buttons)
function addToCart(itemId, itemName) {
    fetch('/cart/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify({ item_id: itemId, qty: 1 })
    })
    .then(r => r.json())
    .then(data => {
        if (data.success) {
            showToast(`${itemName} added to cart! 🛒`, 'success');
            updateCartBadge(data.cart_count);
        } else if (data.conflict) {
            // This is handled by the restaurant detail page's conflictModal
            throw { conflict: true, data };
        } else {
            showToast(data.message || 'Could not add item', 'danger');
        }
    })
    .catch(err => {
        if (err && err.conflict) {
            // Re-throw so detail page can catch it
        } else {
            showToast('Network error. Please try again.', 'danger');
        }
    });
}

// Update cart item quantity via AJAX (used on cart page)
function updateCartItemAjax(itemId, newQty, callback) {
    fetch('/cart/update', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify({ item_id: itemId, qty: newQty })
    })
    .then(r => r.json())
    .then(data => {
        if (data.success) {
            updateCartBadge(data.cart_count);
            if (callback) callback(data.summary);
        }
    });
}

// Remove item from cart
function removeCartItem(itemId) {
    if (!confirm('Remove this item?')) return;
    fetch(`/cart/remove/${itemId}`, {
        method: 'POST',
        headers: { 'X-CSRFToken': getCsrfToken() }
    })
    .then(() => location.reload());
}

// Clear entire cart
function clearCart(callback) {
    fetch('/cart/clear', {
        method: 'POST',
        headers: { 'X-CSRFToken': getCsrfToken() }
    })
    .then(r => r.json())
    .then(data => {
        if (data.success) {
            updateCartBadge(0);
            showToast('Cart cleared', 'info');
            if (callback) callback();
        }
    });
}
