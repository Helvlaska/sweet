import { createContext, useState, useEffect } from "react";
import { authPublicService } from "../services/auth/authPublicService";
import { authPrivateService } from "../services/auth/authPrivateService";

const AuthContext = createContext(null);

export { AuthContext };

export function AuthProvider(props) {

  const children = props.children;

  const [user, setUser] = useState(null);
  const [initializing, setInitializing] = useState(true);


  async function verifySession() {
    try {
      const response = await authPrivateService.getProfile();
      setUser(response.data);
    } catch (error) {
      console.error("Verify session: ", error);
      setUser(null);
    } finally {
      setInitializing(false);
    }
  }


  useEffect(function () {
    verifySession();
  }, []);


  async function login(credentials) {
    try {
      await authPublicService.login(credentials);
      const profileResponse = await authPrivateService.getProfile();
      setUser(profileResponse.data);
      return profileResponse.data;
    } catch (error) {
      setUser(null);
      throw error;
    }
  }


  async function logout() {

    try {
      await authPrivateService.logout();
    } catch (error) {
      console.error("Logout error:", error);
    } finally {
      setUser(null);
    }
  }


  async function updateProfile(updatedData) {
    const response = await authPrivateService.updateProfile(updatedData);
    setUser(response.data);
    return response.data;
  }



  async function updatePassword(updatedData) {
    const response = await authPrivateService.updatePassword(updatedData);
    return response.data;
  }



  async function refreshSession() {
    try {
      const response = await authPrivateService.getProfile();
      setUser(response.data);
      return response.data;
    } catch (error) {
      setUser(null);
      throw error;
    }
  }


  var isAuthenticated = false;

  if (user !== null) {
    isAuthenticated = true;
  }

  var isAdmin = false;

  if (user !== null && user.role === "admin") {
    isAdmin = true;
  }


  return (
    <AuthContext.Provider
      value={{
        user: user,
        isAuthenticated: isAuthenticated,
        isAdmin: isAdmin,
        initializing: initializing,
        login: login,
        logout: logout,
        updateProfile: updateProfile,
        updatePassword: updatePassword,
        refreshSession: refreshSession
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}
