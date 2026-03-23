import { useState, useEffect } from "react";
import { healthProfessionalService } from "../../../../services/professionals/healthProService";


export function useHealthProList() {
  // States
  const [healthPros, setHealthPros] = useState([]);
  const [selectedPro, setSelectedPro] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isOpenPro, setIsOpenPro] = useState(null);
  const [isOpenDocs, setIsOpenDocs] = useState(null);


  async function fetchPros() {
    setIsLoading(true);

    try {
      const response = await healthProfessionalService.getHealthProfessionals();
      setHealthPros(response.data);

    } catch (error) {
      console.error(error);
      setHealthPros([]);

    } finally {
      setIsLoading(false);
    }
  }


  function selectForUpdate(pro) {
    setSelectedPro(pro)
  }


  function togglePro(proId) {
    if (isOpenPro === proId) {
      setIsOpenPro(null);
    } else {
      setIsOpenPro(proId);
    }
  }

  function toggleDocs(proId) {
    if (isOpenDocs === proId) {
      setIsOpenDocs(null);
    } else {
      setIsOpenDocs(proId);
    }
  }


  async function removePro(pro) {
    if (!pro) {
      return;
    }

    try {
      await healthProfessionalService.deleteHealthProfessional(pro.id);
      await fetchPros();

      setSelectedPro(null);
      setIsOpenPro(null);
      setIsOpenDocs(null);
    } catch (error) {
      console.error(error);
    }
  }


  useEffect(function () {
    fetchPros();
  }, []);


  return {
    healthPros,
    selectedPro,
    isLoading,
    isOpenPro,
    isOpenDocs,

    fetchPros,
    selectForUpdate,
    togglePro,
    toggleDocs,
    removePro,
  }
}
