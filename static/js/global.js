/* =====================================================
   C-CONNECT GLOBAL JAVASCRIPT v2.0
   Modern Interactions & Utilities
   ===================================================== */

// ==================== THEME MANAGEMENT ====================
class ThemeManager {
    constructor() {
        this.themeKey = 'cconnect-theme';
        this.init();
    }

    init() {
        // Get saved theme or default to 'light'
        const savedTheme = localStorage.getItem(this.themeKey) || 'light';
        this.setTheme(savedTheme, false);

        // Setup theme toggle button
        const themeToggle = document.getElementById('themeToggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => this.toggleTheme());
        }
    }

    setTheme(theme, save = true) {
        // Apply theme class to html element
        if (theme === 'dark') {
            document.documentElement.classList.add('theme-dark');
        } else {
            document.documentElement.classList.remove('theme-dark');
        }
        
        // Update icon
        const icon = document.getElementById('themeIcon');
        if (icon) {
            icon.className = theme === 'dark' ? 'bi bi-moon-stars-fill' : 'bi bi-sun-fill';
        }

        // Save to localStorage if needed
        if (save) {
            localStorage.setItem(this.themeKey, theme);
        }

        // Dispatch custom event
        window.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme } }));
    }

    toggleTheme() {
        const currentTheme = document.documentElement.classList.contains('theme-dark') ? 'dark' : 'light';
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        this.setTheme(newTheme);
    }

    getTheme() {
        return document.documentElement.classList.contains('theme-dark') ? 'dark' : 'light';
    }
}

// Initialize theme manager
const themeManager = new ThemeManager();

// ==================== SIDEBAR TOGGLE (DESKTOP) ====================
document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');

    if (sidebar && sidebarToggle) {
        // Load saved sidebar state
        const savedState = localStorage.getItem('sidebar-expanded');
        if (savedState === 'true') {
            sidebar.classList.add('is-expanded');
        }

        // Toggle sidebar on button click
        sidebarToggle.addEventListener('click', () => {
            sidebar.classList.toggle('is-expanded');
            const isExpanded = sidebar.classList.contains('is-expanded');
            localStorage.setItem('sidebar-expanded', isExpanded);
        });
    }
});

// ==================== MOBILE MENU (OVERLAY) ====================
document.addEventListener('DOMContentLoaded', () => {
    const mobileMenu = document.getElementById('mobileMenu');
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const mobileMenuClose = document.getElementById('mobileMenuClose');
    const mobileMenuOverlay = document.getElementById('mobileMenuOverlay');

    if (mobileMenu && mobileMenuToggle) {
        // Open mobile menu
        mobileMenuToggle.addEventListener('click', () => {
            mobileMenu.classList.add('is-open');
            document.body.style.overflow = 'hidden';
        });

        // Close mobile menu
        const closeMobileMenu = () => {
            mobileMenu.classList.remove('is-open');
            document.body.style.overflow = '';
        };

        if (mobileMenuClose) {
            mobileMenuClose.addEventListener('click', closeMobileMenu);
        }

        if (mobileMenuOverlay) {
            mobileMenuOverlay.addEventListener('click', closeMobileMenu);
        }

        // Close on navigation link click
        const mobileLinks = mobileMenu.querySelectorAll('.mobile-menu__link');
        mobileLinks.forEach(link => {
            link.addEventListener('click', closeMobileMenu);
        });

        // Close on ESC key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && mobileMenu.classList.contains('is-open')) {
                closeMobileMenu();
            }
        });
    }
});

// ==================== PROFILE DROPDOWN ====================
document.addEventListener('DOMContentLoaded', () => {
    const profileDropdown = document.getElementById('profileDropdown');
    const profileBtn = profileDropdown?.querySelector('.topbar__profile-btn');

    if (profileDropdown && profileBtn) {
        // Toggle dropdown
        profileBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            profileDropdown.classList.toggle('is-open');
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', (e) => {
            if (!profileDropdown.contains(e.target)) {
                profileDropdown.classList.remove('is-open');
            }
        });

        // Close on ESC key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                profileDropdown.classList.remove('is-open');
            }
        });
    }
});

// ==================== GUEST MOBILE MENU ====================
document.addEventListener('DOMContentLoaded', () => {
    const guestMenuToggle = document.getElementById('guestMenuToggle');
    const guestMobileMenu = document.getElementById('guestMobileMenu');

    if (guestMenuToggle && guestMobileMenu) {
        guestMenuToggle.addEventListener('click', () => {
            guestMobileMenu.classList.toggle('is-open');
            const icon = guestMenuToggle.querySelector('i');
            if (icon) {
                if (guestMobileMenu.classList.contains('is-open')) {
                    icon.classList.remove('bi-list');
                    icon.classList.add('bi-x-lg');
                } else {
                    icon.classList.remove('bi-x-lg');
                    icon.classList.add('bi-list');
                }
            }
        });
    }
});

// ==================== FLASH MESSAGE AUTO-DISMISS ====================
document.addEventListener('DOMContentLoaded', () => {
    const flashMessages = document.querySelectorAll('.flash-message');
    
    flashMessages.forEach(message => {
        // Auto dismiss after 5 seconds
        setTimeout(() => {
            message.style.animation = 'slideOut 0.3s ease forwards';
            setTimeout(() => message.remove(), 300);
        }, 5000);

        // Manual close button
        const closeBtn = message.querySelector('.flash-message__close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                message.style.animation = 'slideOut 0.3s ease forwards';
                setTimeout(() => message.remove(), 300);
            });
        }
    });
});

