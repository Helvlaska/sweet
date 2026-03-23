import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { articleService } from "../../../../services/community/articleService";


export function useArticle() {
  const [articles, setArticles] = useState([]);
  const navigate = useNavigate();

  function sortByLikes(articles) {
    const sorted = [];

    for (let i = 0; i < articles.length; i++) {
      sorted.push(articles[i]);
    }

    sorted.sort(function (a, b) {
      return b.likes - a.likes;
    });

    return sorted;
  }


  function getTopArticles(articles, limit) {
    const top = [];

    for (let i = 0; i < limit && i < articles.length; i++) {
      top.push(articles[i]);
    }

    return top;
  }


  async function fetchArticles() {
    try {
      const response = await articleService.getArticles();
      const allArticles = response.data || [];

      const sorted = sortByLikes(allArticles);
      const top = getTopArticles(sorted, 3);

      setArticles(top);

    } catch (error) {
      console.error("Erreur récupération articles :", error);
    }
  }


  function handleReadMore(article) {
    navigate(`/blog/`, {state: { article }});
  }

  function handleViewAll() {
    navigate("/blog");
  }


    useEffect(function () {
    fetchArticles();
  }, []);


  return {
    articles,
    handleReadMore,
    handleViewAll
  }
}
