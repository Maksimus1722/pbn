// Blog data
const blogPosts = [
  {
    id: 1,
    title: "Как цифровая трансформация меняет современный бизнес: тренды 2025 года",
    excerpt: "Исследуем ключевые тренды цифровой трансформации и их влияние на развитие компаний в новом году...",
    image: "images/blog-1.jpg",
    date: "15 января 2025",
    views: 1245,
    category: "Цифровизация",
  },
  {
    id: 2,
    title: "10 стратегий эффективного управления проектами для малого и среднего бизнеса",
    excerpt: "Практические советы по организации проектной работы, которые помогут вашей команде достигать целей...",
    image: "images/blog-2.jpg",
    date: "12 января 2025",
    views: 987,
    category: "Управление",
  },
  {
    id: 3,
    title: "Искусственный интеллект в бизнес-процессах: от теории к практике",
    excerpt: "Разбираемся, как внедрить ИИ в рабочие процессы компании и получить реальную отдачу от инвестиций...",
    image: "images/blog-3.jpg",
    date: "10 января 2025",
    views: 1532,
    category: "Технологии",
  },
  {
    id: 4,
    title: "Финансовое планирование для стартапов: основные принципы и инструменты",
    excerpt: "Как построить финансовую модель, которая поможет привлечь инвестиции и обеспечить устойчивый рост...",
    image: "images/blog-4.jpg",
    date: "5 января 2025",
    views: 876,
    category: "Финансы",
  },
  {
    id: 5,
    title: "Клиентский опыт как конкурентное преимущество: стратегии и метрики",
    excerpt: "Изучаем подходы к созданию превосходного клиентского опыта и способы измерения его эффективности...",
    image: "images/blog-5.jpg",
    date: "2 января 2025",
    views: 1089,
    category: "Маркетинг",
  },
  {
    id: 6,
    title: "Устойчивое развитие бизнеса: экологические инициативы и социальная ответственность",
    excerpt: "Как современные компании внедряют принципы ESG и почему это важно для долгосрочного успеха...",
    image: "images/blog-6.jpg",
    date: "28 декабря 2024",
    views: 765,
    category: "Стратегия",
  },
  {
    id: 7,
    title: "Удаленная работа 2.0: новые модели гибридного взаимодействия команд",
    excerpt: "Эффективные подходы к организации работы распределенных команд в постпандемийную эпоху...",
    image: "images/blog-7.jpg",
    date: "25 декабря 2024",
    views: 1342,
    category: "Управление",
  },
  {
    id: 8,
    title: "Блокчейн в корпоративном секторе: реальные кейсы и перспективы",
    excerpt: "Анализируем успешные примеры внедрения блокчейн-технологий в бизнес-процессы крупных компаний...",
    image: "images/blog-8.jpg",
    date: "20 декабря 2024",
    views: 954,
    category: "Технологии",
  },
  {
    id: 9,
    title: "Нейромаркетинг: как использовать психологию для увеличения продаж",
    excerpt: "Практическое руководство по применению принципов нейромаркетинга в стратегии продвижения продуктов...",
    image: "images/blog-9.jpg",
    date: "15 декабря 2024",
    views: 1187,
    category: "Маркетинг",
  },
  {
    id: 10,
    title: "Кибербезопасность для бизнеса: минимизация рисков в цифровую эпоху",
    excerpt: "Ключевые угрозы информационной безопасности и эффективные стратегии защиты корпоративных данных...",
    image: "images/blog-10.jpg",
    date: "10 декабря 2024",
    views: 1432,
    category: "Безопасность",
  },
  {
    id: 11,
    title: "Agile-трансформация крупных компаний: преодоление сопротивления и культурные изменения",
    excerpt: "Как внедрить гибкие методологии в работу больших команд и преодолеть организационные барьеры...",
    image: "images/blog-11.jpg",
    date: "5 декабря 2024",
    views: 876,
    category: "Управление",
  },
  {
    id: 12,
    title: "Инвестиции в человеческий капитал: стратегии обучения и развития персонала",
    excerpt: "Современные подходы к повышению квалификации сотрудников и их влияние на бизнес-результаты...",
    image: "images/blog-12.jpg",
    date: "1 декабря 2024",
    views: 965,
    category: "HR",
  },
]

