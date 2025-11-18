import { api } from "./api";


function create_medication_entry(data) {
  return api.post("data/medication/", data, {headers: {"Content-type": "application/json"}});
}

function get_medication_entries() {
  return api.get("data/medication/");
}

function update_medication_entry(entry_id, data) {
  return api.put(`data/medication/${entry_id}`, data);
}

function delete_medication_entry(entry_id) {
  return api.delete(`data/medication/${entry_id}`);
}

function take_medication_dose(entry_id) {
  return api.patch(`data/medication/${entry_id}/take`);
}


export const medicationService = { create_medication_entry, get_medication_entries, update_medication_entry, delete_medication_entry, take_medication_dose,};
