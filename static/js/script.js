// Auto-hide flash messages
document.addEventListener('DOMContentLoaded', function() {
    // File upload preview
    const fileInput = document.getElementById('profile_picture');
    const imagePreview = document.getElementById('imagePreview');
    const uploadText = document.querySelector('.upload-text');
    
    if (fileInput) {
        fileInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    imagePreview.innerHTML = `<img src="${e.target.result}" alt="Profile Preview">`;
                    uploadText.textContent = file.name;
                };
                reader.readAsDataURL(file);
            }
        });
    }
    
    // Auto-hide flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.flash');
    flashMessages.forEach(flash => {
        setTimeout(() => {
            flash.style.opacity = '0';
            flash.style.transform = 'translateY(-10px)';
            setTimeout(() => {
                flash.style.display = 'none';
            }, 300);
        }, 5000);
    });

    // Form validation for phone numbers
    const phoneInputs = document.querySelectorAll('input[type="tel"]');
    phoneInputs.forEach(input => {
        input.addEventListener('input', function() {
            // Remove non-digit characters as user types
            this.value = this.value.replace(/\D/g, '');
            
            // Format phone number (US format)
            if (this.value.length >= 6) {
                const formatted = this.value.replace(/(\d{3})(\d{3})(\d{4})/, '($1) $2-$3');
                this.value = formatted;
            }
        });
    });

    // Enhance form submission with loading states
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.textContent = 'Processing...';
                
                // Re-enable button after 3 seconds to prevent permanent disabled state
                setTimeout(() => {
                    submitButton.disabled = false;
                    submitButton.textContent = submitButton.dataset.originalText || 'Submit';
                }, 3000);
            }
        });
    });

    // Store original button text
    const submitButtons = document.querySelectorAll('button[type="submit"]');
    submitButtons.forEach(button => {
        button.dataset.originalText = button.textContent;
    });

    // Smooth scroll for navigation
    const navLinks = document.querySelectorAll('.nav-link[href^="#"]');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Enhanced form field interactions
    const formInputs = document.querySelectorAll('input, select, textarea');
    formInputs.forEach(input => {
        // Add focus styling
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
        });
        
        // Show/hide password strength indicator
        if (input.type === 'password') {
            input.addEventListener('input', function() {
                showPasswordStrength(this);
            });
        }
    });

    // Password strength indicator
    function showPasswordStrength(passwordInput) {
        let existingIndicator = passwordInput.parentElement.querySelector('.password-strength');
        
        if (!existingIndicator) {
            existingIndicator = document.createElement('div');
            existingIndicator.className = 'password-strength';
            passwordInput.parentElement.appendChild(existingIndicator);
        }
        
        const password = passwordInput.value;
        let strength = 0;
        let message = '';
        
        if (password.length >= 8) strength++;
        if (/[a-z]/.test(password)) strength++;
        if (/[A-Z]/.test(password)) strength++;
        if (/[0-9]/.test(password)) strength++;
        if (/[^A-Za-z0-9]/.test(password)) strength++;
        
        switch (strength) {
            case 0:
            case 1:
                message = 'Weak password';
                existingIndicator.className = 'password-strength weak';
                break;
            case 2:
            case 3:
                message = 'Medium password';
                existingIndicator.className = 'password-strength medium';
                break;
            case 4:
            case 5:
                message = 'Strong password';
                existingIndicator.className = 'password-strength strong';
                break;
        }
        
        existingIndicator.textContent = password.length > 0 ? message : '';
    }
});

// Utility functions
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

// Add CSS for password strength indicator
const style = document.createElement('style');
style.textContent = `
    .password-strength {
        font-size: 0.8rem;
        margin-top: 0.25rem;
        padding: 0.25rem 0;
    }
    
    .password-strength.weak {
        color: #dc2626;
    }
    
    .password-strength.medium {
        color: #f59e0b;
    }
    
    .password-strength.strong {
        color: #059669;
    }
    
    .form-group.focused label {
        color: #2563eb;
    }
`;
document.head.appendChild(style);