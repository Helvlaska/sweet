import { useNavigate } from "react-router-dom";


export function useHealthPro() {
  const navigate = useNavigate();


  function goToDashboard() {
    navigate("/dashboard");
  }


  return {
    goToDashboard,
  }
}
