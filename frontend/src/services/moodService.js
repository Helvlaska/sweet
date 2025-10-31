import { api } from "./api"; // Permet de communiquer avec le backend

// Récupération des routes de mood
const create_mood_entry = (data) => api.post("data/mood/", data);
const get_mood_entries = (params) => api.get("data/mood/", { params });
const update_mood_entry = (entry_id, data) => api.put(`data/mood/${entry_id}`, data);
const delete_mood_entry = (entry_id) => api.delete(`data/mood/${entry_id}`);

// Exportation des services
export const moodService = { create_mood_entry, get_mood_entries, update_mood_entry, delete_mood_entry,};
