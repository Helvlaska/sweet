import { useAuth } from "../../context/useAuth";

export function useNavBar() {
  const {user, loading, logout} = useAuth();

  return {
    user,
    loading,
    logout,
  }
}
