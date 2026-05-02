document.addEventListener('DOMContentLoaded', function() {
    const removeAllLogos = () => {
        const selectors = [
            '.brand-link img',
            '.site-logo img',
            '.login-logo',
            '.login-box .login-logo',
            'img[src*="logo"]',
            'img[src*="jas"]',
            'img[src*="sarbaz"]'
        ];
        
        selectors.forEach(sel => {
            document.querySelectorAll(sel).forEach(el => {
                el.style.display = 'none';
                el.style.visibility = 'hidden';
                el.style.height = '0';
                el.style.width = '0';
                el.remove();
            });
        });
        
        document.body.style.background = '#1a1d23';
        
        const box = document.querySelector('.login-box');
        if (box) {
            box.style.margin = '140px auto';
            box.style.float = 'none';
            box.style.width = '380px';
        }
    };
    
    removeAllLogos();
    setTimeout(removeAllLogos, 300);
    setTimeout(removeAllLogos, 800);
});