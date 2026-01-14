Использование:

Базовое использование (создать 75 частиц):

javascript
createParticles('particles', 75);
С настройкой плотности:

javascript
createResponsiveParticles('particles', { density: 'high' });


Интерактивные частицы (реагируют на курсор):

javascript
createInteractiveParticles('particles', 100);
С кастомными параметрами:

javascript
createParticles('particles', 50, 
    { min: 5, max: 40 },   // размер
    { min: 0.05, max: 0.8 } // прозрачность
);
Возможности кода:

Динамическое создание любого количества частиц

Случайные размеры, позиции, прозрачность и анимация

Разные типы анимации для разнообразия

Адаптация при изменении размера окна

Опциональная интерактивность (реакция на курсор)

Производительная оптимизация через DocumentFragment

Для использования в консоли разработчика:
Вы можете вызвать функции прямо из консоли:

javascript
`Particles.createParticles('particles', 200);
Particles.createInteractiveParticles('particles', 150);
`