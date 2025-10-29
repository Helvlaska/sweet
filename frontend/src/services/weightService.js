import { api } from "./api"; // Permet de communiquer avec le backend

// Récupération des routes de glycémie
const create_weight_entry = (data) => api.post("data/weight/", data);
const get_weight_entries = (params) => api.get("data/weight/", { params });
const get_weight_stats = (params) => api.get("data/weight/stats", { params });
const update_weight_entry = (entry_id, data) => api.put(`data/weight/${entry_id}`, data);
const delete_weight_entry = (entry_id) => api.delete(`data/weight/${entry_id}`);

// Exportation des services
export const weightService = { create_weight_entry, get_weight_entries, get_weight_stats, update_weight_entry, delete_weight_entry,};
