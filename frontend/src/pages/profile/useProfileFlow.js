import { useState } from "react";


export function useProfileFlow() {
  // States
  const [currentPage, setCurrentPage] = useState(0);


  function goToMedication() {
    setCurrentPage(function (previousPage) {
      return previousPage + 1;
    });
  }

  function goToProfile() {
    setCurrentPage(function (previousPage) {
      return previousPage - 1;
    });
  }

  return {
    currentPage,
    goToMedication,
    goToProfile
  }
}
