document.addEventListener('DOMContentLoaded', () => {
    const newsSection = document.querySelector('.news-section');

    fetch('ai_news.json')
        .then(response => response.json())
        .then(data => {
            data.news_items.forEach(news => {
                const newsCard = document.createElement('div');
                newsCard.classList.add('news-card');

                newsCard.innerHTML = `
                    <div class="news-card-image">
                        <span>AI News Image</span>
                    </div>
                    <p class="date-tag">${news.date_zh}</p>
                    <h2 class="news-title">${news.title}</h2>
                    <p class="news-subtitle"></p>
                    <p class="news-content">${news.description}</p>
                    <p class="source">Source: ${news.source}</p>
                    <div class="tech-decoration"></div>
                `;
                newsSection.appendChild(newsCard);
            });

            // Re-initialize Intersection Observer for newly added cards
            const cards = document.querySelectorAll('.news-card');
            const observerOptions = {
                root: null,
                rootMargin: '0px',
                threshold: 0.1
            };
            
            const observer = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('visible');
                        observer.unobserve(entry.target);
                    }
                });
            }, observerOptions);
            
            cards.forEach(card => {
                observer.observe(card);
            });
        })
        .catch(error => console.error('Error fetching news data:', error));
});
