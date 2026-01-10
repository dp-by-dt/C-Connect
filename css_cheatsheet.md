# 🎨 C-Connect Design System Cheatsheet

## 📋 Table of Contents
1. [CSS Variables (Theme Colors)](#css-variables)
2. [Layout Classes](#layout-classes)
3. [Card & Container Styles](#cards-containers)
4. [Button Styles](#buttons)
5. [Form Elements](#forms)
6. [Typography](#typography)
7. [Navigation](#navigation)
8. [Icons & Visual Elements](#icons)
9. [Animations](#animations)
10. [JavaScript Functions](#javascript)
11. [Page-Specific Classes](#page-specific)

---

## 🎨 CSS Variables (Theme Colors) {#css-variables}

### Usage: `var(--variable-name)`

### Colors
```css
--primary-color: #3b82f6;      /* Main blue - buttons, links, accents */
--primary-hover: #2563eb;      /* Darker blue - hover states */
--secondary-color: #6366f1;    /* Purple accent - gradients */
--accent-color: #06b6d4;       /* Cyan - secondary accents */
```

### Backgrounds
```css
--bg-primary: #ffffff;         /* Main background (light) / #0f172a (dark) */
--bg-secondary: #f8fafc;       /* Secondary bg (light) / #1e293b (dark) */
--bg-glass: rgba(255,255,255,0.7);  /* Glassmorphism background */
--bg-glass-hover: rgba(255,255,255,0.85);  /* Glass hover state */
```

### Text Colors
```css
--text-primary: #1e293b;       /* Main text (light) / #f1f5f9 (dark) */
--text-secondary: #64748b;     /* Secondary text */
--text-muted: #94a3b8;         /* Muted/disabled text */
```

### Borders & Shadows
```css
--border-color: rgba(148,163,184,0.2);  /* Standard borders */
--shadow-sm: 0 2px 8px rgba(0,0,0,0.05);   /* Small shadow */
--shadow-md: 0 4px 16px rgba(0,0,0,0.08);  /* Medium shadow */
--shadow-lg: 0 8px 32px rgba(0,0,0,0.12);  /* Large shadow */
--glass-border: rgba(255,255,255,0.3);     /* Glass card borders */
--glass-shadow: 0 8px 32px 0 rgba(31,38,135,0.15);  /* Glass shadows */
```

**Example:**
```html
<div style="background: var(--bg-glass); color: var(--text-primary);">
    Content
</div>
```

---

## 📐 Layout Classes {#layout-classes}

### Main Content Area
```html
<main class="main-content">
    <!-- Your page content -->
</main>
```
- **Effect:** Padding-top for navbar, min-height for full viewport
- **Used in:** Every page (set in base.html)

### Container Wrappers
```html
<!-- Standard container -->
<div class="container py-4">...</div>

<!-- Full-width container -->
<div class="container-fluid px-4">...</div>
```
- **py-4:** Padding Y-axis (top/bottom) - Bootstrap
- **px-4:** Padding X-axis (left/right) - Bootstrap

### Rows & Columns (Bootstrap Grid)
```html
<div class="row">
    <div class="col-lg-6 col-md-12">Left</div>
    <div class="col-lg-6 col-md-12">Right</div>
</div>
```
- **col-lg-6:** 50% width on large screens
- **col-md-12:** 100% width on medium screens
- **mb-3, mb-4, mb-5:** Margin-bottom spacing

---

## 🎴 Card & Container Styles {#cards-containers}

### Glass Card (Primary Component)
```html
<div class="glass-card">
    <!-- Content -->
</div>
```
- **Effect:** Glassmorphism with blur, transparency, border
- **Hover:** Lifts up (translateY -4px), increases shadow
- **Used in:** Dashboard, profile, all content cards

### Glass Card with Padding
```html
<div class="glass-card p-4">...</div>  <!-- Medium padding -->
<div class="glass-card p-5">...</div>  <!-- Large padding -->
```

### Auth-Specific Cards
```html
<div class="auth-container">
    <div class="auth-card glass-card">
        <div class="auth-header text-center mb-4">
            <div class="auth-icon mb-3">
                <i class="bi bi-person-lock"></i>
            </div>
            <h2 class="auth-title">Title</h2>
            <p class="auth-subtitle">Subtitle</p>
        </div>
        <!-- Form content -->
    </div>
</div>
```
- **auth-container:** Vertically centers content
- **auth-card:** Padding + fade-in animation
- **auth-icon:** 80x80 gradient circle with icon
- **Used in:** Login, Signup pages

### Dashboard Cards
```html
<div class="dashboard-card glass-card">
    <div class="card-header-custom">
        <h5 class="card-title-custom">
            <i class="bi bi-icon me-2"></i>Title
        </h5>
    </div>
    <!-- Card content -->
</div>
```
- **dashboard-card:** Padding + margin
- **card-header-custom:** Flex layout, bottom border
- **Used in:** Dashboard sections

### Stat Cards
```html
<div class="stat-card glass-card text-center">
    <div class="stat-icon"><i class="bi bi-people-fill"></i></div>
    <div class="stat-value">123</div>
    <div class="stat-label">Label</div>
</div>
```
- **stat-icon:** Gradient text icon (2.5rem)
- **stat-value:** Large bold number (2rem)
- **stat-label:** Small secondary text
- **Hover:** Lifts up -8px
- **Used in:** Dashboard stats

---

## 🔘 Button Styles {#buttons}

### Primary Button
```html
<button class="btn btn-primary-custom">
    <i class="bi bi-icon me-2"></i>Text
</button>
```
- **Effect:** Blue gradient, white text, shadow
- **Hover:** Lifts up, increases brightness
- **Sizes:** Add `btn-sm`, `btn-lg`

### Outline Button
```html
<button class="btn btn-outline-custom">Text</button>
```
- **Effect:** Transparent bg, blue border
- **Hover:** Fills with blue, white text

### Theme Toggle Button
```html
<button class="btn btn-theme-toggle" id="themeToggle">
    <i class="bi bi-sun-fill" id="themeIcon"></i>
</button>
```
- **Effect:** Circular (40x40), glass background
- **Hover:** Rotates 180°
- **Used in:** Navbar (auto-handled by JS)

### Quick Action Buttons
```html
<a href="#" class="quick-action-item">
    <div class="quick-action-icon">
        <i class="bi bi-compass"></i>
    </div>
    <div class="quick-action-label">Label</div>
</a>
```
- **quick-action-icon:** 60x60 gradient circle
- **quick-action-label:** Small text below
- **Hover:** Lifts up -4px
- **Used in:** Dashboard quick actions

### Loading State (via JS)
```javascript
const originalText = window.cconnect.showLoading(button);
// Do async work
window.cconnect.hideLoading(button, originalText);
```

---

## 📝 Form Elements {#forms}

### Form Container
```html
<form method="POST" class="needs-validation" novalidate>
    <!-- Form fields -->
</form>
```
- **needs-validation:** Bootstrap validation class
- **novalidate:** Disables browser validation (uses Bootstrap)

### Input Field
```html
<div class="mb-3">
    <label for="email" class="form-label">
        <i class="bi bi-envelope me-1"></i>Email
    </label>
    <input 
        type="email" 
        class="form-control" 
        id="email" 
        name="email" 
        placeholder="you@example.com"
        required
    >
    <div class="form-text">Helper text</div>
    <div class="invalid-feedback">Error message</div>
</div>
```
- **form-control:** Glass background, border, focus effect
- **form-label:** Semi-bold, secondary color
- **form-text:** Small helper text below input
- **invalid-feedback:** Shows on validation error

### Password Field with Toggle
```html
<div class="password-input-wrapper">
    <input 
        type="password" 
        class="form-control" 
        id="password" 
        name="password"
    >
    <button 
        type="button" 
        class="password-toggle" 
        onclick="togglePassword('password')"
        tabindex="-1"
    >
        <i class="bi bi-eye" id="password-icon"></i>
    </button>
</div>
```
- **password-input-wrapper:** Relative positioning
- **password-toggle:** Absolute positioned button
- **togglePassword():** JS function (see JS section)

### Password Strength Indicator
```html
<div class="password-strength" id="passwordStrength"></div>
```
- **Classes:** Add `.weak`, `.medium`, or `.strong` via JS
- **Effect:** Progress bar that changes color
- **Used in:** Signup page

### Checkbox
```html
<div class="form-check">
    <input type="checkbox" class="form-check-input" id="remember">
    <label class="form-check-label" for="remember">
        Remember me
    </label>
</div>
```

### Select Dropdown
```html
<select class="form-select" id="subject" name="subject" required>
    <option value="">Choose...</option>
    <option value="option1">Option 1</option>
</select>
```

---

## ✍️ Typography {#typography}

### Headings
```html
<h1 class="page-title">Main Page Title</h1>
<p class="page-subtitle">Subtitle below title</p>

<h2 class="section-title">Section Title</h2>
<p class="section-subtitle">Section subtitle</p>
```
- **page-title:** 3rem, extra bold
- **page-subtitle:** 1.25rem, secondary color
- **section-title:** 2rem, bold
- **section-subtitle:** 1.125rem, secondary

### Text Gradient
```html
<span class="text-gradient">Gradient Text</span>
```
- **Effect:** Blue-to-cyan gradient
- **Used in:** Hero titles, highlights

### Links
```html
<a href="#" class="auth-link">Link Text</a>
```
- **auth-link:** Primary color, underline on hover
- **Used in:** Auth pages

```html
<a href="#" class="footer-link">Footer Link</a>
```
- **footer-link:** Secondary color, small size

### Text Colors (Bootstrap)
```html
<p class="text-muted">Muted text</p>
<p class="text-primary">Primary color</p>
<p class="text-secondary">Secondary color</p>
```

---

## 🧭 Navigation {#navigation}

### Navbar Structure
```html
<nav class="navbar navbar-expand-lg navbar-glass fixed-top">
    <div class="container-fluid px-4">
        <a class="navbar-brand brand-logo" href="/">
            <span class="brand-c">C</span>
            <span class="brand-connect">-Connect</span>
        </a>
        <!-- Rest of navbar -->
    </div>
</nav>
```
- **navbar-glass:** Glassmorphism effect
- **fixed-top:** Stays at top on scroll
- **brand-c:** Large blue "C"
- **brand-connect:** Gradient "-Connect"

### Nav Links
```html
<li class="nav-item">
    <a class="nav-link" href="#">
        <i class="bi bi-icon"></i> Text
    </a>
</li>
```
- **Effect:** Secondary color, rounded bg on hover

### Dropdown Menu
```html
<li class="nav-item dropdown">
    <a class="nav-link dropdown-toggle" href="#" data-bs-toggle="dropdown">
        Menu
    </a>
    <ul class="dropdown-menu dropdown-menu-end glass-dropdown">
        <li><a class="dropdown-item" href="#">Item</a></li>
        <li><hr class="dropdown-divider"></li>
        <li><a class="dropdown-item" href="#">Item 2</a></li>
    </ul>
</li>
```
- **glass-dropdown:** Glassmorphism dropdown
- **dropdown-menu-end:** Align to right

---

## 🎯 Icons & Visual Elements {#icons}

### Bootstrap Icons (Always Available)
```html
<i class="bi bi-icon-name"></i>
```

### Common Icons Used:
```
bi-speedometer2         Dashboard
bi-compass             Discover
bi-chat-dots           Messages
bi-person-circle       Profile
bi-gear                Settings
bi-box-arrow-right     Logout
bi-person-plus         Signup/Add user
bi-envelope            Email
bi-key                 Password
bi-eye / bi-eye-slash  Show/hide password
bi-check-circle        Success
bi-exclamation-triangle Error
bi-info-circle         Info
bi-people-fill         Users/connections
bi-calendar-event-fill Events
bi-collection-fill     Groups
bi-heart-fill          Favorite
bi-shield-check        Security
bi-stars               Featured
bi-lightning-charge    Quick actions
```

### Avatar Placeholder
```html
<div class="avatar-placeholder">
    {{ username[0].upper() }}
</div>
```
- **Effect:** Circular gradient background with initial
- **Size:** Set via width/height (usually 100px-120px)
- **Used in:** Profile, dashboard

### Hero Icons (Large gradient)
```html
<i class="bi bi-icon hero-icon"></i>
```
- **Effect:** 3rem, gradient text
- **Used in:** Home page hero section

### Stat Icons
```html
<div class="stat-icon">
    <i class="bi bi-icon"></i>
</div>
```
- **Effect:** 2.5rem, gradient text
- **Used in:** Dashboard stat cards

---

## ✨ Animations {#animations}

### Scroll Animation
```html
<div class="animate-on-scroll">
    <!-- Content fades in when scrolled into view -->
</div>
```
- **Effect:** Opacity 0→1, translateY 20→0
- **Auto-triggers:** Via Intersection Observer
- **Used in:** All page sections

### Animation Delays
```html
<div class="hero-card" style="animation-delay: 0.2s;">...</div>
<div class="hero-card" style="animation-delay: 0.4s;">...</div>
```
- **Effect:** Stagger animations for multiple elements

### Keyframe Animations (Auto-applied)
```css
@keyframes fadeInUp      /* Auth cards */
@keyframes floatIn       /* Hero cards */
@keyframes float         /* Decorative elements */
@keyframes slideInRight  /* Flash messages */
```

### Hover Effects (Built-in)
- **glass-card:** Hover lifts up
- **stat-card:** Hover lifts up -8px
- **buttons:** Hover lifts up, brightens
- **nav-links:** Hover changes color, bg

---

## 🎭 Flash Messages & Alerts {#alerts}

### Flash Messages (Auto-positioned)
```python
# In Flask route
flash('Message text', 'success')  # or 'danger', 'info', 'warning'
```

```html
<!-- Already in base.html, auto-displays -->
```
- **Categories:** success, danger, info, warning
- **Position:** Fixed top-right
- **Auto-dismiss:** After 5 seconds
- **Animation:** Slides in from right

### Custom Toast (via JS)
```javascript
window.cconnect.showToast('Message', 'success');
// Types: success, danger, info, warning, error
```

### Alert Boxes (Manual)
```html
<div class="alert alert-success glass-alert" role="alert">
    <i class="bi bi-check-circle me-2"></i>
    Success message!
</div>
```

---

## 🎮 JavaScript Functions {#javascript}

### Theme Management
```javascript
// Toggle theme
window.cconnect.themeManager.toggleTheme();

// Set specific theme
window.cconnect.themeManager.setTheme('dark');  // or 'light'

// Get current theme
const theme = window.cconnect.themeManager.getTheme();

// Set custom accent color
window.cconnect.themeManager.setAccentColor('#ff0000');
```

### Button Loading States
```javascript
const btn = document.getElementById('myBtn');
const originalText = window.cconnect.showLoading(btn);
// Do async work
window.cconnect.hideLoading(btn, originalText);
```

### Toast Notifications
```javascript
window.cconnect.showToast('Message text', 'success');
// Types: success, danger, info, warning, error
```

### Debounce (for search/filter)
```javascript
const debouncedSearch = window.cconnect.debounce((query) => {
    // Search logic
}, 300);

searchInput.addEventListener('input', (e) => {
    debouncedSearch(e.target.value);
});
```

### Animated Counter
```javascript
const element = document.getElementById('counter');
window.cconnect.animateCounter(element, 100, 2000);
// Animates from 0 to 100 over 2 seconds
```

### Password Toggle (Defined in templates)
```javascript
function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    const icon = document.getElementById(`${inputId}-icon`);
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
```

---

## 📄 Page-Specific Classes {#page-specific}

### Home Page
```html
<!-- Hero Section -->
<section class="hero-section">
    <div class="hero-content">
        <h1 class="hero-title">...</h1>
        <p class="hero-subtitle">...</p>
        <div class="hero-buttons">
            <a class="btn btn-primary-custom btn-lg">...</a>
        </div>
    </div>
    <div class="hero-visual">
        <div class="hero-card glass-card">
            <div class="hero-card-inner">
                <i class="bi bi-icon hero-icon"></i>
                <h3>Title</h3>
                <p>Description</p>
            </div>
        </div>
    </div>
    <div class="hero-decoration hero-decoration-1"></div>
    <div class="hero-decoration hero-decoration-2"></div>
</section>
```

### Dashboard
```html
<div class="dashboard-container">
    <div class="welcome-banner glass-card">
        <h1 class="welcome-title">...</h1>
        <p class="welcome-subtitle">...</p>
    </div>
    
    <div class="stat-card glass-card">...</div>
    
    <div class="dashboard-card glass-card">
        <div class="card-header-custom">
            <h5 class="card-title-custom">...</h5>
        </div>
        <!-- Content -->
    </div>
    
    <div class="quick-actions-grid">
        <a class="quick-action-item">...</a>
    </div>
</div>
```

### Discover Page
```html
<div class="glass-card text-center p-4">
    <div style="position: relative;">
        <i class="bi bi-search" style="position: absolute; left: 1rem; top: 50%; transform: translateY(-50%);"></i>
        <input type="text" class="form-control" style="padding-left: 3rem;" placeholder="Search...">
    </div>
</div>

<!-- User grid -->
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1.5rem;">
    <div class="glass-card p-4 text-center">
        <div class="avatar-placeholder" style="width: 100px; height: 100px; margin: 0 auto;">U</div>
        <h3>Username</h3>
        <p class="text-muted">email@example.com</p>
        <button class="btn btn-primary-custom btn-sm">Connect</button>
    </div>
</div>
```

### Settings Page
```html
<div class="glass-card p-4">
    <h2><i class="bi bi-gear me-2"></i>Settings</h2>
    <div class="mb-4">
        <h5>Appearance</h5>
        <div class="form-check form-switch">
            <input class="form-check-input" type="checkbox" id="darkModeToggle">
            <label class="form-check-label" for="darkModeToggle">Dark Mode</label>
        </div>
    </div>
</div>

<script>
document.getElementById('darkModeToggle').addEventListener('change', function() {
    window.cconnect.themeManager.toggleTheme();
});
document.getElementById('darkModeToggle').checked = 
    window.cconnect.themeManager.getTheme() === 'dark';
</script>
```

### Empty States
```html
<div class="empty-state text-center py-4">
    <i class="bi bi-icon" style="font-size: 3rem; color: var(--text-muted);"></i>
    <p class="text-muted mt-3">No items found</p>
    <p class="text-muted small">Additional info</p>
    <a href="#" class="btn btn-primary-custom btn-sm mt-2">Action</a>
</div>
```

---

## 🎯 Quick Reference: Common Patterns

### Standard Page Layout
```html
{% extends "base.html" %}
{% block title %}Page Title{% endblock %}

{% block extra_css %}
<style>
/* Page-specific styles */
</style>
{% endblock %}

{% block body %}
<div class="container py-4">
    <div class="glass-card p-4 animate-on-scroll">
        <h1 class="page-title">Title</h1>
        <p class="page-subtitle">Subtitle</p>
        <!-- Content -->
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
// Page-specific JS
</script>
{% endblock %}
```

### Grid Layout
```html
<div class="row g-4">
    <div class="col-lg-4 col-md-6 animate-on-scroll">
        <div class="glass-card p-4">Card 1</div>
    </div>
    <div class="col-lg-4 col-md-6 animate-on-scroll">
        <div class="glass-card p-4">Card 2</div>
    </div>
    <div class="col-lg-4 col-md-6 animate-on-scroll">
        <div class="glass-card p-4">Card 3</div>
    </div>
</div>
```

### Two-Column Layout
```html
<div class="row">
    <div class="col-lg-4 mb-4">
        <!-- Sidebar -->
        <div class="glass-card p-4">Sidebar</div>
    </div>
    <div class="col-lg-8">
        <!-- Main content -->
        <div class="glass-card p-4 mb-4">Content 1</div>
        <div class="glass-card p-4">Content 2</div>
    </div>
</div>
```

### Icon + Text Pattern
```html
<i class="bi bi-icon me-2"></i>Text
<!-- me-2 = margin-end (right) 2 units -->
```

### Responsive Show/Hide
```html
<div class="d-none d-md-block">Shows on medium+ screens</div>
<div class="d-block d-md-none">Shows on small screens only</div>
```

---

## 🔥 Pro Tips

1. **Always use `glass-card`** for containers
2. **Add `animate-on-scroll`** to sections for entrance animations
3. **Use `var(--color-name)`** for colors (theme compatibility)
4. **Bootstrap spacing:** `m/p + t/b/l/r/x/y + 0-5` (e.g., `mt-3`, `px-4`, `mb-5`)
5. **Test both themes** when adding new styles
6. **Use `text-center`** with glass cards for clean layouts
7. **Icon + text:** Always add `me-2` or `ms-2` for spacing
8. **Loading states:** Use `window.cconnect.showLoading()` for all async actions
9. **Validation:** Add `needs-validation` and `novalidate` to all forms
10. **Gradients:** Use on icons, buttons, avatars for brand consistency

---

**Last Updated:** Compatible with current C-Connect implementation
**Bootstrap Version:** 5.3.2
**Icons:** Bootstrap Icons 1.11.1













--------------------- After UI-Upgrade-v4 
----------- The old color theme variables from global.css file -----------

/* ==================== CSS VARIABLES (original below) ==================== */
/* :root {
    /* ===== Brand Colors - Rich Deep Green Theme ===== */
    --primary-color: #1a4d2e;           /* Rich deep forest green */
    --primary-hover: #27613d;           /* Slightly lighter */
    --primary-light: #2f7a4a;           /* Bright forest */
    --accent-color: #8fb996;            /* Muted sage accent */
    --accent-bright: #b8e986;           /* Fresh lime CTA */
    
    /* ===== Backgrounds (Light Mode) ===== */
    --bg-primary: #fefffe;
    --bg-secondary: #f5faf7;
    --bg-tertiary: #ebf5ef;
    --bg-hover: #e0f0e6;
    --bg-gradient-start: #f5faf7;
    --bg-gradient-end: #ebf5ef;
    
    /* ===== Glass Effect ===== */
    --glass-bg: rgba(255, 255, 255, 0.75);
    --glass-border: rgba(26, 77, 46, 0.12);
    --glass-shadow: rgba(26, 77, 46, 0.1);
    
    /* ===== Text Colors ===== */
    --text-primary: #0d1f16;
    --text-secondary: #1a4d2e;
    --text-tertiary: #2f7a4a;
    --text-muted: #7a9e88;
    
    
    /* ===== Semantic Colors ===== */
    --success-color: #3d6b1f;
    --danger-color: #c63d3d;
    --warning-color: #d89a2c;
    --info-color: #3d6b8f;
    
    /* ===== Borders & Shadows ===== */
    --border-color: rgba(45, 80, 22, 0.12);
    --border-subtle: rgba(45, 80, 22, 0.06);
    
    --radius-sm: 10px;
    --radius-md: 16px;
    --radius-lg: 20px;
    --radius-xl: 28px;
    --radius-full: 50%;
    
    --shadow-xs: 0 2px 8px var(--glass-shadow);
    --shadow-sm: 0 4px 16px var(--glass-shadow);
    --shadow-md: 0 8px 24px var(--glass-shadow);
    --shadow-lg: 0 12px 40px rgba(45, 80, 22, 0.15);
    
    /* ===== Transitions ===== */
    --transition-fast: 200ms cubic-bezier(0.4, 0, 0.2, 1);
    --transition-base: 300ms cubic-bezier(0.4, 0, 0.2, 1);
    --transition-smooth: 400ms cubic-bezier(0.4, 0, 0.2, 1);
    
    /* ===== Layout Dimensions ===== */
    --sidebar-width: 260px;
    --sidebar-collapsed: 80px;
    --topbar-height: 72px;
    --bottom-nav-height: 68px;
}

/* ===== Dark Theme ===== */
.theme-dark {
    --primary-color: #8fb996;
    --primary-hover: #a8c9ae;
    --primary-light: #c1dac5;
    --accent-color: #2f7a4a;
    --accent-bright: #b8e986;
    
    --bg-primary: #0a1410;
    --bg-secondary: #0f1a15;
    --bg-tertiary: #14211a;
    --bg-hover: #1a2820;
    --bg-gradient-start: #0a1410;
    --bg-gradient-end: #14211a;
    
    --glass-bg: rgba(15, 26, 21, 0.85);
    --glass-border: rgba(143, 185, 150, 0.18);
    --glass-shadow: rgba(0, 0, 0, 0.5);
    
    --text-primary: #e8f4ec;
    --text-secondary: #c5dccb;
    --text-tertiary: #8fb996;
    --text-muted: #5a7864;
    

    
    --border-color: rgba(168, 208, 141, 0.15);
    --border-subtle: rgba(168, 208, 141, 0.08);
    
    --shadow-xs: 0 2px 8px rgba(0, 0, 0, 0.3);
    --shadow-sm: 0 4px 16px rgba(0, 0, 0, 0.4);
    --shadow-md: 0 8px 24px rgba(0, 0, 0, 0.5);
    --shadow-lg: 0 12px 40px rgba(0, 0, 0, 0.6);
} */