// Add slideOut animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// ==================== UTILITY FUNCTIONS ====================

/**
 * Show loading state on button
 * @param {HTMLElement} button - Button element
 * @returns {string} Original button HTML
 */
function showLoading(button) {
    if (!button) return '';
    const originalHTML = button.innerHTML;
    button.setAttribute('data-original-html', originalHTML);
    button.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
    button.disabled = true;
    return originalHTML;
}

/**
 * Hide loading state on button
 * @param {HTMLElement} button - Button element
 */
function hideLoading(button) {
    if (!button) return;
    const originalHTML = button.getAttribute('data-original-html');
    if (originalHTML) {
        button.innerHTML = originalHTML;
        button.disabled = false;
        button.removeAttribute('data-original-html');
    }
}

/**
 * Show toast notification
 * @param {string} message - Message to display
 * @param {string} type - Type of toast (success, danger, warning, info)
 */
function showToast(message, type = 'info') {
    let toastContainer = document.querySelector('.toast-container');
    
    // Create toast container if it doesn't exist
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
        toastContainer.style.zIndex = '1200';
        toastContainer.style.marginTop = '80px';
        document.body.appendChild(toastContainer);
    }
    
    const icons = {
        success: 'check-circle-fill',
        danger: 'exclamation-triangle-fill',
        error: 'exclamation-triangle-fill',
        warning: 'exclamation-circle-fill',
        info: 'info-circle-fill'
    };
    
    const colors = {
        success: 'success',
        danger: 'danger',
        error: 'danger',
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
    
    // Remove toast element after hidden
    toastElement.addEventListener('hidden.bs.toast', () => toastElement.remove());
}

/**
 * Debounce function
 * @param {Function} func - Function to debounce
 * @param {number} wait - Wait time in milliseconds
 * @returns {Function} Debounced function
 */
function debounce(func, wait = 300) {
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

/**
 * Animated counter
 * @param {HTMLElement} element - Element to animate
 * @param {number} target - Target number
 * @param {number} duration - Animation duration in milliseconds
 */
function animateCounter(element, target, duration = 2000) {
    if (!element) return;
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

/**
 * Toggle password visibility
 * @param {string} inputId - ID of password input
 */
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

/**
 * Initialize search functionality
 * @param {string} inputId - ID of search input
 * @param {string} itemsSelector - Selector for items to filter
 */
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
            } else {
                item.style.display = 'none';
            }
        });
    }, 300);

    searchInput.addEventListener('input', (e) => {
        debouncedSearch(e.target.value);
    });
}

// ==================== AJAX FORM ACTIONS ====================
/**
 * Initialize AJAX actions for connection requests
 */
function initializeAjaxActions() {
    document.addEventListener('click', function(e) {
        // Cancel connection requests
        if (e.target.matches('.cancel-btn') || e.target.closest('.cancel-btn')) {
            e.preventDefault();
            const button = e.target.closest('.cancel-btn');
            const connId = button.dataset.connId;
            
            showLoading(button);
            
            // Get CSRF token
            const csrfToken = document.querySelector('input[name="csrf_token"]')?.value;
            
            fetch(`/connections/cancel/${connId}`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.ok) {
                    // Fade out and remove connection item
                    const item = button.closest('.connection-item');
                    if (item) {
                        item.style.transition = 'opacity 0.3s ease';
                        item.style.opacity = '0';
                        setTimeout(() => { 
                            item.remove(); 
                            updateOutgoingCount();
                        }, 300);
                    }
                    showToast(data.message || 'Request cancelled', 'success');
                } else {
                    showToast(data.message || 'Failed to cancel', 'danger');
                    hideLoading(button);
                }
            })
            .catch(() => {
                showToast('Network error occurred', 'danger');
                hideLoading(button);
            });
        }
    });
}

/**
 * Update connection counters
 */
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

// ==================== SMOOTH SCROLL FOR ANCHOR LINKS ====================
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#' && href !== '') {
                const target = document.querySelector(href);
                if (target) {
                    e.preventDefault();
                    const topbar = document.querySelector('.topbar') || document.querySelector('.guest-nav');
                    const navHeight = topbar ? topbar.offsetHeight : 0;
                    const targetPosition = target.offsetTop - navHeight - 20;
                    
                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    });
                }
            }
        });
    });
});

// ==================== IMAGE LAZY LOADING ====================
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

// ==================== SCROLL ANIMATIONS ====================
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

    refresh() {
        this.observeElements();
    }
}

const scrollAnimations = new ScrollAnimations();

// ==================== INITIALIZE ON DOM LOAD ====================
document.addEventListener('DOMContentLoaded', () => {
    // Initialize AJAX actions
    initializeAjaxActions();
    
    // Add fade-in class to body
    document.body.classList.add('fade-in');
    
    // Remove page loader if exists
    const loader = document.querySelector('.page-loader');
    if (loader) {
        loader.style.opacity = '0';
        setTimeout(() => loader.remove(), 300);
    }
    
    // Log initialization
    console.log('✨ C-Connect: Global JavaScript initialized successfully!');
});

// ==================== EXPORT GLOBAL API ====================
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