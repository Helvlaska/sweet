import { useNavigate } from "react-router-dom";

export function useNavigation() {
  const navigate = useNavigate();

  function goToLanding() {
    navigate("/");
  }

  function goToLogin() {
    navigate("/login");
  }

  function goToAdmin() {
    navigate("/admin");
  }

  function goToRegister() {
    navigate("/register");
  }

  function goToDashboard() {
    navigate("/dashboard");
  }


  return {
    goToLanding: goToLanding,
    goToLogin: goToLogin,
    goToAdmin: goToAdmin,
    goToRegister: goToRegister,
    goToDashboard: goToDashboard,
  };
}
