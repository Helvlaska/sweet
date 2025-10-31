import { api } from "./api"; // Permet de communiquer avec le backend

// Récupération des routes de glycémie
const create_glycemia_entry = (data) => api.post("data/glycemia/", data);
const get_glycemia_entries = (params) => api.get("data/glycemia/", { params });
const get_glycemia_stats = (params) => api.get("data/glycemia/stats", { params });
const update_glycemia_entry = (entry_id, data) => api.put(`data/glycemia/${entry_id}`, data);
const delete_glycemia_entry = (entry_id) => api.delete(`data/glycemia/${entry_id}`);

// Exportation des services
export const glycemiaService = { create_glycemia_entry, get_glycemia_entries, get_glycemia_stats, update_glycemia_entry, delete_glycemia_entry,};
