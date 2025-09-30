class NewsInfiniteScroll {
    constructor(containerId) {
        // Находим основные DOM-элементы по их ID
        this.container = document.getElementById(containerId);        // Контейнер для новостей
        this.loadingIndicator = document.getElementById('loadingIndicator'); // Индикатор загрузки
        this.endMessage = document.getElementById('endMessage');      // Сообщение о конце списка

        // Инициализация переменных состояния
        this.counter = 0;         // Счетчик загруженных новостей (для пагинации)
        this.isLoading = false;   // Флаг: идет ли сейчас загрузка данных
        this.hasMore = true;      // Флаг: есть ли еще данные на сервере

        // Создаем сентинел-элемент и инициализируем компонент
        this.createSentinel();    // Создаем элемент-наблюдатель
        this.init();              // Запускаем инициализацию
    }

    init() {
        // Основная инициализация компонента
        this.setupObserver();     // Настраиваем Intersection Observer
        this.loadInitialNews();   // Загружаем первые новости
    }

    createSentinel() {
        // Создаем элемент-сентинел (наблюдатель) для отслеживания прокрутки
        this.sentinel = document.createElement('div');  // Создаем новый div элемент
        this.sentinel.id = 'sentinel';                  // Назначаем ID для идентификации
        this.sentinel.style.height = '1px';             // Делаем минимальную высоту (почти невидим)
        this.container.appendChild(this.sentinel);      // Добавляем сентинел в контейнер новостей
    }

    setupObserver() {
        // Создаем Intersection Observer для отслеживания видимости сентинела
        this.observer = new IntersectionObserver(entries => {
            // entries[0] - информация о наблюдении за сентинелом
            if (entries[0].isIntersecting &&     // Если сентинел виден в viewport
                !this.isLoading &&               // И не идет загрузка
                this.hasMore) {                  // И есть еще данные
                this.loadMoreNews();             // Загружаем новые новости
            }
        }, {
            rootMargin: '100px' // Расширяем зону наблюдения на 100px ДО достижения сентинела
        });

        // Начинаем наблюдение за сентинел-элементом
        this.observer.observe(this.sentinel);
    }

    async loadInitialNews() {
        // Загрузка первоначальных новостей при старте
        await this.loadMoreNews(); // Просто вызываем основную функцию загрузки
    }

    async loadMoreNews() {
        // Основная функция загрузки новостей с сервера
        if (this.isLoading || !this.hasMore) return; // Выходим если уже грузим или данных нет

        this.isLoading = true;  // Устанавливаем флаг загрузки
        this.showLoading();     // Показываем индикатор загрузки

        try {
            // Выполняем HTTP-запрос к серверу для получения новостей
            const response = await fetch(`/news/load?c=${this.counter}`);
            if (!response.ok) throw new Error('Network error'); // Проверяем успешность запроса

            // Парсим JSON ответ от сервера
            const newsData = await response.json();

            // Проверяем, есть ли данные в ответе
            if (!newsData.length) {
                this.hasMore = false;    // Данных больше нет
                this.showEndMessage();   // Показываем сообщение о конце
                return;                  // Завершаем выполнение
            }

            // Отображаем полученные новости и обновляем счетчик
            this.renderNews(newsData);           // Рендерим новости на странице
            this.counter += newsData.length;     // Увеличиваем счетчик на количество загруженных новостей

        } catch (error) {
            // Обработка ошибок при загрузке
            console.error('Ошибка загрузки новостей:', error);
            this.showError(); // Показываем сообщение об ошибке
        } finally {
            // Этот блок выполняется ВСЕГДА, независимо от успеха/ошибки
            this.isLoading = false; // Сбрасываем флаг загрузки
            this.hideLoading();     // Скрываем индикатор загрузки
        }
    }

    renderNews(newsArray) {
        // Функция отображения массива новостей на странице
        const fragment = document.createDocumentFragment(); // Создаем DocumentFragment для эффективного добавления

        // Для каждой новости в массиве создаем DOM-элемент
        newsArray.forEach(newsItem => {
            const newsElement = this.createNewsElement(newsItem); // Создаем элемент новости
            fragment.appendChild(newsElement); // Добавляем элемент во fragment
        });

        // Вставляем все новые элементы ПЕРЕД сентинелом (чтобы он оставался в конце)
        this.container.insertBefore(fragment, this.sentinel);
    }

    createNewsElement(newsItem) {
        // Создает DOM-элемент для одной новости
        const newsDiv = document.createElement('div'); // Создаем div элемент
        newsDiv.className = 'recycler-item';           // Назначаем CSS-класс для стилизации

        // Заполняем HTML содержимое элемента данными новости
        newsDiv.innerHTML = `
            <h3>Новость #${newsItem[0]}: ${this.escapeHtml(newsItem[1])}</h3>  <!-- Заголовок -->
            <p>${this.escapeHtml(newsItem[2])}</p>                              <!-- Текст новости -->
            <small>Загружено: ${new Date().toLocaleTimeString()}</small>        <!-- Время загрузки -->
        `;
        return newsDiv; // Возвращаем готовый элемент
    }

    escapeHtml(unsafe) {
        // Функция экранирования HTML-символов для защиты от XSS-атак
        if (!unsafe) return ''; // Проверка на пустое значение

        // Замена опасных символов на HTML-entities:
        return unsafe
            .replace(/&/g, "&amp;")   // Амперсанд
            .replace(/</g, "&lt;")    // Меньше
            .replace(/>/g, "&gt;")    // Больше
            .replace(/"/g, "&quot;")  // Двойная кавычка
            .replace(/'/g, "&#039;"); // Одинарная кавычка
    }

    showLoading() {
        // Показывает индикатор загрузки
        if (this.loadingIndicator) {
            this.loadingIndicator.style.display = 'block'; // Делаем видимым
        }
    }

    hideLoading() {
        // Скрывает индикатор загрузки
        if (this.loadingIndicator) {
            this.loadingIndicator.style.display = 'none'; // Скрываем
        }
    }

    showEndMessage() {
        // Показывает сообщение о том, что все новости загружены
        if (this.endMessage) {
            this.endMessage.style.display = 'block'; // Показываем основное сообщение
        }
        // Также обновляем сентинел, чтобы показать сообщение и там
        this.sentinel.innerHTML = '<div class="end-message">Все новости загружены</div>';
    }

    showError() {
        // Функция для отображения ошибок (можно расширить)
        console.error('Произошла ошибка при загрузке новостей');
        // Здесь можно добавить показ красивого сообщения об ошибке
    }
}

// Инициализация компонента после полной загрузки DOM
document.addEventListener('DOMContentLoaded', () => {
    // Создаем экземпляр класса и сохраняем в глобальной переменной
    window.newsLoader = new NewsInfiniteScroll('newsContainer');
});