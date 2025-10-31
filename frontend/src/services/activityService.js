import { api } from "./api"; // Permet de communiquer avec le backend

// Récupération des routes de glycémie
const create_activity_entry = (data) => api.post("data/activity/", data);
const get_activity_entries = (params) => api.get("data/activity/", { params });
const get_activity_stats = (params) => api.get("data/activity/stats", { params });
const update_activity_entry = (entry_id, data) => api.put(`data/activity/${entry_id}`, data);
const delete_activity_entry = (entry_id) => api.delete(`data/activity/${entry_id}`);

// Exportation des services
export const activityService = { create_activity_entry, get_activity_entries, get_activity_stats, update_activity_entry, delete_activity_entry,};
