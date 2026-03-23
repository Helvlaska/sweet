import { useArticle } from "./useArticle";

import Button from "../../../../components/Button/buttons";
import Icon from "../../../../components/Icon/Icons";


function Article() {
  const {
    articles,
    handleReadMore,
    handleViewAll
  } = useArticle();

  return (
    <section className="article">
      <h2 className="article__title">
        Articles populaires
      </h2>

      <div className="article__container">
        {articles.length > 0 ? (
          <ul className="article__list">
            {articles.map(function(article) {
              return (
                <li key={article.id} className="article__item">
                  <div className="article__card--color"></div>

                  <div className="article__content">
                    <h4 className="article__title">
                        {article.title}
                    </h4>

                    <p className="article__text">
                        {article.content.slice(0, 90)}...
                    </p>

                    <Button
                      onClick={handleReadMore}
                      className="btn-pill-article"
                    >
                      Lire plus

                      <Icon
                        name="chevronRight"
                        strokeWidth="2"
                        size={20}
                      />
                    </Button>
                  </div>
                </li>
              );
            })}
          </ul>
        ) : (
          <p className="article__list--empty">
            Aucun article disponible.
          </p>
        )}

        <div className="article__action">
          <Button
            onClick={handleViewAll}
            className="btn-pill-article--all"
          >
            Découvrir tous nos articles

            <Icon
              name="chevronRight"
              strokeWidth="2"
              size={17}
            />
          </Button>
        </div>
      </div>
    </section>
  )
}

export default Article;
