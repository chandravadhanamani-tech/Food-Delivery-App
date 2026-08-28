/**
 * order-tracking.js — FoodApp Real-time Order Tracking
 * Polls /orders/<id>/status every 10 seconds and updates the UI
 */

let trackingInterval = null;
let lastStatus = null;

function startTracking(orderId, currentStatus) {
    lastStatus = currentStatus;
    // Poll every 10 seconds
    trackingInterval = setInterval(() => {
        pollOrderStatus(orderId);
    }, 10000);
}

function stopTracking() {
    if (trackingInterval) {
        clearInterval(trackingInterval);
        trackingInterval = null;
    }
}

function pollOrderStatus(orderId) {
    fetch(`/orders/${orderId}/status`)
        .then(r => r.json())
        .then(data => {
            if (data.status !== lastStatus) {
                lastStatus = data.status;
                updateTrackingUI(data);

                // Stop polling if terminal state
                if (['delivered', 'cancelled'].includes(data.status)) {
                    stopTracking();
                    const spinner = document.getElementById('trackingSpinner');
                    if (spinner) spinner.style.display = 'none';

                    // Reload page for fresh action buttons
                    setTimeout(() => location.reload(), 1500);
                }
            }
        })
        .catch(() => {
            // Silent fail — network issue
        });
}

function updateTrackingUI(data) {
    // Update status banner
    const statusLabel = document.getElementById('statusLabel');
    const statusSub = document.getElementById('statusSub');
    if (statusLabel) statusLabel.textContent = data.label;

    const subtitles = {
        'placed': 'Your order is waiting for confirmation',
        'confirmed': 'Restaurant has confirmed your order',
        'preparing': 'The kitchen is preparing your food 🔥',
        'out_for_delivery': 'Your order is on the way! 🛵',
        'delivered': 'Enjoy your meal! 😋',
        'cancelled': 'Order was cancelled'
    };
    if (statusSub) statusSub.textContent = subtitles[data.status] || '';

    // Update timeline steps
    if (data.timeline) {
        data.timeline.forEach(step => {
            const el = document.getElementById(`step-${step.status}`);
            if (el) {
                el.className = `timeline-step ${step.state}`;
            }
        });
    }

    // Update delivery partner info
    if (data.delivery_partner) {
        const partnerEl = document.getElementById('partnerInfo');
        if (partnerEl) partnerEl.textContent = data.delivery_partner;
    }

    // Show toast for status change
    const messages = {
        'confirmed': '✅ Order confirmed by restaurant!',
        'preparing': '👨‍🍳 Your food is being prepared!',
        'out_for_delivery': '🛵 Your order is on the way!',
        'delivered': '🎉 Order delivered! Enjoy your meal!',
        'cancelled': '❌ Order has been cancelled.'
    };
    if (messages[data.status]) {
        showToast(messages[data.status], data.status === 'cancelled' ? 'danger' : 'success');
    }
}
