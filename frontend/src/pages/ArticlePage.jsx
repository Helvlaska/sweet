import React, { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { articleService } from "../services/articleService";

// imports icones
import ArrowRightIcon from "../assets/icones/arrow-right-white.png";
import ArrowLeftIcon from "../assets/icones/arrow-left-white.png"
import CrossClose from "../assets/dashboard/page/DashboardPopUpIconQuitter.png";
import HeartIcon from "../assets/article/ArticleIconCoeur.svg";

function ArticlePage() {
    // Gestion de la navigation
    const { state } = useLocation();
    const navigate = useNavigate();

    // Stochage des données
    const [articles, setArticles] = useState([]);
    const [selectedArticle, setSelectedArticle] = useState(state?.article || null);

    // Récupération des articles
    useEffect(() => {
        async function fetchArticles() {
            try {
                const response = await articleService.get_articles();
                const allArticles = response.data || [];
                setArticles(allArticles);
            } catch (error) {
                console.error("[ArticleCard] Erreur chargement articles :", error);
            }
        }
        fetchArticles();
    }, []);

    // Ouvre le pop-up avec l'article sélectionné
    function handleReadMore(article) {
        setSelectedArticle(article);
    }

    // Ferme le pop-up
    function handleCloseModal() {
        setSelectedArticle(null);
    }

    // Fonction propre pour gérer le like
    async function handleToggleLike(articleId) {
        try {
            const response = await articleService.toggle_like(articleId);

            // Met à jour l'article dans la modale
            setSelectedArticle((prev) => ({
                ...prev,
                likes: response.data.likes,
            }));

            // Met aussi à jour la liste d’articles sans refetch
            setArticles((prevArticles) =>
                prevArticles.map((article) =>
                article.id === articleId
                    ? { ...article, likes: response.data.likes }
                    : article
                )
            );
        } catch (error) {
            console.error("[ArticlePage] Erreur lors du like :", error);
        }
    }

    return (
        <div className="article-page">
            <div className="article-page__navigation">
                <button className="navigation__button" onClick={() => navigate("/dashboard")}>
                    <img src={ArrowLeftIcon}/>
                    <p>Retour au dashboard</p>
                </button>
            </div>
            <div className="article-page__list">
                {articles.length > 0 ? (
                    <ul className="article-card__items">
                        {articles.map((article) => (
                            <li key={article.id} className="article-card__item">
                                <div className="article-card__content">
                                    <p className="article-card__item-title">
                                        {article.title}
                                    </p>
                                    <p className="article-card__text">
                                        {article.content.slice(0, 120)}...
                                    </p>
                                    <button className="article-card__readmore" onClick={() => handleReadMore(article)}>
                                        <p>Lire plus</p>
                                        <img src={ArrowRightIcon} alt="Icône flèche pour lire plus" className="article-card__readmore-icon" />
                                    </button>
                                </div>
                            </li>
                        ))}
                    </ul>
                ) : (
                    <p className="article-card__empty">Aucun article disponible.</p>
                )}
            </div>
            {selectedArticle && (
                <div className="article-modal" onClick={handleCloseModal}>
                    <div className="article-modal__window" onClick={(e) => e.stopPropagation()}>
                        <button className="article-modal__close" onClick={handleCloseModal}>
                            <img src={CrossClose} />
                        </button>
                        <div className="article-modal__content">
                            <h2 className="article-modal__title">{selectedArticle.title}</h2>
                            <p className="article-modal__text">{selectedArticle.content}</p>
                            <div className="article-modal__footer">
                                <button className="article-modal__like-btn" onClick={() => handleToggleLike(selectedArticle.id)}>
                                    {selectedArticle.likes || 0}
                                    <img src={HeartIcon}/>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    )
}
export default ArticlePage
