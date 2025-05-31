// 浏览器端JSON加载和渲染
document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('ai_news.json');
        if (!response.ok) throw new Error('Network response was not ok');
        const data = await response.json();
        
        const newsSection = document.querySelector('.news-section');
        newsSection.innerHTML = data.news_items.map(item => `
            <article class="news-card">
                <div class="tech-decoration"></div>
                <span class="date-tag">${item.date_zh}</span>
                <h2 class="news-title">${item.title}</h2>
                <p class="news-content">${item.description}</p>
                <p class="source">${item.description.match(/来源：(.*)/)?.[1] || 'AI Weekly'}</p>
            </article>
        `).join('\n');

        // 初始化滚动动画观察器
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });

        document.querySelectorAll('.news-card').forEach(card => {
            observer.observe(card);
        });
    } catch (error) {
        console.error('Error loading news data:', error);
    }
});
