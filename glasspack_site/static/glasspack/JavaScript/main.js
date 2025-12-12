document.addEventListener("DOMContentLoaded", function () {
    // Scroll Animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: "0px 0px -50px 0px"
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    const animatedElements = document.querySelectorAll('.animate-on-scroll, section h2, section p, .product-card, .glass-card');
    animatedElements.forEach(el => {
        el.style.opacity = '0'; // Initial state before animation classes kick in (if not handled by CSS class directly)
        el.classList.add('fade-in-up'); // For now, just adding class immediately or let observer handle it if we want trigger.
        // Actually, let's reset opacity in JS if we want the observer to trigger it properly, 
        // OR rely on the CSS 'fade-in-up' class starting at opacity 0.
        // Let's refine:
        el.classList.remove('fade-in-up'); // Remove if present
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
        observer.observe(el);
    });

    // Override the observer callback to just change styles vs add class if we want manual control,
    // but adding class is cleaner. 
    // Let's re-instantiate observer with simpler logic matching CSS.

    const simpleObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                simpleObserver.unobserve(entry.target);
            }
        });
    }, observerOptions);

    animatedElements.forEach(el => simpleObserver.observe(el));
});
