# Template Components - Update Documentation

## 📋 Overview
Updated three global template components with modern, card-based designs matching the new C-Connect aesthetic.

---

## 📁 Files Updated

### 1. **user_card.html**
**Location**: `templates/components/user_card.html` (or wherever you store it)

#### Major Changes:

**Old Design:**
- Centered circular avatar with gradient background
- Stacked layout: Avatar → Name → Email → Button
- Basic card styling

**New Design:**
- Full-bleed user image covering most of card (380px height)
- Name + email overlay at top with gradient background
- Blurred footer section at bottom with action buttons
- "Connecting" status indicator with animated spinner
- Eye icon button for quick profile view
- Hover effect: Card lifts and image zooms slightly

#### Structure:
```html
<div class="user-card">
  <div class="user-card__image-wrapper">
    <img class="user-card__image">
    <div class="user-card__header"> <!-- Overlay -->
      <h3 class="user-card__name">
      <p class="user-card__email">
    </div>
  </div>
  <div class="user-card__footer"> <!-- Blurred -->
    <div class="user-card__status"> <!-- Optional -->
    <div class="user-card__actions">
      <!-- Buttons -->
    </div>
  </div>
</div>
```

#### Backend Variables Preserved:
- ✅ `{{ user.id }}`
- ✅ `{{ user.username }}`
- ✅ `{{ user.email }}`
- ✅ `{{ user.profile.profile_picture }}`
- ✅ `{{ conn_status }}` (connected, requested, incoming, or empty)
- ✅ `{{ csrf_token() }}`
- ✅ `{{ url_for('main.view_user_profile', user_id=user.id) }}`
- ✅ `{{ url_for('messages.chat', user_id=user.id) }}`
- ✅ `{{ url_for('connections.connections_send', target_id=user.id) }}`

#### Button States:
1. **Connected**: Message button + Eye icon
2. **Incoming**: "Pending" disabled button
3. **Requested**: "Requested" disabled button + spinner status
4. **None**: "Add Member" connect button + Eye icon

#### CSS Classes (BEM):
- `.user-card` - Main container
- `.user-card__image-wrapper` - Image section
- `.user-card__image` - Actual image
- `.user-card__avatar-fallback` - Gradient with initial letter
- `.user-card__header` - Top overlay (name/email)
- `.user-card__footer` - Bottom blurred section
- `.user-card__status` - Status indicator
- `.user-card__actions` - Button container
- `.user-card__btn` - Button base
- `.user-card__btn--primary` - Primary button style
- `.user-card__btn--secondary` - Secondary button style
- `.user-card__btn--disabled` - Disabled state
- `.user-card__spinner` - Loading spinner

---

### 2. **user_card_action_btn.html**
**Location**: `templates/components/user_card_action_btn.html`

#### Major Changes:

**Old Design:**
- Basic Bootstrap button styles
- Simple icon + text

**New Design:**
- Modern rounded buttons with smooth transitions
- Loading states with spinners
- Better visual feedback (hover effects)
- AJAX functionality built-in
- Toast notifications on success/error

#### Button Types:

1. **Connected (Accepted)**:
   ```html
   <button class="action-btn action-btn--success" disabled>
     Connected
   </button>
   ```

2. **Incoming Request**:
   ```html
   <div class="action-btn-group">
     <button class="action-btn--primary action-accept">Accept</button>
     <button class="action-btn--danger action-reject">Reject</button>
   </div>
   ```

3. **Outgoing Request (Pending)**:
   ```html
   <button class="action-btn--warning action-cancel">
     Cancel Request
   </button>
   ```

4. **No Connection**:
   ```html
   <button class="action-btn--primary action-connect">
     Connect
   </button>
   ```

#### AJAX Functionality:
All buttons now have built-in AJAX handlers:
- Shows loading spinner during request
- Displays toast notification on success/error
- Reloads page after successful action
- Restores button state on error

#### API Endpoints Used:
- ✅ `/connections/accept/{conn_id}` - POST
- ✅ `/connections/reject/{conn_id}` - POST
- ✅ `/connections/cancel/{conn_id}` - POST
- ✅ `/connections/send/{user_id}` - POST

#### CSS Classes:
- `.action-btn` - Base button
- `.action-btn--primary` - Green gradient
- `.action-btn--success` - Success green
- `.action-btn--danger` - Red outline
- `.action-btn--warning` - Orange outline
- `.action-btn--secondary` - Gray outline
- `.action-btn--sm` - Small size
- `.action-btn__spinner` - Loading animation
- `.action-btn-group` - Horizontal button group

---

### 3. **flash.html**
**Location**: `templates/components/flash.html`

#### Major Changes:

**Old Design:**
- Basic Bootstrap alerts
- Manual dismiss only
- Fixed positioning

**New Design:**
- Modern toast-style notifications
- Fixed top-right positioning (responsive)
- Auto-dismiss after 5 seconds
- Animated slide-in/slide-out
- Progress bar showing time remaining
- Icon-based visual indicators
- Manual close button

#### Features:

1. **Auto-dismiss**: Fades out after 5 seconds
2. **Progress bar**: Visual countdown at bottom
3. **Icons**: Different icons for each category
4. **Animations**: Smooth slide-in from right, slide-out
5. **Stacking**: Multiple messages stack vertically
6. **Responsive**: Full-width on mobile

#### Message Types:
```html
<!-- Success -->
<div class="flash-message flash-message--success">
  <i class="bi bi-check-circle-fill"></i>
  Message
</div>

<!-- Danger/Error -->
<div class="flash-message flash-message--danger">
  <i class="bi bi-exclamation-triangle-fill"></i>
  Message
</div>

<!-- Warning -->
<div class="flash-message flash-message--warning">
  <i class="bi bi-exclamation-circle-fill"></i>
  Message
</div>

<!-- Info -->
<div class="flash-message flash-message--info">
  <i class="bi bi-info-circle-fill"></i>
  Message
</div>
```

