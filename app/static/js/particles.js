// Функция для создания частиц
function createParticles(containerId, count = 50) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    // Очищаем контейнер перед созданием новых частиц
    container.innerHTML = '';
    
    // Создаем частицы
    for (let i = 0; i < count; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        
        // Случайные параметры для каждой частицы
        const size = Math.random() * 25 + 5; // От 5px до 30px
        const opacity = Math.random() * 0.4 + 0.1; // От 0.1 до 0.5
        const left = Math.random() * 100; // От 0% до 100%
        const top = Math.random() * 100; // От 0% до 100%
        const animationDelay = Math.random() * 5; // От 0s до 5s
        const animationDuration = Math.random() * 4 + 4; // От 4s до 8s
        
        // Применяем стили
        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;
        particle.style.left = `${left}%`;
        particle.style.top = `${top}%`;
        particle.style.opacity = opacity;
        particle.style.animationDelay = `${animationDelay}s`;
        particle.style.animationDuration = `${animationDuration}s`;
        
        // Случайный градиент для разнообразия
        const gradients = [
            'linear-gradient(45deg, #ff6b6b, #4ecdc4)',
            'linear-gradient(45deg, #4ecdc4, #ff6b6b)',
            'linear-gradient(45deg, #ff6b6b, #ffd93d)',
            'linear-gradient(45deg, #6bcf7f, #4ecdc4)'
        ];
        const randomGradient = gradients[Math.floor(Math.random() * gradients.length)];
        particle.style.background = randomGradient;
        
        // Добавляем в контейнер
        container.appendChild(particle);
    }
}

// Улучшенная функция для адаптивного создания частиц
function createResponsiveParticles(containerId, options = {}) {
    const {
        density = 'medium', // 'low', 'medium', 'high', 'very-high'
        sizeRange = { min: 3, max: 30 },
        opacityRange = { min: 0.1, max: 0.6 }
    } = options;
    
    const densityMap = {
        'low': 20,
        'medium': 50,
        'high': 100,
        'very-high': 200
    };
    
    const count = densityMap[density] || 50;
    createParticles(containerId, count, sizeRange, opacityRange);
}

// Обновленная функция createParticles с дополнительными параметрами
function createParticles(containerId, count = 50, sizeRange = { min: 3, max: 30 }, opacityRange = { min: 0.1, max: 0.6 }) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    container.innerHTML = '';
    
    // Создаем фрагмент для оптимизации производительности
    const fragment = document.createDocumentFragment();
    
    for (let i = 0; i < count; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        
        // Случайные параметры
        const size = Math.random() * (sizeRange.max - sizeRange.min) + sizeRange.min;
        const opacity = Math.random() * (opacityRange.max - opacityRange.min) + opacityRange.min;
        const left = Math.random() * 100;
        const top = Math.random() * 100;
        const animationDelay = Math.random() * 5;
        const animationDuration = Math.random() * 4 + 4;
        
        // Случайный цвет градиента
        const hue1 = Math.random() * 360;
        const hue2 = (hue1 + 120) % 360; // Комплементарный цвет
        const gradient = `linear-gradient(45deg, hsl(${hue1}, 70%, 60%), hsl(${hue2}, 70%, 60%))`;
        
        // Применяем стили
        Object.assign(particle.style, {
            width: `${size}px`,
            height: `${size}px`,
            left: `${left}%`,
            top: `${top}%`,
            opacity: opacity,
            animationDelay: `${animationDelay}s`,
            animationDuration: `${animationDuration}s`,
            background: gradient,
            borderRadius: Math.random() > 0.7 ? '30%' : '50%',
            filter: `blur(${size * 0.1}px)`,
            transform: `rotate(${Math.random() * 360}deg)`
        });
        
        fragment.appendChild(particle);
    }
    
    container.appendChild(fragment);
}

// Функция для обновления частиц при изменении размера окна
function updateParticlesOnResize(containerId) {
    let resizeTimeout;
    
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            const container = document.getElementById(containerId);
            if (container && container.children.length > 0) {
                // Сохраняем текущие настройки и пересоздаем частицы
                const particles = Array.from(container.children);
                const count = particles.length;
                
                // Пересоздаем с теми же параметрами
                createParticles(containerId, count);
            }
        }, 250);
    });
}

// Функция для интерактивных частиц (реагируют на курсор)
function createInteractiveParticles(containerId, count = 50) {
    createParticles(containerId, count);
    const container = document.getElementById(containerId);
    
    container.addEventListener('mousemove', (e) => {
        const rect = container.getBoundingClientRect();
        const x = ((e.clientX - rect.left) / rect.width) * 100;
        const y = ((e.clientY - rect.top) / rect.height) * 100;
        
        const particles = container.children;
        const force = 30; // Сила отталкивания
        
        Array.from(particles).forEach(particle => {
            const particleLeft = parseFloat(particle.style.left);
            const particleTop = parseFloat(particle.style.top);
            
            const dx = particleLeft - x;
            const dy = particleTop - y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            
            if (distance < 20) {
                const angle = Math.atan2(dy, dx);
                const moveX = Math.cos(angle) * force;
                const moveY = Math.sin(angle) * force;
                
                particle.style.transform = `translate(${moveX}px, ${moveY}px)`;
                particle.style.transition = 'transform 0.3s ease';
            } else {
                particle.style.transform = 'translate(0, 0)';
                particle.style.transition = 'transform 0.5s ease';
            }
        });
    });
}

// Инициализация после загрузки страницы
document.addEventListener('DOMContentLoaded', () => {
    // Создаем 75 частиц по умолчанию
    createInteractiveParticles('particles', 100);
    
    // Или используйте одну из других функций:
    // createResponsiveParticles('particles', { density: 'high' });
    // createInteractiveParticles('particles', 100);
    
    // Добавляем обработчик изменения размера окна
    updateParticlesOnResize('particles');
});

// Экспортируем функции для использования в консоли разработчика
window.Particles = {
    createParticles,
    createResponsiveParticles,
    createInteractiveParticles,
    updateParticlesOnResize
};

