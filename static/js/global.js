/* =====================================================
   C-CONNECT GLOBAL JAVASCRIPT v3.0
   Smooth Interactions & Enhanced UX
   ===================================================== */

// ==================== THEME MANAGEMENT ====================
class ThemeManager {
    constructor() {
        this.themeKey = 'cconnect-theme';
        this.init();
    }

    init() {
        const savedTheme = localStorage.getItem(this.themeKey) || 'light';
        this.setTheme(savedTheme, false);

        const themeToggle = document.getElementById('themeToggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => this.toggleTheme());
        }
    }

    setTheme(theme, save = true) {
        if (theme === 'dark') {
            document.documentElement.classList.add('theme-dark');
        } else {
            document.documentElement.classList.remove('theme-dark');
        }
        
        const icon = document.getElementById('themeIcon');
        if (icon) {
            icon.className = theme === 'dark' ? 'bi bi-moon-stars-fill' : 'bi bi-sun-fill';
        }

        if (save) {
            localStorage.setItem(this.themeKey, theme);
        }

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

const themeManager = new ThemeManager();

// ==================== SIDEBAR TOGGLE (DESKTOP) ====================
document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');

    if (sidebar && sidebarToggle) {
        const savedState = localStorage.getItem('sidebar-expanded');
        if (savedState === 'true') {
            sidebar.classList.add('is-expanded');
        }

        sidebarToggle.addEventListener('click', () => {
            sidebar.classList.toggle('is-expanded');
            const isExpanded = sidebar.classList.contains('is-expanded');
            localStorage.setItem('sidebar-expanded', isExpanded);
            
            // Smooth animation for toggle button
            sidebarToggle.style.transform = isExpanded ? 'translateY(-50%) rotate(5deg)' : 'translateY(-50%) rotate(-5deg)';
            setTimeout(() => {
                sidebarToggle.style.transform = 'translateY(-50%)';
            }, 200);
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
        mobileMenuToggle.addEventListener('click', () => {
            mobileMenu.classList.add('is-open');
            document.body.style.overflow = 'hidden';
        });

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

        const mobileLinks = mobileMenu.querySelectorAll('.mobile-menu__link');
        mobileLinks.forEach(link => {
            link.addEventListener('click', closeMobileMenu);
        });

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
        profileBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            profileDropdown.classList.toggle('is-open');
        });

        document.addEventListener('click', (e) => {
            if (!profileDropdown.contains(e.target)) {
                profileDropdown.classList.remove('is-open');
            }
        });

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
        setTimeout(() => {
            message.style.animation = 'slideOut 0.4s cubic-bezier(0.4, 0, 0.2, 1) forwards';
            setTimeout(() => message.remove(), 400);
        }, 5000);

        const closeBtn = message.querySelector('.flash-message__close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                message.style.animation = 'slideOut 0.4s cubic-bezier(0.4, 0, 0.2, 1) forwards';
                setTimeout(() => message.remove(), 400);
            });
        }
    });
});

// Flash message slideOut animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        to {
            transform: translateX(120%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// ==================== ACTIVE NAVIGATION HIGHLIGHTING ====================
document.addEventListener('DOMContentLoaded', () => {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.sidebar__link, .mobile-menu__link, .bottom-nav__item');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href && currentPath.includes(href) && href !== '/') {
            link.classList.add('active');
        }
    });
});

// Add active state styling
const activeStyle = document.createElement('style');
activeStyle.textContent = `
    .sidebar__link.active,
    .mobile-menu__link.active {
        background: var(--bg-hover);
        color: var(--primary-color);
        font-weight: 600;
    }
    
    .sidebar__link.active::before {
        transform: translateX(0);
    }
    
    .bottom-nav__item.active {
        color: var(--primary-color);
    }
`;
document.head.appendChild(activeStyle);

// ==================== UTILITY FUNCTIONS ====================

/**
 * Show loading state on button
 */
