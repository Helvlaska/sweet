import { api } from "./api"; // Permet de communiquer avec le backend

// Récupération des routes de glycémie
const create_meal_entry = (data) => api.post("data/meal/", data);
const get_meal_entries = (params) => api.get("data/meal/", { params });
const update_meal_entry = (entry_id, data) => api.put(`data/meal/${entry_id}`, data);
const delete_meal_entry = (entry_id) => api.delete(`data/meal/${entry_id}`);

// Exportation des services
export const mealService = { create_meal_entry, get_meal_entries, update_meal_entry, delete_meal_entry,};
