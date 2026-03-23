import React, { useState, useEffect } from "react";
import { articleService } from "../services/community/articleService";
import { useAuth } from "../context/useAuth";

// Import des icones
import LogoutIcon from "../assets/dashboard/navbar/NavBarIconLogOut.svg";
import imageIllus from "../assets/dashboard/page/DashboardIllustrationLogo.png"
import imageBubble from "../assets/dashboard/page/DashboardBulle.svg";
import likeIcon from "../assets/article/ArticleIconCoeur.svg"
import validateIcon from "../assets/profile/ProfileIconValider.png";
import trashIcon from "../assets/profile/ProfileIconTrash.png";

function AdminPage() {
    const {user, logout} = useAuth();

    const [articles, setArticles] = useState([]);
    const [selectedArticle, setSelectedArticle] = useState(null);
    const [title, setTitle] = useState("");
    const [content, setContent] = useState("");

    // Gestion de la déconnexion de l'admin
    const handleLogout = async () => {
        try {
            await logout();
        } catch (error) {
            console.error("Erreur lors de la déconnexion :", error);
        }
    };

    // Récupération des articles de la BDD
    useEffect(() => {
        async function fetchArticles() {
            try {
                const response = await articleService.get_articles();
                setArticles(response.data);
            } catch (error) {
                console.error("[AdminPage] Erreur chargement articles :", error);
            }
        }
        fetchArticles();
    }, []);

    // Création ou modification d'un article
    async function handleSubmit(e) {
        e.preventDefault();
        try {
            if (selectedArticle) {
                // Modification
                await articleService.update_article(selectedArticle.id, { title, content });
            } else {
                // Création
                await articleService.create_article({ title, content });
            }
            setTitle("");
            setContent("");
            setSelectedArticle(null);
            const updated = await articleService.get_articles();
            setArticles(updated.data);
        } catch (error) {
            console.error("[AdminPage] Erreur création/modif :", error);
        }
    }

    // Supprimer un article
    async function handleDelete() {
        if (!selectedArticle) return;
        if (!window.confirm("Supprimer cet article ?")) return;
        try {
            await articleService.delete_article(selectedArticle.id);
            setSelectedArticle(null);
            setTitle("");
            setContent("");
            const updated = await articleService.get_articles();
            setArticles(updated.data);
        } catch (error) {
            console.error("[AdminPage] Erreur suppression :", error);
        }
    }

    // Selection pour l'édition d'un article
    function handleSelect(article) {
        setSelectedArticle(article);
        setTitle(article.title);
        setContent(article.content);
    }

    return (
        <div className="admin-page">
            <header className="admin-header">
                <div className="admin-header__illustration">
                    <img src={imageIllus} alt="Illustration décorative" className="admin-header__image"/>
                    <div className="admin-header__bubble">
                        <img src= {imageBubble} alt="Bulle décorative" className="admin-header__bubble-img"  />
                        <div className="admin-header__bubble-content">
                            <h2 className="admin-header__greeting">Bonjour {user?.first_name} !</h2>
                            <p className="admin-header__text">
                                Comment vas-tu aujourd’hui ?<br />
                                Créons un nouvel article !
                            </p>
                        </div>
                    </div>
                </div>
                <button onClick={handleLogout} className="admin-header__logout">
                    <img src= {LogoutIcon} alt="Icône de déconnexion"/>
                </button>
            </header>
            <div className="admin-layout">
                <div className="admin-layout__form">
                    <h2 className="admin-layout__title">{selectedArticle ? "Modifier l’article" : "Créer un nouvel article"}</h2>
                    <form onSubmit={handleSubmit} className="admin-layout__form-content">
                        <label className="admin-layout__label">
                            Titre :
                            <input
                                type="text"
                                value={title}
                                onChange={(e) => setTitle(e.target.value)}
                                className="admin-layout__input"
                                required
                            />
                        </label>
                        <label className="admin-layout__label">
                            Contenu :
                            <textarea
                                rows="8"
                                value={content}
                                onChange={(e) => setContent(e.target.value)}
                                className="admin-layout__textarea"
                                required
                            ></textarea>
                        </label>
                        <footer className="admin-layout__footer">
                            <div className="admin-layout__buttons">
                                <button type="submit" className="btn btn--primary">
                                    {selectedArticle ? <img src={validateIcon}/> : <img src={validateIcon}/>}
                                </button>
                                {selectedArticle && (
                                    <button
                                        type="button"
                                        className="btn btn--danger"
                                        onClick={handleDelete}
                                    >
                                        <img src={trashIcon} />
                                    </button>
                                )}
                            </div>
                        </footer>
                    </form>
                </div>
                <div className="admin-layout__list">
                    {articles.length > 0 ? (
                        <ul className="admin-layout__list-items">
                            {articles.map((article) => (
                                <li
                                    key={article.id}
                                    onClick={() => handleSelect(article)}
                                    className={`card-article ${selectedArticle?.id === article.id ? "card-article--selected" : ""}`}
                                >
                                    <div className="card-article__content">
                                        <strong className="card-article__title">{article.title}</strong>
                                        <p className="card-article__text">{article.content.slice(0, 60)}...</p>
                                    </div>
                                    <div className="card-article__content-likes">
                                        <p className="card-article__likes-count">{article.likes}</p>
                                        <img src={likeIcon} alt="Icône de like" className="card-article__likes-icon"/>
                                    </div>
                                </li>
                            ))}
                        </ul>
                    ) : (
                        <p>Aucun article publié.</p>
                    )}
                </div>
            </div>
        </div>
    );
}
export default AdminPage
