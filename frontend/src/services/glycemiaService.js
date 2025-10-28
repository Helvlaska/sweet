// Import pour communiquer avec le backend
import {api} from "./api";

// Récupération des routes backend de la glycemie
const create = (data) => api.post("/data/glycemia", data, {headers: {"Content-type": "application/json"}})

export const glycemiaService = {create}
