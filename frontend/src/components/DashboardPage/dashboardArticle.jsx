import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { articleService } from "../../services/community/articleService";

// imports icones
import ArrowWriteIcon from "../../assets/icones/arrow-right-white.png";

function ArticleCard() {
    // Stockage des données
    const [articles, setArticles] = useState([]);

    // Gestion de la navigation
    const navigate = useNavigate();

    // Récupération et tri des articles
    useEffect(() => {
        async function fetchArticles() {
            try {
                const response = await articleService.get_articles();
                const allArticles = response.data || [];
                // Trie par nombre de likes décroissant et prend les 3 premiers
                const topLiked = [...allArticles]
                .sort((a, b) => b.likes - a.likes)
                .slice(0, 3);
                setArticles(topLiked);
            } catch (error) {
                console.error("[ArticleCard] Erreur chargement articles :", error);
            }
        }
        fetchArticles();
    }, []);

    // Redirection vers la page article spécifique
    function handleReadMore(article) {
        navigate(`/blog/`, { state: { article } });
    }

    // Redirection vers la page globale de tous les articles
    function handleViewAll() {
        navigate("/blog");
    }

    return (
        <div className="article-card">
            <h2 className="article-card__title">Articles populaires</h2>
            <div className="article-card__list">
                {articles.length > 0 ? (
                    <ul className="article-card__items">
                        {articles.map((article) => (
                            <li key={article.id} className="article-card__item">
                                <div className="article-card__color">
                                    <div className="article-card__content">
                                        <p className="article-card__item-title">
                                            {article.title}
                                        </p>
                                        <p className="article-card__text">
                                            {article.content.slice(0, 120)}...
                                        </p>
                                        <button
                                            className="article-card__readmore"
                                            onClick={() => handleReadMore(article)}
                                        >
                                            <span>Lire plus</span>
                                            <img
                                            src={ArrowWriteIcon}
                                            alt="Icône flèche pour lire plus"
                                            className="article-card__readmore-icon"
                                            />
                                        </button>
                                    </div>
                                </div>
                            </li>
                        ))}
                    </ul>
                ) : (
                    <p className="article-card__empty">Aucun article disponible.</p>
                )}
                <button className="article-card__viewall" onClick={handleViewAll}>
                <span>Découvrir tous nos articles</span>
                <img
                src={ArrowWriteIcon}
                alt="Icône flèche vers tous les articles"
                className="article-card__viewall-icon"
                />
            </button>
            </div>
        </div>
    );
}

export default ArticleCard;
