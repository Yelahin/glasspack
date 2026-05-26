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
