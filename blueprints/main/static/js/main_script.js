// ===== MAIN BLUEPRINT SPECIFIC JAVASCRIPT =====

// ===== SCROLL ANIMATIONS =====
document.addEventListener('DOMContentLoaded', () => {
    // Intersection Observer for scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);

    // Observe all elements with animate-on-scroll class
    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        observer.observe(el);
    });
});

// ===== SMOOTH ANCHOR SCROLLING =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href !== '#' && href.length > 1) {
            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
    });
});

// ===== FEATURE CARD HOVER EFFECTS =====
const featureCards = document.querySelectorAll('.feature-card');
featureCards.forEach(card => {
    card.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-8px)';
    });
    
    card.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0)';
    });
});

// ===== STAT COUNTER ANIMATION =====
function animateStatsOnScroll() {
    const statsSection = document.querySelector('.stats-section');
    if (!statsSection) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const statNumbers = document.querySelectorAll('.stat-number');
                statNumbers.forEach(stat => {
                    const target = parseInt(stat.getAttribute('data-target'));
                    if (target > 0) {
                        window.cconnect.animateCounter(stat, target, 2000);
                    }
                });
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.3 });

    observer.observe(statsSection);
}

// Call on page load
animateStatsOnScroll();

// ===== HERO SECTION PARALLAX EFFECT =====
const heroSection = document.querySelector('.hero-section');
if (heroSection) {
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const parallaxElements = heroSection.querySelectorAll('.hero-decoration');
        
        parallaxElements.forEach((el, index) => {
            const speed = (index + 1) * 0.5;
            el.style.transform = `translateY(${scrolled * speed}px)`;
        });
    });
}

// ===== CTA BUTTON RIPPLE EFFECT =====
function createRipple(event) {
    const button = event.currentTarget;
    const ripple = document.createElement('span');
    const diameter = Math.max(button.clientWidth, button.clientHeight);
    const radius = diameter / 2;

    ripple.style.width = ripple.style.height = `${diameter}px`;
    ripple.style.left = `${event.clientX - button.offsetLeft - radius}px`;
    ripple.style.top = `${event.clientY - button.offsetTop - radius}px`;
    ripple.classList.add('ripple');

    const existingRipple = button.querySelector('.ripple');
    if (existingRipple) {
        existingRipple.remove();
    }

    button.appendChild(ripple);
}

// Add ripple effect to primary buttons
document.querySelectorAll('.btn-primary-custom').forEach(button => {
    button.addEventListener('click', createRipple);
});

// ===== FORM ENHANCEMENTS =====

// Contact form character counter
const messageTextarea = document.getElementById('message');
if (messageTextarea) {
    const charCount = document.getElementById('charCount');
    
    messageTextarea.addEventListener('input', function() {
        const count = this.value.length;
        const maxLength = 500;
        
        if (charCount) {
            charCount.textContent = count;
            
            if (count > maxLength) {
                this.value = this.value.substring(0, maxLength);
                charCount.textContent = maxLength;
            }
            
            // Color indication
            if (count > maxLength * 0.9) {
                charCount.style.color = 'var(--danger, #ef4444)';
            } else if (count > maxLength * 0.7) {
                charCount.style.color = 'var(--warning, #f59e0b)';
            } else {
                charCount.style.color = 'var(--text-muted)';
            }
        }
    });
}

// ===== DISCOVER PAGE FUNCTIONALITY =====

// Search with debounce
const searchInput = document.getElementById('searchInput');
if (searchInput) {
    searchInput.addEventListener('input', window.cconnect.debounce(function() {
        const query = this.value.toLowerCase().trim();
        filterUsers(query);
    }, 300));
}

function filterUsers(query) {
    const userCards = document.querySelectorAll('.user-card');
    let visibleCount = 0;
    
    userCards.forEach(card => {
        const userName = card.querySelector('.user-name')?.textContent.toLowerCase() || '';
        const userEmail = card.querySelector('.user-email')?.textContent.toLowerCase() || '';
        
        if (userName.includes(query) || userEmail.includes(query)) {
            card.style.display = '';
            visibleCount++;
        } else {
            card.style.display = 'none';
        }
    });
    
    // Show/hide empty state
    const emptyState = document.getElementById('emptyState');
    if (emptyState) {
        emptyState.style.display = visibleCount === 0 ? 'block' : 'none';
    }
}

// Filter chips functionality
const filterChips = document.querySelectorAll('.filter-chip');
filterChips.forEach(chip => {
    chip.addEventListener('click', function() {
        // Remove active from all chips
        filterChips.forEach(c => c.classList.remove('active'));
        // Add active to clicked chip
        this.classList.add('active');
        
        const filter = this.getAttribute('data-filter');
        applyFilter(filter);
    });
});

function applyFilter(filterType) {
    // In a real app, this would make an API call
    console.log('Applying filter:', filterType);
    
    // Show toast notification
    const filterNames = {
        'all': 'Showing all users',
        'year': 'Showing users from your year',
        'department': 'Showing users from your department',
        'interests': 'Showing users with similar interests'
    };
    
    if (window.cconnect && window.cconnect.showToast) {
        window.cconnect.showToast(filterNames[filterType] || 'Filter applied', 'info');
    }
}

