// static/portal/js/menu.js

document.addEventListener('DOMContentLoaded', function() {
    const recommendationsBlock = document.getElementById('recommendations-block');
    if (!recommendationsBlock) return;
    
    const customerId = window.customerId;
    if (!customerId) {
        console.warn('customerId не найден');
        return;
    }
    
    // Получаем количество рекомендаций из настроек или используем 5
    const limit = window.recommendationsLimit || 5;
    
    function renderRecommendations(containerId, data) {
        const container = document.getElementById(containerId);
        if (!container) return;
        container.innerHTML = '';
        
        if (data && data.recommendations && data.recommendations.length > 0) {
            let html = '';
            let seasonLabel = '';
            const cols = Math.min(data.recommendations.length, 4);
            
            if (data.season) {
                seasonLabel = `<div class="col-12 mb-3"><p class="text-muted">🍂 ${data.season} рекомендации</p></div>`;
            }
            
            data.recommendations.forEach(dish => {
                html += `
                    <div class="col-md-3 col-sm-6 mb-3">
                        <div class="card h-100">
                            <div class="card-body">
                                <h6 class="card-title">${dish.name}</h6>
                                <p class="card-text"><strong>${dish.price} руб.</strong></p>
                                ${dish.similarity ? `<small class="text-muted">Похожесть: ${(dish.similarity * 100).toFixed(0)}%</small>` : ''}
                                ${dish.orders_count ? `<small class="text-muted">📦 ${dish.orders_count} заказов</small>` : ''}
                            </div>
                        </div>
                    </div>
                `;
            });
            
            container.innerHTML = seasonLabel + html;
        } else {
            container.innerHTML = `
                <div class="col-12">
                    <p class="text-muted">Рекомендации пока недоступны</p>
                </div>
            `;
        }
    }
    
    // Загрузка популярных
    fetch(`/api/popular/?limit=${limit}`)
        .then(response => response.json())
        .then(data => {
            renderRecommendations('popular-container', {recommendations: data.popular || []});
        })
        .catch(err => {
            console.error('Ошибка загрузки популярных:', err);
            renderRecommendations('popular-container', {recommendations: []});
        });
    
    // Загрузка сезонных
    fetch(`/api/recommend/season/?limit=${limit}`)
        .then(response => response.json())
        .then(data => {
            renderRecommendations('season-container', data);
        })
        .catch(err => {
            console.error('Ошибка загрузки сезонных:', err);
            renderRecommendations('season-container', {recommendations: []});
        });
    
    // Загрузка персональных
    fetch(`/api/recommend/customer/${customerId}/?limit=${limit}`)
        .then(response => response.json())
        .then(data => {
            renderRecommendations('personal-container', data);
        })
        .catch(err => {
            console.error('Ошибка загрузки персональных:', err);
            renderRecommendations('personal-container', {recommendations: []});
        });
});