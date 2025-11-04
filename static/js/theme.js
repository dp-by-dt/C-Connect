// ============================================
// C-CONNECT THEME SYSTEM
// Handles light/dark theme switching
// ============================================

(function() {
  'use strict';
  
  const THEME_KEY = 'c-connect-theme';
  const themeToggle = document.getElementById('themeToggle');
  const html = document.documentElement;
  
  // Get saved theme or default to 'light'
  function getSavedTheme() {
    return localStorage.getItem(THEME_KEY) || 'light';
  }
  
  // Apply theme to document
  function applyTheme(theme) {
    html.setAttribute('data-theme', theme);
    localStorage.setItem(THEME_KEY, theme);
  }
  
  // Toggle between themes
  function toggleTheme() {
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    applyTheme(newTheme);
    
    // Add subtle animation
    themeToggle.style.transform = 'rotate(360deg)';
    setTimeout(() => {
      themeToggle.style.transform = 'rotate(0deg)';
    }, 300);
  }
  
  // Initialize theme on page load
  function initTheme() {
    const savedTheme = getSavedTheme();
    applyTheme(savedTheme);
    
    // Add event listener to toggle button
    if (themeToggle) {
      themeToggle.addEventListener('click', toggleTheme);
    }
  }
  
  // Run on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTheme);
  } else {
    initTheme();
  }
  
})();