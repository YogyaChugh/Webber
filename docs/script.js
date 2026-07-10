document.addEventListener('DOMContentLoaded', () => {
    // Terminal typing effect
    const terminalOutput = document.querySelectorAll('.terminal .output, .terminal .prompt:not(:first-child)');
    let delay = 0;
    
    terminalOutput.forEach((el, index) => {
        el.style.opacity = '0';
        setTimeout(() => {
            el.style.opacity = '1';
        }, 1000 + (delay * 1000));
        delay += 0.8;
    });

    // Copy to clipboard
    const copyBtn = document.getElementById('copy-btn');
    if (copyBtn) {
        copyBtn.addEventListener('click', () => {
            const codeText = copyBtn.querySelector('code').innerText;
            navigator.clipboard.writeText(codeText).then(() => {
                const icon = copyBtn.querySelector('.copy-icon');
                const originalText = icon.innerText;
                icon.innerText = '✅';
                setTimeout(() => {
                    icon.innerText = originalText;
                }, 2000);
            });
        });
    }

    // Parallax effect on hero
    const heroVisual = document.querySelector('.app-mockup');
    const heroSection = document.querySelector('.hero');
    
    if (heroVisual && heroSection) {
        heroSection.addEventListener('mousemove', (e) => {
            if (window.innerWidth > 900) {
                const xAxis = (window.innerWidth / 2 - e.pageX) / 30;
                const yAxis = (window.innerHeight / 2 - e.pageY) / 30;
                
                heroVisual.style.transform = `rotateY(${xAxis}deg) rotateX(${yAxis}deg)`;
            }
        });
        
        heroSection.addEventListener('mouseleave', () => {
            if (window.innerWidth > 900) {
                heroVisual.style.transform = `rotateY(-15deg) rotateX(5deg)`;
            }
        });
    }
});
