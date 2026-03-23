 import React, { useState, useEffect } from "react";
import { healthProfessionalService } from "../services/professionals/healthProService";
import { noteService } from "../services/professionals/noteService";

// import des composants
import NavBar from "../components/NavBar/NavBar";

// Import des images et icônes
import CrossClose from "../assets/dashboard/page/DashboardPopUpIconQuitter.png";
import PlusIcon from "../assets/icones/plus_lightgrey.png";
import EyeIconOpen from "../assets/healthpro/HealthProIconEye.png";
import UpdateIcon from "../assets/healthpro/HealthProIconModifier.png";

function HealthProPage() {
    // Stockage des données
    const [newValue, setNewValue] = useState({ fullname: "", speciality: "", phone: "" });
    const [entries, setEntries] = useState([]);
    const [selectedPro, setSelectedPro] = useState(null);
    const [notes, setNotes] = useState([]);
    const [noteInput, setNoteInput] = useState({ title: "", content: "" });
    const [showNotePopup, setShowNotePopup] = useState(false);
    const [selectedNote, setSelectedNote] = useState(null);
    const [isEditing, setIsEditing] = useState(false);
    const [isEditingNote, setIsEditingNote] = useState(false);

    // Gestion du temps de chargement des données et du pop-up
    const [loading, setLoading] = useState(true);
    const [showPopup, setShowPopup] = useState(false);

    // Dictionnaire de traduction des spécialités
    const SPECIALITIES = {
        "Médecin généraliste": "general_practitioner",
        "Diabétologue": "diabetologist",
        "Endocrinologue": "endocrinologist",
        "Cardiologue": "cardiologist",
        "Ophtalmologue": "ophthalmologist",
        "Néphrologue": "nephrologist",
        "Podologue": "podiatrist",
        "Dentiste": "dentist",
        "Diététicien": "dietitian",
        "Infirmier / Infirmière": "nurse",
        "Psychologue": "psychologist",
        "Pharmacien": "pharmacist",
        "Kinésithérapeute": "physiotherapist",
        "Éducateur physique": "physical_educator",
        "Assistant social": "social_worker",
        "Gynécologue": "gynecologist"
    };

    // Récupération des professionels
    const fetchHealthProData = async () => {
        try {
            const response = await healthProfessionalService.getHealthProfessionals();
            const data = response.data || response;
            setEntries(data);
        } catch (error) {
            console.error("[FRONT][HealthProPage] Erreur récupération des données :", error);
        }
    };

    // Récupération des notes
    const fetchNotes = async (proId) => {
        try {
            const response = await noteService.getNotes(proId);
            const data = response.data || [];
            setNotes(data);
        } catch (error) {
            console.error("[FRONT][HealthProPage] Erreur récupération des notes :", error);
        }
    };

    // Ajout d’un professionnel
    const handleAddProfessional = async (event) => {
        event.preventDefault();
        if (!newValue.fullname || !newValue.speciality || !newValue.phone) return;

        try {
            await healthProfessionalService.createHealthProfessional({
                fullname: newValue.fullname,
                speciality: newValue.speciality,
                phone: newValue.phone,
            });
            await fetchHealthProData(); // rafraîchit la liste après ajout
            setNewValue({ fullname: "", speciality: "", phone: "" });
            setShowPopup(false);
        } catch (error) {
            console.error("[FRONT][HealthProPage] Erreur ajout professionnel de santé :", error);
        }
    };

    // Ajout d'une note
    const handleAddNote = async (event) => {
        event.preventDefault();
        if (!noteInput.title || !noteInput.content || !selectedPro) return;

        try {
            await noteService.createNote(selectedPro.id, noteInput);
            setNoteInput({ title: "", content: "" });
            await fetchNotes(selectedPro.id); // rafraîchit la liste après ajout
        } catch (error) {
            console.error("[FRONT][HealthProPage] Erreur ajout note :", error);
        }
    };

    // Modification d'un pro
    const handleUpdateProfessional = async (event) => {
        event.preventDefault();
        if (!selectedPro) return;

        try {
            const response = await healthProfessionalService.updateHealthProfessional(
                selectedPro.id,
                {
                    fullname: newValue.fullname,
                    speciality: newValue.speciality,
                    phone: newValue.phone,
                }
            );

            const updatedPro = response.data || response;

            setEntries((prevEntries) =>
                prevEntries.map((pro) =>
                    pro.id === updatedPro.id ? updatedPro : pro
                )
            );

            setSelectedPro(updatedPro);

            setShowPopup(false);
            setIsEditing(false);
            setNewValue({ fullname: "", speciality: "", phone: "" });

        } catch (error) {
            console.error("[FRONT][HealthProPage] Erreur modification professionnel :", error);
        }
    };

    // Modification d'une note
    const handleUpdateNote = async (event) => {
        event.preventDefault();
        if (!selectedNote || !selectedPro) return;

        try {
            await noteService.updateNote(
                selectedPro.id,
                selectedNote.id,
                {
                    title: selectedNote.title,
                    content: selectedNote.content,
                }
            );
            await fetchNotes(selectedPro.id);
            setShowNotePopup(false);
            setSelectedNote(null);
        } catch (error) {
            console.error("[FRONT][HealthProPage] Erreur mise à jour de la note :", error);
        }
    };

    // Suppression d'un pro
    const handleDeleteProfessional = async () => {
        if (!selectedPro) return;

        const confirmDelete = window.confirm(
            `Voulez-vous vraiment supprimer ${selectedPro.fullname} ?`
        );
        if (!confirmDelete) return;

        try {
            await healthProfessionalService.deleteHealthProfessional(selectedPro.id);
            await fetchHealthProData();
            setSelectedPro(null);
        } catch (error) {
            console.error("[FRONT][HealthProPage] Erreur suppression professionnel :", error);
        }
    };

    // Suppression d'une note
    const handleDeleteNote = async () => {
        if (!selectedNote || !selectedPro) return;

        const confirmDelete = window.confirm("Voulez-vous vraiment supprimer cette note ?");
        if (!confirmDelete) return;

        try {
            await noteService.deleteNote(selectedPro.id, selectedNote.id);
            await fetchNotes(selectedPro.id);
            setShowNotePopup(false);
            setSelectedNote(null);
        } catch (error) {
            console.error("[FRONT][HealthProPage] Erreur suppression de la note :", error);
        }
    };

    useEffect(() => {
        const loadData = async () => {
            setLoading(true);
            await fetchHealthProData();
            setLoading(false);
        };
        loadData();
    }, []);

    // Gestion du changement des champs
    const handleChange = (event) => {
        const { name, value } = event.target;
        setNewValue({ ...newValue, [name]: value });
    };

    // Traduction des spécialités anglais -> français
    const getSpecialityLabel = (englishValue) => {
        const found = Object.entries(SPECIALITIES).find(
            ([labelFr, valueEn]) => valueEn === englishValue
        );
        return found ? found[0] : englishValue;
    };

    return (
        <section className="healthpro">
            <NavBar />
            <div className="healthpro__body">
                <section className="healthpro__list">
                    {loading ? (
                        <p className="healthpro__loading">Chargement des professionnels...</p>
                    ) : entries.length === 0 ? (
                        <p className="healthpro__empty">Aucun professionnel enregistré.</p>
                    ) : (
                        <div className="healthpro__cards">
                            {entries.map((pro) => (
                                <div
                                    key={pro.id}
                                    className={`healthpro__card ${
                                        selectedPro?.id === pro.id ? "healthpro__card--active" : ""
                                    }`}
                                    onClick={() => {
                                        setSelectedPro(pro);
                                        fetchNotes(pro.id);
                                    }}
                                >
                                    <p className="healthpro__card-speciality">{getSpecialityLabel(pro.speciality)}</p>
                                    <p className="healthpro__card-name">{pro.fullname}</p>
                                </div>
                            ))}
                        </div>
                    )}
                    <button className="healthpro__add-btn" onClick={() => setShowPopup(true)}>
                        <span>Rajouter un professionnel de santé</span>
                        <img src={PlusIcon} alt="Ajouter" />
                    </button>
                </section>
                <section className="healthpro__details">
                    {selectedPro ? (
                        <div className="healthpro__details-card">
                            <header className="healthpro__details-header">
                                <h4 className="healthpro__details-speciality">{getSpecialityLabel(selectedPro.speciality)}</h4>
                                <img
                                    src={CrossClose}
                                    alt="Fermer"
                                    className="healthpro__details-close"
                                    onClick={() => {
                                        setSelectedPro(null);
                                        setNotes([]);
                                    }}
                                />
                            </header>
                            <div className="healthpro__details-info">
                                <div className="healthpro__details-top">
                                    <p className="healthpro__details-name">{selectedPro.fullname}</p>
                                    <img
                                        src={UpdateIcon}
                                        alt="Modifier"
                                        className="healthpro__details-edit"
                                        onClick={() => {
                                            setNewValue({
                                                fullname: selectedPro.fullname,
                                                speciality: selectedPro.speciality,
                                                phone: selectedPro.phone,
                                            });
                                            setIsEditing(true);
                                            setShowPopup(true);
                                        }}
                                    />
                                </div>
                                <p className="healthpro__details-phone">{selectedPro.phone}</p>
                            </div>
                            <form className="healthpro__note-form" onSubmit={handleAddNote}>
                                <div className="healthpro__note-form-content">
                                    <input
                                        type="text"
                                        placeholder="Titre"
                                        value={noteInput.title}
                                        onChange={(e) => setNoteInput({ ...noteInput, title: e.target.value })}
                                        required
                                    />
                                    <textarea
                                        placeholder="Écrire une note..."
                                        value={noteInput.content}
                                        onChange={(e) => setNoteInput({ ...noteInput, content: e.target.value })}
                                        required
                                    />
                                </div>
                                <button type="submit" className="healthpro__note-submit">
                                    Rajouter note
                                </button>
                            </form>
                            <div className="healthpro__notes">
                                {notes.length === 0 ? (
                                    <p className="healthpro__notes-empty">
                                        Aucune note pour ce professionnel.
                                    </p>
                                ) : (
                                    notes.map((note) => (
                                        <div key={note.id} className="healthpro__note">
                                            <div className="healthpro__note-text">
                                                <p className="healthpro__note-date">
                                                    Note <br/>du{" "}
                                                    {new Date(note.entry_date).toLocaleDateString("fr-FR")}
                                                </p>
                                            </div>
                                            <div className="healthpro__note-view">
                                                <img
                                                    src={EyeIconOpen}
                                                    alt="Voir"
                                                    className="healthpro__note-icon"
                                                    onClick={() => {
                                                        setSelectedNote(note);
                                                        setShowNotePopup(true);
                                                    }}
                                                />
                                            </div>
                                        </div>
                                    ))
                                )}
                            </div>
                        </div>
                    ) : (
                        <p className="healthpro__empty">Sélectionnez un professionnel pour voir ses détails</p>
                    )}
                </section>
            </div>
            {showPopup && (
                <div className="popup">
                    <div className="popup__content">
                        <header className="popup__header">
                            <div className="popup__close" >
                                <button
                                    className="popup__close-btn"
                                    onClick={() => {
                                        setShowPopup(false)
                                        setIsEditing(false);
                                        setNewValue({ fullname: "", speciality: "", phone: "" });
                                    }}
                                >
                                    <img src={CrossClose} alt="Fermer" />
                                </button>
                            </div>
                            <h3 className="popup__title-pros">{isEditing ? "Modifier le professionnel ?" : "Ajouter un professionnel ?"}</h3>
                        </header>
                        <form
                            className="popup__form"
                            onSubmit={isEditing ? handleUpdateProfessional : handleAddProfessional}
                        >
                            <div className="popup__form-group">
                                <input
                                    type="text"
                                    name="fullname"
                                    value={newValue.fullname}
                                    onChange={handleChange}
                                    placeholder="Nom complet"
                                    required
                                />
                            </div>
                            <div className="popup__form-group">
                                <select
                                    name="speciality"
                                    value={newValue.speciality}
                                    onChange={(e) => setNewValue({ ...newValue, speciality: e.target.value })}
                                    required
                                >
                                    <option value="">Sélectionnez une spécialité</option>
                                    {Object.entries(SPECIALITIES).map(([labelFr, valueEn]) => (
                                        <option key={valueEn} value={valueEn}>
                                            {labelFr}
                                        </option>
                                    ))}
                                </select>
                            </div>
                            <div className="popup__form-group">
                                <input
                                    type="text"
                                    name="phone"
                                    value={newValue.phone}
                                    onChange={handleChange}
                                    placeholder="06 12 34 56 78"
                                    required
                                />
                            </div>
                            <div className="popup__actions">
                                <button type="submit" className="popup__submit">
                                    {isEditing ? "Enregistrer" : "Ajouter"}
                                </button>
                                {isEditing && (
                                    <button
                                        type="button"
                                        className="popup__submit"
                                        onClick={handleDeleteProfessional}
                                    >
                                        Supprimer
                                    </button>
                                )}
                            </div>
                        </form>
                    </div>
                </div>
            )}
            {showNotePopup && selectedNote && (
                <div className="popup popup--note">
                    <div className="popup__content">
                        <header className="popup__header">
                            <button
                                className="popup__close"
                                onClick={() => {
                                        setShowNotePopup(false);
                                        setSelectedNote(null);
                                        setIsEditingNote(false);
                                }}
                            >
                                <img src={CrossClose} alt="Fermer" />
                            </button>
                            <div className="popup__actions-header">
                                <h3 className="popup__title-note">
                                    Note du : <br/>{new Date(selectedNote.entry_date).toLocaleDateString("fr-FR")}
                                </h3>
                                {!isEditingNote && (
                                    <img
                                        src={UpdateIcon}
                                        alt="Modifier"
                                        className="popup__edit-icon"
                                        onClick={() => setIsEditingNote(true)}
                                    />
                                )}
                            </div>
                        </header>
                        {!isEditingNote ? (
                            <div className="popup__note-view">
                                <h4 className="popup__note-title">{selectedNote.title}</h4>
                                <p className="popup__note-content">{selectedNote.content}</p>
                            </div>
                        ) : (
                            <form className="popup__form" onSubmit={handleUpdateNote}>
                                <div className="popup__form-group">
                                    <input
                                        type="text"
                                        value={selectedNote.title}
                                        onChange={(e) =>
                                            setSelectedNote({ ...selectedNote, title: e.target.value })
                                        }
                                    />
                                </div>
                                <div className="popup__form-group">
                                    <textarea
                                        value={selectedNote.content}
                                        onChange={(e) =>
                                            setSelectedNote({ ...selectedNote, content: e.target.value })
                                        }
                                    />
                                </div>
                                <div className="popup__actions">
                                    <button type="submit" className="popup__submit">
                                        Enregistrer
                                    </button>
                                    <button
                                        type="button"
                                        className="popup__submit"
                                        onClick={handleDeleteNote}
                                    >
                                        Supprimer
                                    </button>
                                    <button
                                        type="button"
                                        className="popup__submit"
                                        onClick={() => setIsEditingNote(false)}
                                    >
                                        Annuler
                                    </button>
                                </div>
                            </form>
                        )}
                    </div>
                </div>
            )}
        </section>
    );
}

export default HealthProPage;
