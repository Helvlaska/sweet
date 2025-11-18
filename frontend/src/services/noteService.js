import { api } from "./api";

const create_note_entry = (professional_id, data) =>
    api.post(`data/health_professionals/${professional_id}/notes/`, data);

const get_note_entries = (professional_id) =>
    api.get(`data/health_professionals/${professional_id}/notes/`);

const update_note_entry = (professional_id, note_id, data) =>
    api.put(`data/health_professionals/${professional_id}/notes/${note_id}`, data);

const delete_note_entry = (professional_id, note_id) =>
    api.delete(`data/health_professionals/${professional_id}/notes/${note_id}`);

export const noteService = {
    create_note_entry,
    get_note_entries,
    update_note_entry,
    delete_note_entry,
};