#### JavaScript Functions:

1. **dismissFlashMessage(button)**
   - Manually dismiss message
   - Called on close button click

2. **showFlashMessage(message, category)**
   - Programmatically create flash message
   - Available globally via `window.showFlashMessage()`
   - Usage: `showFlashMessage('Success!', 'success')`

#### CSS Classes:
- `.flash-messages-container` - Fixed container
- `.flash-message` - Individual message
- `.flash-message--success/danger/warning/info` - Type variants
- `.flash-message__icon` - Icon container
- `.flash-message__content` - Message text
- `.flash-message__close` - Close button
- `.flash-message__progress` - Progress bar
- `.flash-message--hiding` - Exit animation

---

## 🔧 Integration Guide

### How to Use:

#### 1. User Card:
```jinja
{% include 'components/user_card.html' 
   with user=user, 
        conn_status='connected' %}
```

**Variables needed:**
- `user` - User object
- `conn_status` - Connection status ('connected', 'requested', 'incoming', or None)

#### 2. Action Buttons:
```jinja
{% include 'components/user_card_action_btn.html' 
   with connection_status='pending',
        incoming_request=True,
        connection_id=123,
        user=user %}
```

**Variables needed:**
- `connection_status` - 'accepted', 'pending', or None
- `incoming_request` - Boolean (True if incoming)
- `connection_id` - ID for accept/reject/cancel
- `user` - User object (for connect action)

#### 3. Flash Messages:
```jinja
{% include 'components/flash.html' %}
```

**Backend usage:**
```python
from flask import flash

flash('Connection sent successfully!', 'success')
flash('Error occurred', 'danger')
flash('Please verify email', 'warning')
flash('Profile updated', 'info')
```

**JavaScript usage:**
```javascript
showFlashMessage('Saved successfully!', 'success');
```

---

## 🎨 Customization

### Change Card Dimensions:
```css
.user-card__image-wrapper {
    height: 320px;  /* Adjust image height */
}

.user-card {
    max-width: 280px;  /* Adjust card width */
}
```

### Change Button Colors:
```css
.action-btn--primary {
    background: your-gradient;
}
```

### Change Toast Duration:
```javascript
// In flash.html, find setTimeout(5000)
setTimeout(function() { ... }, 8000);  // 8 seconds
```

---

## 📱 Responsive Behavior

### User Card:
- **Desktop**: 320px max width, 380px image height
- **Mobile**: Full width, 320px image height
- **Hover**: Disabled on touch devices

### Action Buttons:
- **Desktop**: Horizontal layout
- **Mobile**: Stack vertically if needed
- Touch targets: Minimum 44x44px

### Flash Messages:
- **Desktop**: Fixed top-right, 400px max width
- **Mobile**: Full width with side padding

---

## 🐛 Common Issues

### Issue 1: User image not displaying
**Cause**: `user.profile` or `profile_picture` is None
**Solution**: Card shows gradient with initial letter as fallback

### Issue 2: AJAX buttons not working
**Cause**: CSRF token not found or `window.cconnect` not available
**Solution**: Ensure global.js is loaded and CSRF token in form

### Issue 3: Flash messages not auto-dismissing
**Cause**: JavaScript not executing
**Solution**: Check console for errors, ensure script tag is present

### Issue 4: Buttons too small on mobile
**Cause**: Font size or padding too small
**Solution**: Adjust `.action-btn--sm` padding for mobile

---

## ✅ Testing Checklist

### User Card:
- [ ] Image displays correctly
- [ ] Fallback gradient shows when no image
- [ ] Name and email overlay visible
- [ ] Buttons work for all connection states
- [ ] Card clickable (redirects to profile)
- [ ] Hover effects work
- [ ] Responsive on mobile

### Action Buttons:
- [ ] Accept button works
- [ ] Reject button works
- [ ] Cancel button works
- [ ] Connect button works
- [ ] Loading spinner shows during request
- [ ] Toast notification appears
- [ ] Page reloads on success
- [ ] Button restores on error

### Flash Messages:
- [ ] Messages appear in top-right
- [ ] Auto-dismiss after 5 seconds
- [ ] Manual close works
- [ ] Progress bar animates
- [ ] Icons show correctly
- [ ] Multiple messages stack properly
- [ ] Responsive on mobile
- [ ] JavaScript function `showFlashMessage()` works

---

## 🔄 Migration Notes

### What You Need to Do:

1. **Replace template files** in your project
2. **Update any pages** that include these components
3. **Test all connection flows** (send, accept, reject, cancel)
4. **Verify CSRF tokens** are present in forms
5. **Check toast notifications** appear correctly

### Backend Routes Required:
- `/connections/accept/<conn_id>` - POST
- `/connections/reject/<conn_id>` - POST
- `/connections/cancel/<conn_id>` - POST
- `/connections/send/<user_id>` - POST
- `/messages/chat/<user_id>` - POST
- `/main/view_user_profile/<user_id>` - GET

**All these should already exist in your Flask app!**

---

## 🚀 Performance

- **User Card**: ~3KB CSS, no JS
- **Action Buttons**: ~2KB CSS, ~4KB JS
- **Flash Messages**: ~2KB CSS, ~3KB JS
- **Total**: ~14KB combined (unminified)

---

## 📞 Next Steps

After confirming these work:
1. Test on search/discover pages
2. Test on connections page
3. Test on profile pages
4. Verify all AJAX actions
5. Check mobile responsiveness

---

**Version**: 2.0
**Last Updated**: December 2024
**Status**: Ready for Integration