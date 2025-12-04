/* =====================================================
   C-CONNECT GLOBAL JAVASCRIPT
   Modern Theme Management & Utilities
   ===================================================== */

// ===== THEME MANAGEMENT =====
class ThemeManager {
    constructor() {
        this.themeKey = 'cconnect-theme';
        this.init();
    }

    init() {
        const savedTheme = localStorage.getItem(this.themeKey) || 'system';
        this.setTheme(savedTheme, false);

        const themeToggle = document.getElementById('themeToggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => this.toggleTheme());
        }
    }

    setTheme(theme, save = true) {
        document.body.setAttribute('data-theme', theme);
        
        const icon = document.getElementById('themeIcon');
        if (icon) {
            icon.className = theme === 'dark' ? 'bi bi-moon-stars-fill' : 'bi bi-sun-fill';
        }

        if (save) {
            localStorage.setItem(this.themeKey, theme);
        }

        // Dispatch custom event for theme change
        window.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme } }));
    }

    toggleTheme() {
        const currentTheme = document.body.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        this.setTheme(newTheme);
    }

    getTheme() {
        return document.body.getAttribute('data-theme');
    }
}

const themeManager = new ThemeManager();

// ===== SMOOTH SCROLL ANIMATIONS =====
class ScrollAnimations {
    constructor() {
        this.init();
    }

    init() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        this.observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                    this.observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        this.observeElements();
    }

    observeElements() {
        const elements = document.querySelectorAll('.animate-on-scroll');
        elements.forEach(el => this.observer.observe(el));
    }

    // Method to re-observe new dynamic elements
    refresh() {
        this.observeElements();
    }
}

const scrollAnimations = new ScrollAnimations();

// ===== NAVBAR SCROLL EFFECTS =====
let lastScroll = 0;
const navbar = document.querySelector('.navbar-glass');

if (navbar) {
    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll > 50) {
            navbar.style.boxShadow = 'var(--shadow-lg)';
        } else {
            navbar.style.boxShadow = 'var(--shadow-sm)';
        }
        
        lastScroll = currentScroll;
    });
}

// ===== AUTO-DISMISS ALERTS =====
document.addEventListener('DOMContentLoaded', () => {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getInstance(alert) || new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});

// ===== FORM VALIDATION =====
const forms = document.querySelectorAll('.needs-validation');
forms.forEach(form => {
    form.addEventListener('submit', event => {
        if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        }
        form.classList.add('was-validated');
    }, false);
});

// ===== UTILITY FUNCTIONS =====

// Show loading state on button
function showLoading(button) {
    const originalHTML = button.innerHTML;
    button.setAttribute('data-original-html', originalHTML);
    button.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
    button.disabled = true;
    return originalHTML;
}

// Hide loading state
function hideLoading(button) {
    const originalHTML = button.getAttribute('data-original-html');
    if (originalHTML) {
        button.innerHTML = originalHTML;
        button.disabled = false;
    }
}


// ===== AJAX FORM ACTIONS =====
function initializeAjaxActions() {
    document.addEventListener('click', function(e) {
        // Cancel connection requests
        if (e.target.matches('.cancel-btn')) {
            e.preventDefault();
            const button = e.target.closest('.cancel-btn');
            const connId = button.dataset.connId;
            
            const originalHTML = cconnect.showLoading(button);
            
            fetch(`/connections/cancel/${connId}`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('input[name="csrf_token"]').value
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.ok) {
                    // Fade out and remove connection item
                    const item = button.closest('.connection-item');
                    item.style.transition = 'opacity 0.3s ease';
                    item.style.opacity = '0';
                    setTimeout(() => { item.remove(); updateOutgoingCount();} , 300);
                    cconnect.showToast(data.message || 'Request cancelled', 'success');
                } else {
                    cconnect.showToast(data.message || 'Failed to cancel', 'danger');
                    cconnect.hideLoading(button);
                }
            })
            .catch(() => {
                cconnect.showToast('Network error occurred', 'danger');
                cconnect.hideLoading(button);
            });
        }
    });
}



