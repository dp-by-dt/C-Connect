/* =====================================================
   C-CONNECT GLOBAL JAVASCRIPT
   Theme Management & Utility Functions
   ===================================================== */

// ===== THEME MANAGEMENT SYSTEM =====
class ThemeManager {
    constructor() {
        this.themeKey = 'cconnect-theme';
        this.colorKey = 'cconnect-accent-color';
        this.init();
    }

    init() {
        // Load saved theme or default to light
        const savedTheme = localStorage.getItem(this.themeKey) || 'light';
        this.setTheme(savedTheme, false);

        // Load saved accent color if exists
        const savedColor = localStorage.getItem(this.colorKey);
        if (savedColor) {
            this.setAccentColor(savedColor, false);
        }

        // Setup theme toggle button
        const themeToggle = document.getElementById('themeToggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => this.toggleTheme());
        }
    }

    setTheme(theme, save = true) {
        document.body.setAttribute('data-theme', theme);
        
        // Update theme icon
        const icon = document.getElementById('themeIcon');
        if (icon) {
            if (theme === 'dark') {
                icon.className = 'bi bi-moon-stars-fill';
            } else {
                icon.className = 'bi bi-sun-fill';
            }
        }

        if (save) {
            localStorage.setItem(this.themeKey, theme);
        }
    }

    toggleTheme() {
        const currentTheme = document.body.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        this.setTheme(newTheme);
    }

    setAccentColor(color, save = true) {
        document.documentElement.style.setProperty('--primary-color', color);
        
        if (save) {
            localStorage.setItem(this.colorKey, color);
        }
    }

    getTheme() {
        return document.body.getAttribute('data-theme');
    }
}

// Initialize theme manager
const themeManager = new ThemeManager();

// ===== SMOOTH SCROLLING FOR ANCHOR LINKS =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href !== '#' && href !== '') {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
    });
});

// ===== AUTO-DISMISS ALERTS AFTER 5 SECONDS =====
document.addEventListener('DOMContentLoaded', () => {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});

// ===== FORM VALIDATION ENHANCEMENT =====
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

// ===== NAVBAR SCROLL EFFECT =====
let lastScroll = 0;
const navbar = document.querySelector('.navbar-glass');

if (navbar) {
    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll <= 0) {
            navbar.style.boxShadow = 'var(--shadow-sm)';
        } else {
            navbar.style.boxShadow = 'var(--shadow-md)';
        }
        
        lastScroll = currentScroll;
    });
}

// ===== UTILITY FUNCTIONS =====

// Show loading spinner on button
function showLoading(button) {
    const originalText = button.innerHTML;
    button.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
    button.disabled = true;
    return originalText;
}

// Hide loading spinner on button
function hideLoading(button, originalText) {
    button.innerHTML = originalText;
    button.disabled = false;
}

// Show toast notification
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
        <div class="toast align-items-center text-bg-${colors[type]} border-0" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">
                    <i class="bi bi-${icons[type]} me-2"></i>
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    
    const toastElement = toastContainer.lastElementChild;
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
    
    toastElement.addEventListener('hidden.bs.toast', () => {
        toastElement.remove();
    });
}

function createToastContainer() {
    const container = document.createElement('div');
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    container.style.zIndex = '1060';
    document.body.appendChild(container);
    return container;
}

// Debounce function for search/filter
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

// ===== ANIMATED COUNTER =====
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

// ===== INTERSECTION OBSERVER FOR SCROLL ANIMATIONS =====
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate-in');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe elements with animation class
document.addEventListener('DOMContentLoaded', () => {
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    animatedElements.forEach(el => observer.observe(el));
});

// Export functions for use in other scripts
window.cconnect = {
    themeManager,
    showLoading,
    hideLoading,
    showToast,
    debounce,
    animateCounter
};

console.log('C-Connect: Global JS loaded successfully!');