// Переменные для пагинации
let currentPage = 1
const postsPerPage = 6
let filteredPosts = []

// Функция для рендеринга HTML постов
function renderPostsHTML(posts) {
  return posts
    .map(
      (post) => `
    <article class="blog-card">
      <div class="blog-card-image">
        <img src="${post.image}" alt="${post.title}" query="business article illustration">
      </div>
      <div class="blog-card-content">
        <div class="blog-category">${post.category}</div>
        <h3 class="blog-card-title">${post.title}</h3>
        <p class="blog-card-excerpt">${post.excerpt}</p>
        <div class="blog-card-meta">
          <span class="blog-date">📅 ${post.date}</span>
          <span class="blog-views">👁 ${post.views.toLocaleString("ru-RU")}</span>
        </div>
      </div>
    </article>
  `,
    )
    .join("")
}

// Функция загрузки дополнительных постов
function loadMorePosts() {
  currentPage++
  const startIndex = (currentPage - 1) * postsPerPage
  const endIndex = currentPage * postsPerPage
  const newPosts = filteredPosts.slice(startIndex, endIndex)
  
  if (newPosts.length > 0) {
    appendPosts(newPosts)
  }
  
  updateLoadMoreButtonVisibility()
}

// Добавление постов к существующим
function appendPosts(posts) {
  const blogGrid = document.querySelector('.blog-grid')
  if (blogGrid) {
    const postsHTML = renderPostsHTML(posts)
    blogGrid.innerHTML += postsHTML
  }
}

// Обновление видимости кнопки "Загрузить еще"
function updateLoadMoreButtonVisibility() {
  const loadMoreButton = document.getElementById('loadMoreButton')
  if (loadMoreButton) {
    const totalDisplayed = currentPage * postsPerPage
    if (totalDisplayed >= filteredPosts.length) {
      loadMoreButton.style.display = 'none'
    } else {
      loadMoreButton.style.display = 'block'
    }
  }
}

// Инициализация фильтров категорий
function initCategoryFilters() {
  const categoryButtons = document.querySelectorAll('.category-button')
  if (categoryButtons) {
    categoryButtons.forEach(button => {
      button.addEventListener('click', function() {
        const category = this.getAttribute('data-category')
        
        // Удаление активного класса у всех кнопок
        categoryButtons.forEach(btn => btn.classList.remove('active'))
        
        // Добавление активного класса текущей кнопке
        this.classList.add('active')
        
        // Фильтрация постов
        if (category === 'all') {
          filteredPosts = [...blogPosts]
        } else {
          filteredPosts = blogPosts.filter(post => post.category === category)
        }
        
        // Сброс пагинации и отображение отфильтрованных постов
        currentPage = 1
        renderPosts(filteredPosts.slice(0, postsPerPage))
        updateLoadMoreButtonVisibility()
      })
    })
  }
}

// Рендеринг постов (перезаписывает существующие)
function renderPosts(posts) {
  const blogGrid = document.querySelector('.blog-grid')
  if (blogGrid) {
    blogGrid.innerHTML = renderPostsHTML(posts)
  }
}

// Функция инициализации блога
function initBlog() {
  // Инициализация с первыми постами
  filteredPosts = [...blogPosts]
  renderPosts(filteredPosts.slice(0, postsPerPage))
  
  // Обработчик кнопки "Загрузить еще"
  const loadMoreButton = document.getElementById('loadMoreButton')
  if (loadMoreButton) {
    loadMoreButton.addEventListener('click', loadMorePosts)
    // Скрыть кнопку, если постов меньше чем postsPerPage
    updateLoadMoreButtonVisibility()
  }
  
  // Инициализация фильтров категорий
  initCategoryFilters()
}

// Initialize when DOM is loaded
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initBlog)
} else {
  initBlog()
}
