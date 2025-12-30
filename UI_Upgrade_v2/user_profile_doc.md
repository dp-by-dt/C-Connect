# Profile Page - Update Documentation

## 📋 Overview
Modern split-layout profile page with glassmorphism design. Fixed sidebar (desktop) with scrollable content area. Sticky header on mobile.

---

## 🎨 Design Features

### Layout:
- **Desktop**: 
  - Left: Fixed profile card (420px, sticky)
  - Right: Scrollable posts section
  - Glass morphism effects throughout
  
- **Mobile**: 
  - Stacked layout
  - Sticky header appears on scroll (profile pic + name)
  - Normal scroll behavior

### Visual Elements:
1. **Profile Card (Left)**:
   - Large avatar with gradient background
   - Username + email
   - Stats (connections & posts count)
   - Bio section
   - Details (email, department, year, location)
   - Interest tags
   - Edit profile button

2. **Posts Section (Right)**:
   - Header with title
   - Grid layout for posts
   - Empty state placeholder
   - Ready for backend integration

---

## 📁 File Structure

### HTML Structure:
```html
<div class="profile-page">
  <!-- Mobile sticky header -->
  <div class="profile-mobile-header">...</div>
  
  <!-- Left: Profile card (fixed) -->
  <aside class="profile-page__left">
    <div class="profile-card">
      <!-- Avatar -->
      <!-- Info -->
      <!-- Stats -->
      <!-- Bio -->
      <!-- Details -->
      <!-- Interests -->
      <!-- Edit button -->
    </div>
  </aside>
  
  <!-- Right: Posts (scrollable) -->
  <main class="profile-page__right">
    <div class="profile-posts">
      <!-- Posts grid or empty state -->
    </div>
  </main>
</div>
```

### CSS Classes (BEM):
- `.profile-page` - Main container
- `.profile-page__left` - Left sidebar
- `.profile-page__right` - Right content
- `.profile-card__*` - Profile card elements
- `.profile-posts__*` - Posts section elements
- `.profile-mobile-header__*` - Mobile sticky header

---

## 🔧 Backend Integration Points

### Current Variables Used:
```jinja
{{ current_user.username }}
{{ current_user.email }}
{{ profile.profile_picture }}
{{ profile.bio }}
{{ profile.department }}
{{ profile.year }}
{{ profile.location }}
{{ profile.interests }}  // Array/list
{{ url_for('auth.profile_edit') }}
```

### Placeholder Variables (TODO):
```jinja
<!-- Add these to your User model -->
{{ current_user.connection_count }}  // or connections.count()
{{ current_user.posts_count }}       // or posts.count()
```

### Posts Integration (TODO):
```jinja
<!-- Currently shows empty state -->
<!-- Replace {% if false %} with: -->

{% if current_user.posts %}
  <div class="profile-posts__grid">
    {% for post in current_user.posts %}
      <!-- Your post card here -->
      <div class="post-item">
        {% if post.image %}
          <img src="{{ post.image }}">
        {% endif %}
        {{ post.content }}
      </div>
    {% endfor %}
  </div>
{% else %}
  <!-- Empty state -->
{% endif %}
```

---

## 🎯 Features

### 1. Profile Stats:
- **Connections Count**: Shows connection/follower count
- **Posts Count**: Shows total posts
- Both use placeholder "0" if not defined
- Hover effects on stat cards

### 2. Bio Section:
- Shows user bio if exists
- Placeholder text if empty
- Bordered, highlighted design

### 3. Details Section:
- Email (always shown)
- Department
- Year
- Location
- Each with icon and label
- "Not specified" for empty fields
- Hover effects

### 4. Interest Tags:
- Gradient background
- View-only (not clickable yet)
- Grid layout, wraps nicely
- Hover lift effect
- TODO: Make clickable for filtering

### 5. Edit Profile Button:
- Redirects to `{{ url_for('auth.profile_edit') }}`
- Gradient background
- Icon + text
- Full width
- Hover lift effect