// Connect button handler
document.addEventListener('click', function(e) {
    const connectBtn = e.target.closest('.btn-connect');
    if (connectBtn) {
        e.preventDefault();
        const userCard = connectBtn.closest('.user-card');
        const userName = userCard.querySelector('.user-name')?.textContent || 'User';
        
        // Change button state
        connectBtn.innerHTML = '<i class="bi bi-check-circle"></i> Connected';
        connectBtn.disabled = true;
        connectBtn.style.opacity = '0.6';
        
        // Show success toast
        if (window.cconnect && window.cconnect.showToast) {
            window.cconnect.showToast(`Connected with ${userName}!`, 'success');
        }
    }
    
    // Message button handler
    const messageBtn = e.target.closest('.btn-message');
    if (messageBtn) {
        e.preventDefault();
        if (window.cconnect && window.cconnect.showToast) {
            window.cconnect.showToast('Messaging feature coming soon!', 'info');
        }
    }
});


// ========= Search page
document.addEventListener('DOMContentLoaded', () => {

    const input = document.getElementById("searchInput");
    const results = document.getElementById("resultsContainer");

    let timer = null;

    input.addEventListener("input", () => {
        clearTimeout(timer);
        timer = setTimeout(() => {
            const q = input.value.trim();
            if (q.length === 0) {
                results.innerHTML = "";
                return;
            }
            performSearch(q);
        }, 300);
    });

    function performSearch(q) {
        results.innerHTML = `<div class="loading">Searching...</div>`;

        fetch(`/api/search?q=${encodeURIComponent(q)}`)
            .then(r => r.json())
            .then(data => {

                results.innerHTML = "";

                if (!data.results || data.results.length === 0) {
                    results.innerHTML = `
                        <div class="empty-state glass-card p-5">
                            <div class="empty-icon"><i class="bi bi-search"></i></div>
                            <p>No matching users found.</p>
                        </div>`;
                    return;
                }

                data.results.forEach(item => {
                    const card = buildUserCard(item);
                    results.appendChild(card);
                });
            });
    }

    // CLONE OF THE DISCOVER CARD TEMPLATE
    function buildUserCard(u) {
        const div = document.createElement("div");
        div.className = "user-card glass-card";

        div.innerHTML = `
            <div class="user-avatar">
                ${u.profile_picture
                  ? `<img src="${u.avatar_url}" class="profile-img">`
                  : u.name[0].toUpperCase()
                }
            </div>

            <h3 class="user-name">${u.name}</h3>
            <p class="user-email">${u.department || ""}</p>

            <div class="user-actions" style="justify-content: center;">
                ${renderConnectionButton(u)}
            </div>
        `;

        return div;
    }

    // Connection logic
    function renderConnectionButton(u) {
        if (u.connection_status === "connected") {
            return `<button class="btn btn-connected btn-sm" disabled>
                        <i class="bi bi-check-circle"></i> Connected
                    </button>`;
        }
        if (u.connection_status === "pending") {
            return `<button class="btn btn-pending btn-sm" disabled>
                        <i class="bi bi-clock"></i> Pending
                    </button>`;
        }
        return `<button class="btn btn-primary-custom btn-sm action-connect"
                        data-user-id="${u.id}">
                    <i class="bi bi-person-plus"></i> Connect
                </button>`;
    }
});






// ===== LOAD MORE FUNCTIONALITY =====
const loadMoreBtn = document.getElementById('loadMoreBtn');
if (loadMoreBtn) {
    loadMoreBtn.addEventListener('click', function() {
        // In real app, this would load more users from API
        const originalText = window.cconnect.showLoading(this);
        
        setTimeout(() => {
            window.cconnect.hideLoading(this, originalText);
            window.cconnect.showToast('No more users to load', 'info');
        }, 1000);
    });
}

// ===== PAGE TRANSITION EFFECTS =====
window.addEventListener('beforeunload', function() {
    document.body.style.opacity = '0';
});

// ===== KEYBOARD SHORTCUTS =====
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + K for search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.focus();
        }
    }
    
    // Escape to clear search
    if (e.key === 'Escape') {
        const searchInput = document.getElementById('searchInput');
        if (searchInput && searchInput.value) {
            searchInput.value = '';
            searchInput.dispatchEvent(new Event('input'));
        }
    }
});

// ===== TOOLTIP INITIALIZATION =====
// Initialize Bootstrap tooltips if present
document.addEventListener('DOMContentLoaded', function() {
    const tooltipTriggerList = [].slice.call(
        document.querySelectorAll('[data-bs-toggle="tooltip"]')
    );
    
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
});

// ===== LAZY LOADING IMAGES =====
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                }
                imageObserver.unobserve(img);
            }
        });
    });

    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

// ===== CONSOLE EASTER EGG =====
console.log('%c🎓 C-Connect', 'font-size: 24px; font-weight: bold; color: #3b82f6;');
console.log('%cBuilding campus communities, one connection at a time.', 'font-size: 14px; color: #64748b;');
console.log('%c💡 Tip: Press Ctrl+K (or Cmd+K) to focus search', 'font-size: 12px; color: #94a3b8;');