document.addEventListener('DOMContentLoaded', function() {
    const header = document.querySelector('header');
    const body = document.body;
    let lastScrollY = window.scrollY;
    
    updateHeader();


    function updateHeader() {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
            body.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
            body.classList.remove('scrolled');
        }
        lastScrollY = window.scrollY;
    }


    let ticking = false;
    window.addEventListener('scroll', function() {
        if (!ticking) {
            window.requestAnimationFrame(function() {
                updateHeader();
                ticking = false;
            });
            ticking = true;
        }
    });

    window.addEventListener('resize', updateHeader);
});

