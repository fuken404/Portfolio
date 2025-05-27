// Este archivo contiene el código JavaScript que maneja la interactividad de la sección de noticias.

document.addEventListener('DOMContentLoaded', () => {
    const newsContainer = document.getElementById('news-container');

    // Función para cargar noticias
    const loadNews = async () => {
        try {
            const response = await fetch('https://api.example.com/news'); // URL de la API de noticias
            const newsData = await response.json();
            displayNews(newsData);
        } catch (error) {
            console.error('Error al cargar las noticias:', error);
        }
    };

    // Función para mostrar noticias en el contenedor
    const displayNews = (news) => {
        newsContainer.innerHTML = ''; // Limpiar el contenedor
        news.forEach(article => {
            const articleElement = document.createElement('article');
            articleElement.setAttribute('itemscope', '');
            articleElement.setAttribute('itemtype', 'https://schema.org/NewsArticle');

            articleElement.innerHTML = `
                <header>
                    <h2 itemprop="headline">${article.title}</h2>
                    <time itemprop="datePublished" datetime="${article.date}">${new Date(article.date).toLocaleDateString()}</time>
                </header>
                <p itemprop="articleBody">${article.content}</p>
            `;
            newsContainer.appendChild(articleElement);
        });
    };

    // Cargar noticias al iniciar
    loadNews();
});