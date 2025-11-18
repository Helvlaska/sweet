import { api } from "./api";

const create_article = (data) => api.post("/article/", data, {headers: {"Content-type": "application/json"}});
const get_articles = () => api.get("/article/");
const get_article = (id) => api.get(`/article/${id}`);
const update_article = (id, data) => api.put(`/article/${id}`, data);
const delete_article = (id) => api.delete(`/article/${id}`);
const toggle_like = (article_id) => api.post(`/article/${article_id}/like`);

export const articleService = {create_article, get_articles, get_article, update_article, delete_article, toggle_like,};
