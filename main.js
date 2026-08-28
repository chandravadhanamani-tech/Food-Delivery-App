/**
 * main.js — FoodApp Global JavaScript
 * Handles: Navbar scroll, cart badge updates, toast notifications, CSRF token
 */

// ---------- CSRF TOKEN ----------
function getCsrfToken() {
    const meta = document.querySelector('meta[name="csrf-token"]');
    if (meta) return meta.content;
    const hidden = document.querySelector('input[name="csrf_token"]');
    return hidden ? hidden.value : '';
}

// ---------- NAVBAR SCROLL EFFECT ----------
const nav = document.getElementById('mainNav');
window.addEventListener('scroll', function () {
    if (window.scrollY > 40) {
        nav && nav.classList.add('scrolled');
    } else {
        nav && nav.classList.remove('scrolled');
    }
}, { passive: true });

// ---------- CART BADGE ----------
function updateCartBadge(count) {
    const badge = document.getElementById('cartBadge');
    if (!badge) return;
    badge.textContent = count;
    if (count > 0) {
        badge.style.display = 'flex';
        badge.classList.add('bump');
        setTimeout(() => badge.classList.remove('bump'), 300);
    } else {
        badge.style.display = 'none';
    }
}

// Load cart count on page load
(function loadCartCount() {
    fetch('/cart/count')
        .then(r => r.json())
        .then(data => updateCartBadge(data.count))
        .catch(() => {});
})();

// ---------- TOAST NOTIFICATIONS ----------
let toastContainer = null;

function showToast(message, type = 'success') {
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container';
        document.body.appendChild(toastContainer);
    }

    const icons = {
        success: '✅',
        danger: '❌',
        warning: '⚠️',
        info: 'ℹ️'
    };

    const toast = document.createElement('div');
    toast.className = `food-toast ${type}`;
    toast.innerHTML = `
        <span style="font-size:1.2rem">${icons[type] || '🔔'}</span>
        <span style="font-weight:500;flex:1">${message}</span>
        <button onclick="this.parentElement.remove()" style="background:none;border:none;cursor:pointer;color:#9ca3af;font-size:1.1rem">✕</button>
    `;
    toastContainer.appendChild(toast);
    setTimeout(() => {
        toast.style.animation = 'slideOutRight 0.4s ease forwards';
        setTimeout(() => toast.remove(), 400);
    }, 4000);
}

// ---------- AUTO-DISMISS FLASH MESSAGES ----------
document.addEventListener('DOMContentLoaded', function () {
    const alerts = document.querySelectorAll('#flashContainer .alert');
    alerts.forEach((alert, i) => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000 + i * 500);
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(link => {
        link.addEventListener('click', function (e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                // Update active menu cat link
                document.querySelectorAll('.menu-cat-link').forEach(l => l.classList.remove('active'));
                const matchingLink = document.querySelector(`.menu-cat-link[href="${this.getAttribute('href')}"]`);
                if (matchingLink) matchingLink.classList.add('active');
            }
        });
    });

    // Intersection Observer for menu category nav highlight
    if (document.querySelector('.menu-section')) {
        const sections = document.querySelectorAll('.menu-section');
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const id = entry.target.getAttribute('id');
                    document.querySelectorAll('.menu-cat-link').forEach(l => l.classList.remove('active'));
                    const link = document.querySelector(`.menu-cat-link[href="#${id}"]`);
                    if (link) link.classList.add('active');
                }
            });
        }, { rootMargin: '-40% 0px -40% 0px' });
        sections.forEach(s => observer.observe(s));
    }
});

// ---------- CONFIRM DIALOGS ----------
document.querySelectorAll('[data-confirm]').forEach(el => {
    el.addEventListener('click', function (e) {
        if (!confirm(this.dataset.confirm)) e.preventDefault();
    });
});