// ===== UPDATE COUNTERS in the conenctions page =====
function updateOutgoingCount() {
    const outgoingItems = document.querySelectorAll('.connection-item');
    const badge = document.querySelector('.section-header .badge-count');
    
    if (badge) {
        const newCount = outgoingItems.length;
        badge.textContent = newCount;
        
        // Hide badge if zero
        if (newCount === 0) {
            badge.style.display = 'none';
            // Show empty state if no items
            const emptyState = document.querySelector('.empty-state');
            if (emptyState) {
                emptyState.style.display = 'block';
            }
        } else {
            badge.style.display = 'inline';
        }
    }
}



// Toast notification system
function showToast(message, type = 'info') {
    const toastContainer = document.querySelector('.toast-container') || createToastContainer();
    
    const icons = {
        success: 'check-circle-fill',
        error: 'exclamation-triangle-fill',
        danger: 'exclamation-triangle-fill',
        warning: 'exclamation-circle-fill',
        info: 'info-circle-fill'
    };
    
    const colors = {
        success: 'success',
        error: 'danger',
        danger: 'danger',
        warning: 'warning',
        info: 'info'
    };
    
    const toastHTML = `
        <div class="toast align-items-center text-bg-${colors[type]} border-0" role="alert" style="backdrop-filter: blur(10px);">
            <div class="d-flex">
                <div class="toast-body">
                    <i class="bi bi-${icons[type]} me-2"></i>${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    
    const toastElement = toastContainer.lastElementChild;
    const toast = new bootstrap.Toast(toastElement, { autohide: true, delay: 4000 });
    toast.show();
    
    toastElement.addEventListener('hidden.bs.toast', () => toastElement.remove());
}

function createToastContainer() {
    const container = document.createElement('div');
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    container.style.zIndex = '1060';
    container.style.marginTop = '80px';
    document.body.appendChild(container);
    return container;
}

// Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Animated counter
function animateCounter(element, target, duration = 2000) {
    const start = 0;
    const increment = target / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current);
        }
    }, 16);
}

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href !== '#' && href !== '') {
            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                const navHeight = document.querySelector('.navbar-glass').offsetHeight;
                const targetPosition = target.offsetTop - navHeight - 20;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        }
    });
});

// Image lazy loading
function lazyLoadImages() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// Initialize lazy loading on page load
document.addEventListener('DOMContentLoaded', lazyLoadImages);

// ===== PASSWORD VISIBILITY TOGGLE =====
function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    const icon = document.getElementById(`${inputId}-icon`);
    
    if (input && icon) {
        if (input.type === 'password') {
            input.type = 'text';
            icon.classList.remove('bi-eye');
            icon.classList.add('bi-eye-slash');
        } else {
            input.type = 'password';
            icon.classList.remove('bi-eye-slash');
            icon.classList.add('bi-eye');
        }
    }
}

// ===== SEARCH FUNCTIONALITY =====
function initializeSearch(inputId, itemsSelector) {
    const searchInput = document.getElementById(inputId);
    if (!searchInput) return;

    const debouncedSearch = debounce((query) => {
        const items = document.querySelectorAll(itemsSelector);
        const lowerQuery = query.toLowerCase();

        items.forEach(item => {
            const text = item.textContent.toLowerCase();
            if (text.includes(lowerQuery)) {
                item.style.display = '';
                item.classList.add('animate-on-scroll', 'animate-in');
            } else {
                item.style.display = 'none';
            }
        });
    }, 300);

    searchInput.addEventListener('input', (e) => {
        debouncedSearch(e.target.value);
    });
}

// ===== CARD HOVER EFFECTS =====
document.addEventListener('DOMContentLoaded', () => {
    const cards = document.querySelectorAll('.glass-card');
    
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transition = 'all 0.3s ease';
        });
    });
    initializeAjaxActions();
});

// ===== EXPORT GLOBAL API =====
window.cconnect = {
    themeManager,
    showLoading,
    hideLoading,
    showToast,
    debounce,
    animateCounter,
    togglePassword,
    initializeSearch,
    scrollAnimations,
    initializeAjaxActions,
    updateOutgoingCount
};

// Log initialization
console.log('✨ C-Connect: Global JavaScript initialized successfully!');

// ===== PAGE LOAD PERFORMANCE =====
window.addEventListener('load', () => {
    document.body.classList.add('fade-in');
    
    // Remove loading class if exists
    const loader = document.querySelector('.page-loader');
    if (loader) {
        loader.style.opacity = '0';
        setTimeout(() => loader.remove(), 300);
    }
});