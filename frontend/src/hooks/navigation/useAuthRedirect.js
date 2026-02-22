import { useEffect } from "react";
import { useNavigation } from "./useNavigation";

export function useAuthRedirect(isAuthenticated) {
  const navigation = useNavigation();

  function handleAuthRedirect() {
    if (!isAuthenticated) {
      navigation.goToLanding();
    }
  }

  useEffect(handleAuthRedirect, [isAuthenticated, navigation]);
}