### 6. Mobile Sticky Header:
- Hidden by default
- Appears when scrolled past avatar
- Shows compact: avatar + username + email
- Smooth slide-in animation
- Glass morphism background

---

## 📱 Responsive Behavior

### Desktop (> 1024px):
- Split layout
- Left card sticky, max-height viewport
- Right side scrolls independently
- Animations: fadeInLeft & fadeInRight

### Tablet (768px - 1024px):
- Stacked layout
- Profile card centered (max 600px)
- Posts section full width
- No sticky positioning

### Mobile (< 768px):
- Full stacked layout
- Sticky header on scroll
- Reduced padding
- Smaller avatar (120px)
- 2-column posts grid

### Small Mobile (< 480px):
- Smaller stats
- Minimal spacing
- Touch-optimized

---

## 🎨 Glass Morphism Implementation

### Profile Card:
```css
background: var(--glass-bg);
backdrop-filter: blur(30px) saturate(180%);
border: 1px solid var(--glass-border);
```

### Decorative Gradient:
- Top of card has subtle gradient overlay
- 8% opacity
- Provides depth without overwhelming

---

## 🔄 Migration Notes

### Changes from Old Design:
1. ✅ Removed centered single-card layout
2. ✅ Added split-screen layout
3. ✅ Added glass morphism effects
4. ✅ New deep forest green theme
5. ✅ Stats section redesigned
6. ✅ Details with icons
7. ✅ Posts placeholder section added
8. ✅ Mobile sticky header added

### Backend Variables Preserved:
- ✅ All `current_user.*` variables
- ✅ All `profile.*` variables
- ✅ All `url_for()` routes
- ✅ No breaking changes

### New Variables Needed:
- `current_user.connection_count` - Add to model
- `current_user.posts_count` - Add to model
- `current_user.posts` - For posts grid

---

## ✅ Testing Checklist

- [ ] Profile card displays correctly
- [ ] Avatar shows (image or initial)
- [ ] Stats show placeholder "0"
- [ ] Bio displays or shows placeholder
- [ ] All details display correctly
- [ ] Interest tags display
- [ ] Edit profile button redirects correctly
- [ ] Posts empty state shows
- [ ] Desktop: Left card is sticky
- [ ] Desktop: Right side scrolls
- [ ] Tablet: Stacked layout
- [ ] Mobile: Sticky header appears on scroll
- [ ] Mobile: 2-column posts grid
- [ ] Glass effects work
- [ ] Dark mode compatible
- [ ] Animations smooth

---

## 🚀 Next Steps

1. **Add Connections Count**:
```python
# In User model
@property
def connection_count(self):
    return Connection.query.filter_by(
        user_id=self.id, 
        status='accepted'
    ).count()
```

2. **Add Posts Count**:
```python
@property
def posts_count(self):
    return Post.query.filter_by(user_id=self.id).count()
```

3. **Integrate Posts Grid**:
   - Query user posts
   - Pass to template
   - Update `{% if false %}` to `{% if current_user.posts %}`
   - Design post card component

4. **Make Interests Clickable** (Future):
   - Add route for interest filtering
   - Update tags to `<a>` elements
   - Filter/search functionality

---

## 📞 Customization Guide

### Change Card Width:
```css
.profile-page__left {
    flex: 0 0 500px;  /* Wider card */
}
```

### Change Avatar Size:
```css
.profile-card__avatar {
    width: 180px;
    height: 180px;
}
```

### Change Posts Grid Columns:
```css
.profile-posts__grid {
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
}
```

### Disable Sticky Header (Mobile):
Remove or comment out the `<script>` section at the bottom

---

**Version**: 2.0
**Status**: Ready for Integration
**Dependencies**: base.html, global.css (v3.0), global.js

**Compatible with**: New deep forest green theme, glass morphism design system