//Чистка старых результатов
function del_old_results() {
    $("#count_result").empty();
    $("#content").empty();
    $("#h1").empty();
}

//Отрисовка результатов поиска
function create_results(data) {
    let content = ""
    $.each(data.list_articles, function (i, article) {
        let block_article = `<div class="col-xl-4 col-sm-6 col-small-6 col-xs-12">
                        <article class="post-112249 post type-post status-publish format-standard has-post-thumbnail hentry category-5623"
                                 itemprop="blogPosts"
                                 itemscope
                                 itemtype="http://schema.org/BlogPosting">
                            <div class="post-thumb">
                                <a href="/blog/${article.category_slug}/${article.slug}/">
                                    <img class="cover-image visible"
                                         src="/media/${article.img_preview}"
                                         alt="${article.name}"
                                         itemprop="image">
                                </a>
                            </div>
                            <div class="post-details">
                                <h2 class="post-title" itemprop="headline">
                                    <a href="/blog/${article.category_slug}/${article.slug}/"
                                       class="article-title">${article.name}</a>
                                </h2>
                                <p>⌛ ${article.time_read} мин | 👀 ${article.page_view}</p>
                                <p itemprop="description">${article.text_preview}</p>
                            </div>
                            <div class="date-published">
                                <span class="small">${article.created}</span>
                            </div>
                        </article>
                    </div>`
        content = content + block_article
    })
    $("#h1").append(`Результаты по запросу: ${data.text_search}`);
    $("#count_result").append(`Найдено результатов: ${data.qunt_article}`);
    $("#content").append(content);
}


// Отправка формы поиска
$(document).on('submit', '#form-search', function (e) {
    del_old_results();
    e.preventDefault();
    $.ajax({
        data: {
            name: "form",
            text_search: $('#text-search').val(),
        },
        url: '/search/',
        type: "GET",
        beforeSend: function () {
            $("#loadingDiv").css("display", "block");
        },
        complete: function () {
            $("#loadingDiv").css("display", "none");
        },
        success: function (data) {
            if (data.valid) {
                create_results(data)
            }
        }
    });
});

