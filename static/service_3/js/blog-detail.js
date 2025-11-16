// Blog Detail Page Functionality
document.addEventListener('DOMContentLoaded', function() {
    initBlogDetail();
});

function initBlogDetail() {
    initStickyTOC();
    initSmoothScroll();
    initTOCHighlight();
}

// Sticky TOC functionality
function initStickyTOC() {
    const sidebar = document.querySelector('.article-sidebar');
    const mainContent = document.querySelector('.article-main');
    
    if (!sidebar || !mainContent) return;
    
    const sidebarTop = sidebar.offsetTop;
    
    function updateStickyTOC() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const mainContentBottom = mainContent.offsetTop + mainContent.offsetHeight;
        
        if (scrollTop >= sidebarTop - 20) {
            sidebar.classList.add('sticky');
            
            // Prevent sidebar from going below main content
            if (scrollTop + sidebar.offsetHeight >= mainContentBottom) {
                sidebar.classList.add('bottom-reached');
            } else {
                sidebar.classList.remove('bottom-reached');
            }
        } else {
            sidebar.classList.remove('sticky', 'bottom-reached');
        }
    }
    
    window.addEventListener('scroll', updateStickyTOC);
    window.addEventListener('resize', updateStickyTOC);
}

// Smooth scroll for TOC links
function initSmoothScroll() {
    const tocLinks = document.querySelectorAll('.toc-list a');
    
    tocLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                const headerHeight = document.querySelector('.header').offsetHeight;
                const targetPosition = targetElement.offsetTop - headerHeight - 20;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Highlight active TOC section
function initTOCHighlight() {
    const sections = document.querySelectorAll('.article-content section');
    const tocLinks = document.querySelectorAll('.toc-list a');
    
    if (sections.length === 0 || tocLinks.length === 0) return;
    
    function updateActiveSection() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const headerHeight = document.querySelector('.header').offsetHeight;
        
        let activeSection = null;
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop - headerHeight - 50;
            const sectionBottom = sectionTop + section.offsetHeight;
            
            if (scrollTop >= sectionTop && scrollTop < sectionBottom) {
                activeSection = section;
            }
        });
        
        // Remove active class from all links
        tocLinks.forEach(link => link.classList.remove('active'));
        
        // Add active class to current section link
        if (activeSection) {
            const activeId = activeSection.getAttribute('id');
            const activeLink = document.querySelector(`.toc-list a[href="#${activeId}"]`);
            if (activeLink) {
                activeLink.classList.add('active');
            }
        }
    }
    
    window.addEventListener('scroll', updateActiveSection);
    updateActiveSection(); // Initial call
}
