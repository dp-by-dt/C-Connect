# Login Page - Update Documentation

## 📋 Overview
Modern, split-screen login page with form on left and hero image on right. Fully responsive with smooth animations.

---

## 🎨 Design Features

### Layout:
- **Desktop**: Split 50/50 - Form (left) | Image (right)
- **Tablet**: Full-width form, image hidden
- **Mobile**: Full-width form with decorative blur elements

### Visual Elements:
1. **Left Side (Form)**:
   - Clean, centered form container (max-width: 440px)
   - Floating blur decorations in background
   - Smooth fade-in animation on load
   - Minimal, spacious layout

2. **Right Side (Image)**:
   - Full-height hero image
   - Gradient overlay with text
   - Smooth gradient background fallback
   - More floating decorations

---

## 📁 File Structure

### HTML Structure:
```html
<div class="auth-page">
  <div class="auth-page__form-section">
    <!-- Decorations -->
    <div class="auth-page__form-container">
      <!-- Form header -->
      <!-- Form fields -->
      <!-- Social login -->
    </div>
  </div>
  
  <div class="auth-page__image-section">
    <img src="bg-placeholder.jpg">
    <!-- Overlay text -->
  </div>
</div>
```

### CSS Classes (BEM):
- `.auth-page` - Main container
- `.auth-page__form-section` - Left side
- `.auth-page__image-section` - Right side
- `.auth-page__decoration--1/2` - Floating blur circles
- `.auth-form__*` - All form elements
  - `__header` - Title section
  - `__group` - Form field wrapper
  - `__input` - Input fields
  - `__submit` - Submit button
  - `__footer` - Sign up link
  - `__social` - Social buttons

---

## 🔧 Features

### Form Fields:
1. **Email Input**
   - Validation included
   - Error state styling
   - Placeholder text

2. **Password Input**
   - Toggle visibility button (eye icon)
   - Error state styling
   - Uses global `togglePassword()` function

3. **Remember Me Checkbox**
   - Custom styled checkbox
   - Matches design system

4. **Forgot Password Link**
   - Styled link (placeholder href)

### Actions:
1. **Sign In Button**
   - Gradient background
   - Loading state on submit
   - Uses global `showLoading()` function

2. **Sign Up Link**
   - Redirects to signup page
   - `{{ url_for('auth.signup') }}`

3. **Social Login** (Coming Soon)
   - Google, Microsoft, GitHub icons
   - Disabled state
   - Tooltip: "Coming soon"

---

## 🎯 Backend Integration

### Form Variables Preserved:
- ✅ `{{ form.hidden_tag() }}` - CSRF token
- ✅ `{{ form.email }}` - Email field
- ✅ `{{ form.password }}` - Password field
- ✅ `{{ form.email.errors }}` - Email validation errors
- ✅ `{{ form.password.errors }}` - Password errors
- ✅ `{{ url_for('auth.login') }}` - Form action
- ✅ `{{ url_for('auth.signup') }}` - Sign up link

### Form Attributes:
```html
<form method="POST" 
      action="{{ url_for('auth.login') }}" 
      class="needs-validation" 
      novalidate>
```

---

## 🎨 Styling Details

### Colors:
- Uses global CSS variables from `global.css`
- `--primary-color`: Sage green
- `--accent-color`: Complementary green
- `--text-primary/secondary/muted`: Text hierarchy

### Decorative Blur Circles:
```css
.auth-page__decoration {
    width: 400px/300px;
    height: 400px/300px;
    border-radius: 50%;
    filter: blur(80px);
    opacity: 0.15;
    animation: float 8s/10s;
}
```

### Animations:
1. **fadeInUp** (form entry):
   - Duration: 0.6s
   - From: opacity 0, translateY(20px)
   - To: opacity 1, translateY(0)

2. **float** (decorations):
   - Duration: 8s/10s infinite
   - Subtle movement and scale

---

## 📱 Responsive Behavior

### Desktop (> 1024px):
- Split screen layout
- Form: 50% width (max 440px container)
- Image: 50% width (full height)
- Decorations visible on both sides

### Tablet (768px - 1024px):
- Image section hidden
- Form takes full width
- Centered form container
- Decorations visible behind form

### Mobile (< 768px):
- Full-width form
- Padding adjusted (1.5rem → 1rem)
- Font sizes reduced
- Options stack vertically
- Bottom navigation shows (from base.html)

### Small Mobile (< 480px):
- Further reduced font sizes
- Tighter padding on buttons
- Optimized for one-handed use

---

## 🖼️ Image Section

### Current Setup:
```html
<img src="{{ url_for('static', filename='images/bg-placeholder.jpg') }}">
```

### Overlay Text:
- Gradient overlay: `rgba(0, 0, 0, 0.2)`
- Hero headline: "Connect with Your Campus"
- Subtitle with description
- Centered, readable text with text-shadow

### Customization:
You can change:
1. Image source
2. Overlay opacity
3. Text content
4. Text positioning

---

## ⚡ JavaScript Functionality

### 1. Form Submission:
```javascript
loginForm.addEventListener('submit', function(e) {
    if (this.checkValidity()) {
        window.cconnect.showLoading(loginBtn);
    }
});
```

### 2. Password Toggle:
- Uses global function: `window.cconnect.togglePassword('password')`
- Toggles between `bi-eye` and `bi-eye-slash` icons
- Changes input type between `password` and `text`

---

## 🎯 Improvements Over Old Design

| Old | New |
|-----|-----|
| Centered card with decorations | Split-screen with hero image |
| Small form container | Spacious, modern layout |
| Auth logo icon | Clean typography focus |
| Floating label inputs | Standard label + input |
| Purple/blue gradient | Sage green theme |
| Generic background | Campus imagery |

---

## 🔄 Migration Notes

### Changes Required:
1. ✅ Replace `login.html` file
2. ✅ Add placeholder image: `static/images/bg-placeholder.jpg`
3. ✅ Test form submission
4. ✅ Test validation errors
5. ✅ Test responsive behavior

### No Backend Changes:
- All Flask form variables preserved
- Same route: `/auth/login`
- Same validation logic
- Same error handling

---

## 🐛 Testing Checklist

- [ ] Form loads correctly
- [ ] Email validation works
- [ ] Password validation works
- [ ] Password toggle works
- [ ] Remember me checkbox works
- [ ] Form submission shows loading state
- [ ] Errors display correctly
- [ ] Sign up link redirects
- [ ] Image loads correctly
- [ ] Responsive on tablet
- [ ] Responsive on mobile
- [ ] Dark mode compatible
- [ ] Social buttons disabled

---

## 🎨 Customization Guide

### Change Hero Image:
```html
<img src="{{ url_for('static', filename='images/YOUR_IMAGE.jpg') }}">
```

### Change Overlay Text:
Edit the overlay div content inside `.auth-page__image-section`

### Adjust Colors:
All colors use CSS variables, change in `global.css`:
```css
:root {
    --primary-color: YOUR_COLOR;
}
```

### Modify Form Width:
```css
.auth-page__form-container {
    max-width: 500px;  /* Change from 440px */
}
```

---

## 📞 Next Steps

After testing login page:
1. Update **signup.html** with similar design
2. Update **forgot password** page (if exists)
3. Test complete auth flow
4. Add actual hero images for production

---

**Version**: 2.0
**Status**: Ready for Integration
**Dependencies**: base.html, global.css, global.js