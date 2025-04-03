document.addEventListener("DOMContentLoaded", function () {
    console.log("hello from js")
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const closeMenuBtn = document.getElementById('closeMenuBtn');
    const mobileMenu = document.getElementById('mobileMenu');
    const contactForm = document.getElementById('contactForm');

    // Mobile Menu Toggle
    function toggleMobileMenu() {
        mobileMenu.classList.toggle('active');
        console.log("Mobile menu button clicked!");
        document.body.style.overflow = mobileMenu.classList.contains('active') ? 'hidden' : '';
    }


    mobileMenuBtn.addEventListener('click', toggleMobileMenu);
    closeMenuBtn.addEventListener('click', toggleMobileMenu);

    // Close mobile menu when clicking outside
    document.addEventListener('click', (e) => {
    if (mobileMenu.classList.contains('active') && 
        !e.target.closest('.mobile-menu-container') && 
        !e.target.closest('.mobile-menu-btn')) {
        toggleMobileMenu();
    }
    });

    // Smooth scroll for navigation links
    navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const targetId = link.getAttribute('href');
        const targetSection = document.querySelector(targetId);
        
        if (mobileMenu.classList.contains('active')) {
        toggleMobileMenu();
        }

        targetSection.scrollIntoView({ behavior: 'smooth' });
    });
    });

    // Form validation and submission
    contactForm.addEventListener('submit', (e) => {
    e.preventDefault();
    
    // Get form inputs
    const name = document.getElementById('name');
    const email = document.getElementById('email');
    const phone = document.getElementById('phone');
    const course = document.getElementById('course');
    const message = document.getElementById('message');
    
    // Validate inputs
    let isValid = true;
    const errors = [];

    if (!name.value.trim()) {
        isValid = false;
        errors.push('Name is required');
        name.classList.add('error');
    }

    if (!email.value.trim() || !isValidEmail(email.value)) {
        isValid = false;
        errors.push('Valid email is required');
        email.classList.add('error');
    }

    if (!phone.value.trim() || !isValidPhone(phone.value)) {
        isValid = false;
        errors.push('Valid phone number is required');
        phone.classList.add('error');
    }

    if (!course.value) {
        isValid = false;
        errors.push('Please select a course');
        course.classList.add('error');
    }

    if (!message.value.trim()) {
        isValid = false;
        errors.push('Message is required');
        message.classList.add('error');
    }

    // Handle form submission
    if (isValid) {
        // Show success message
        showNotification('Message sent successfully!', 'success');
        contactForm.reset();
        removeErrorStyles();
    } else {
        // Show error message
        showNotification(errors.join(', '), 'error');
    }
    });

    // Input validation helpers
    function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    function isValidPhone(phone) {
    return /^\+?[\d\s-]{10,}$/.test(phone);
    }

    // Remove error styles on input
    const formInputs = contactForm.querySelectorAll('input, select, textarea');
    formInputs.forEach(input => {
    input.addEventListener('input', () => {
        input.classList.remove('error');
    });
    });

    function removeErrorStyles() {
    formInputs.forEach(input => input.classList.remove('error'));
    }

    // Notification system
    function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Remove notification after 3 seconds
    setTimeout(() => {
        notification.remove();
    }, 3000);
    }

    // Add notification styles
    const style = document.createElement('style');
    style.textContent = `
    .notification {
        position: fixed;
        bottom: 20px;
        right: 20px;
        padding: 15px 25px;
        border-radius: 5px;
        color: white;
        font-weight: 500;
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
    }

    .notification.success {
        background-color: #10B981;
    }

    .notification.error {
        background-color: #EF4444;
    }

    .error {
        border-color: #EF4444 !important;
    }

    @keyframes slideIn {
        from {
        transform: translateX(100%);
        opacity: 0;
        }
        to {
        transform: translateX(0);
        opacity: 1;
        }
    }
    `;

    document.head.appendChild(style);

    // Intersection Observer for animations
    const observerOptions = {
    threshold: 0.2,
    rootMargin: '0px'
    };

    const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
        entry.target.classList.add('animate');
        observer.unobserve(entry.target);
        }
    });
    }, observerOptions);

    // Add animation to elements
    const animateElements = document.querySelectorAll('.feature-card, .course-card, .testimonial-card');
    animateElements.forEach(element => {
    element.style.opacity = '0';
    element.style.transform = 'translateY(20px)';
    element.style.transition = 'opacity 0.5s ease-out, transform 0.5s ease-out';
    observer.observe(element);
    });

    // Add animation styles
    const animationStyles = document.createElement('style');
    animationStyles.textContent = `
    .animate {
        opacity: 1 !important;
        transform: translateY(0) !important;
    }
    `;

    document.head.appendChild(animationStyles);

    // Course hover effects
    const courseCards = document.querySelectorAll('.course-card');
    courseCards.forEach(card => {
    card.addEventListener('mouseenter', () => {
        card.style.transform = 'translateY(-5px)';
    });
    
    card.addEventListener('mouseleave', () => {
        card.style.transform = 'translateY(0)';
    });
    });

});