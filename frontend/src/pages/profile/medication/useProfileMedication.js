import { useState, useEffect } from "react";
import { medicationService } from "../../../services/health/medicationService";
import { validateField } from "../../../utils/validator";


export function useProfileMedication() {

  // States
  const [name, setName] = useState("");
  const [dose, setDose] = useState("");
  const [stock, setStock] = useState("");
  const [frequency, setFrequency] = useState("");
  const [lowStock, setLowStock] = useState("");
  const [errors, setErrors] = useState([]);
  const [medications, setMedications] = useState([]);
  const [selectedMedication, setSelectedMedication] = useState(null);
  const [isOpen, setIsOpen] = useState(false);


  function open() {
    setErrors([]);
    setName("");
    setDose("");
    setStock("");
    setFrequency("");
    setLowStock("");
    setIsOpen(true);
  }


  function handleChange(event) {
    const fieldName = event.target.name;
    const value = event.target.value;

    if (fieldName === "name") setName(value);
    if (fieldName === "dose") setDose(value);
    if (fieldName === "stock") setStock(value);
    if (fieldName === "frequency") setFrequency(value);
    if (fieldName === "lowStock") setLowStock(value);

    setErrors([]);
  }


  function handleEdit(medication) {
    setSelectedMedication(medication);
  }


  function handleEditChange(event) {
    const fieldName = event.target.name;
    const value = event.target.value;

    setSelectedMedication(function(previous) {
      return { ...previous, [fieldName]: value };
    });
  }


  function validateRequiredFields() {
    const validationErrors = [];

    if (!name) {
      validationErrors.push("Renseigne le nom de ton médicament.");
    }
    if (name && !validateField("name", name)) {
      validationErrors.push("Le nom est invalide.");
    }
    if (!dose) {
      validationErrors.push("Renseigne le dosage pour une prise.");
    }
    if (dose && !validateField("dose", dose)) {
      validationErrors.push("La dose est invalide.");
    }
    if (!stock) {
      validationErrors.push("Renseigne la quantité totale de ton médicament en mg.");
    }
    if (stock && !validateField("stock", stock)) {
      validationErrors.push("La quantité totale est invalide.");
    }
    if (!frequency) {
      validationErrors.push("Renseigne ton nombre de prise par jour.");
    }
    if (frequency && !validateField("frequency", frequency)) {
      validationErrors.push("La posologie est invalide.");
    }

    if (validationErrors.length > 0) {
      setErrors(validationErrors);
      return false;
    }

    setErrors([]);
    return true;
  }


  async function buildMedicationPayload() {
    if (!validateRequiredFields()) {
      return false;
    }

    return {
      name: name,
      dose: parseInt(dose, 10),
      stock: parseInt(stock, 10),
      frequency: frequency,
      alert_threshold: lowStock ? parseInt(lowStock, 10) : undefined,
    };
  }


  async function handleSubmit(event) {
    event.preventDefault();
    const payload = await buildMedicationPayload();

    if (!payload) {
      return;
    }

    setErrors([]);

    try {
      await medicationService.createMedicationEntry(payload);

      setName("");
      setDose("");
      setStock("");
      setFrequency("");
      setLowStock("");
      setErrors([]);
      setIsOpen(false);

      await fetchMedication();

    } catch (error) {
      console.error("Une erreur est survenue lors de la création du médicament.", error);
    }
  }


  async function handleEditSubmit() {
    if (!selectedMedication) {
      return;
    }

    const payload = {
      name: selectedMedication.name,
      dose: parseInt(selectedMedication.dose, 10),
      stock: parseInt(selectedMedication.stock, 10),
      frequency: selectedMedication.frequency,
      alert_threshold: selectedMedication.alert_threshold ? parseInt(selectedMedication.alert_threshold, 10) : undefined,
    };

    try {
      await medicationService.updateMedicationEntry(selectedMedication.id, payload);
      setSelectedMedication(null);
      await fetchMedication();

    } catch (error) {
      console.error("Erreur lors de la modification du médicament.", error);
    }
  }


  async function fetchMedication() {
    try {
      const response = await medicationService.getMedicationEntries();
      setMedications(response.data || []);

    } catch (error) {
      console.error("Erreur récupération des médicaments.", error);
    }
  }

  useEffect(function() {
    fetchMedication();
  }, []);


  async function removeMedication(medication) {
    try {
      await medicationService.deleteMedicationEntry(medication.id);
      await fetchMedication();

    } catch (error) {
      console.error("Erreur lors de la suppression du médicament.", error);
    }
  }


  return {
    name,
    dose,
    stock,
    frequency,
    lowStock,
    medications,
    selectedMedication,
    errors,
    isOpen,
    open,
    handleChange,
    handleEdit,
    handleEditChange,
    handleEditSubmit,
    handleSubmit,
    removeMedication,
  };
}