function showLoading(button) {
    if (!button) return '';
    const originalHTML = button.innerHTML;
    button.setAttribute('data-original-html', originalHTML);
    button.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
    button.disabled = true;
    button.style.cursor = 'not-allowed';
    return originalHTML;
}

/**
 * Hide loading state on button
 */
function hideLoading(button) {
    if (!button) return;
    const originalHTML = button.getAttribute('data-original-html');
    if (originalHTML) {
        button.innerHTML = originalHTML;
        button.disabled = false;
        button.style.cursor = 'pointer';
        button.removeAttribute('data-original-html');
    }
}

/**
 * Show toast notification
 */
function showToast(message, type = 'info') {
    let toastContainer = document.querySelector('.toast-container');
    
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
        toastContainer.style.zIndex = '1200';
        toastContainer.style.marginTop = '88px';
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
        <div class="toast align-items-center text-bg-${colors[type]} border-0 glass-effect" role="alert">
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

/**
 * Debounce function
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
                item.style.animation = 'fadeIn 0.3s ease';
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
function initializeAjaxActions() {
    document.addEventListener('click', function(e) {
        if (e.target.matches('.cancel-btn') || e.target.closest('.cancel-btn')) {
            e.preventDefault();
            const button = e.target.closest('.cancel-btn');
            const connId = button.dataset.connId;
            
            showLoading(button);
            
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
                    const item = button.closest('.connection-item');
                    if (item) {
                        item.style.transition = 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)';
                        item.style.transform = 'translateX(100%)';
                        item.style.opacity = '0';
                        setTimeout(() => { 
                            item.remove(); 
                            updateOutgoingCount();
                        }, 400);
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
        
        if (newCount === 0) {
            badge.style.display = 'none';
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
                img.style.animation = 'fadeIn 0.5s ease';
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

document.addEventListener('DOMContentLoaded', lazyLoadImages);

// ==================== BUTTON RIPPLE EFFECT ====================
document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('.btn, .topbar__icon-btn, .sidebar__link');
    
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple-effect');
            
            this.appendChild(ripple);
            
            setTimeout(() => ripple.remove(), 600);
        });
    });
});

// Ripple effect styles
const rippleStyle = document.createElement('style');
rippleStyle.textContent = `
    .ripple-effect {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.5);
        transform: scale(0);
        animation: ripple-animation 0.6s ease-out;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(2);
            opacity: 0;
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
`;
document.head.appendChild(rippleStyle);

// ==================== ENHANCE FORM INTERACTIONS ====================
document.addEventListener('DOMContentLoaded', () => {
    const formControls = document.querySelectorAll('.form-control');
    
    formControls.forEach(input => {
        // Float label effect
        input.addEventListener('focus', () => {
            input.parentElement?.classList.add('focused');
        });
        
        input.addEventListener('blur', () => {
            if (!input.value) {
                input.parentElement?.classList.remove('focused');
            }
        });
        
        // Character counter for textareas
        if (input.tagName === 'TEXTAREA' && input.hasAttribute('maxlength')) {
            const maxLength = input.getAttribute('maxlength');
            const counter = document.createElement('small');
            counter.className = 'character-counter text-muted';
            counter.textContent = `0 / ${maxLength}`;
            input.parentElement?.appendChild(counter);
            
            input.addEventListener('input', () => {
                counter.textContent = `${input.value.length} / ${maxLength}`;
                if (input.value.length > maxLength * 0.9) {
                    counter.style.color = 'var(--danger-color)';
                } else {
                    counter.style.color = 'var(--text-muted)';
                }
            });
        }
    });
});

// ==================== INITIALIZE ON DOM LOAD ====================
document.addEventListener('DOMContentLoaded', () => {
    initializeAjaxActions();
    
    document.body.classList.add('fade-in');
    
    const loader = document.querySelector('.page-loader');
    if (loader) {
        loader.style.opacity = '0';
        setTimeout(() => loader.remove(), 300);
    }
    
    console.log('✨ C-Connect v3.0: Enhanced UI initialized successfully!');
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
    initializeAjaxActions,
    updateOutgoingCount,
    lazyLoadImages
};