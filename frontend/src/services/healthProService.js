import { api } from "./api";

const create_health_professional_entry = (data) => api.post("data/health_professionals/", data);
const get_health_professional_entries = (params) => api.get("data/health_professionals/", { params });
const get_health_professional_with_notes = (id) => api.get(`data/health_professionals/${id}/notes`);
const update_health_professional_entry = (id, data) => api.put(`data/health_professionals/${id}`, data);
const delete_health_professional_entry = (id) => api.delete(`data/health_professionals/${id}`);

export const healthProfessionalService = { create_health_professional_entry, get_health_professional_entries, get_health_professional_with_notes, update_health_professional_entry, delete_health_professional_entry,};
