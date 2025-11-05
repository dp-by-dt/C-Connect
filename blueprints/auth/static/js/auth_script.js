// ===== PASSWORD VISIBILITY TOGGLE =====
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

// ===== PASSWORD STRENGTH CHECKER =====
function checkPasswordStrength(password) {
    let strength = 0;
    
    // Length check
    if (password.length >= 8) strength += 1;
    if (password.length >= 12) strength += 1;
    
    // Complexity checks
    if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength += 1;
    if (/\d/.test(password)) strength += 1;
    if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) strength += 1;
    
    return strength;
}

function updatePasswordStrength() {
    const password = document.getElementById('password').value;
    const strengthIndicator = document.getElementById('passwordStrength');
    
    if (!strengthIndicator) return;
    
    const strength = checkPasswordStrength(password);
    
    strengthIndicator.className = 'password-strength';
    
    if (password.length === 0) {
        strengthIndicator.className = 'password-strength';
    } else if (strength <= 2) {
        strengthIndicator.classList.add('weak');
    } else if (strength <= 3) {
        strengthIndicator.classList.add('medium');
    } else {
        strengthIndicator.classList.add('strong');
    }
}

// ===== PASSWORD MATCH VALIDATION =====
function validatePasswordMatch() {
    const password = document.getElementById('password');
    const confirmPassword = document.getElementById('confirm_password');
    const feedback = document.getElementById('confirmPasswordFeedback');
    
    if (!confirmPassword || !password) return;
    
    if (confirmPassword.value && password.value !== confirmPassword.value) {
        confirmPassword.setCustomValidity('Passwords do not match');
        if (feedback) {
            feedback.textContent = 'Passwords do not match';
        }
    } else {
        confirmPassword.setCustomValidity('');
        if (feedback) {
            feedback.textContent = 'Passwords must match';
        }
    }
}

// ===== FORM SUBMISSION HANDLERS =====
document.addEventListener('DOMContentLoaded', () => {
    // Password strength checker
    const passwordInput = document.getElementById('password');
    if (passwordInput) {
        passwordInput.addEventListener('input', updatePasswordStrength);
    }
    
    // Password match validation
    const confirmPasswordInput = document.getElementById('confirm_password');
    if (confirmPasswordInput) {
        confirmPasswordInput.addEventListener('input', validatePasswordMatch);
        passwordInput.addEventListener('input', validatePasswordMatch);
    }
    
    // Login form submission
    const loginForm = document.querySelector('#loginBtn');
    if (loginForm) {
        loginForm.closest('form').addEventListener('submit', function(e) {
            if (this.checkValidity()) {
                const originalText = window.cconnect.showLoading(loginForm);
                // Form will submit normally, loading state for UX
            }
        });
    }
    
    // Signup form submission
    const signupForm = document.getElementById('signupForm');
    if (signupForm) {
        signupForm.addEventListener('submit', function(e) {
            if (this.checkValidity()) {
                const signupBtn = document.getElementById('signupBtn');
                const originalText = window.cconnect.showLoading(signupBtn);
                // Form will submit normally, loading state for UX
            }
        });
    }
    
    // Auto-focus on first input
    const firstInput = document.querySelector('.auth-card input:not([type="checkbox"])');
    if (firstInput && !firstInput.value) {
        firstInput.focus();
    }
});

// ===== USERNAME VALIDATION =====
const usernameInput = document.getElementById('username');
if (usernameInput) {
    usernameInput.addEventListener('input', function() {
        // Remove any non-alphanumeric characters except underscore
        this.value = this.value.replace(/[^a-zA-Z0-9_]/g, '');
    });
}

// ===== EMAIL VALIDATION =====
const emailInput = document.getElementById('email');
if (emailInput) {
    emailInput.addEventListener('blur', function() {
        if (this.value && !this.value.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) {
            this.setCustomValidity('Please enter a valid email address');
        } else {
            this.setCustomValidity('');
        }
    });
}

// ===== REMEMBER ME TOOLTIP =====
const rememberCheckbox = document.getElementById('remember');
if (rememberCheckbox) {
    rememberCheckbox.addEventListener('change', function() {
        if (this.checked) {
            window.cconnect.showToast('You will stay logged in for 30 days', 'info');
        }
    });
}

// ===== PREVENT DOUBLE SUBMISSION =====
document.querySelectorAll('form').forEach(form => {
    let submitted = false;
    form.addEventListener('submit', function(e) {
        if (submitted) {
            e.preventDefault();
            return false;
        }
        if (this.checkValidity()) {
            submitted = true;
        }
    });
});