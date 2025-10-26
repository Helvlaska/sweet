import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App"; // composant racine de l'application
//import "./styles/main.scss"; // tes styles globaux
import { AuthProvider } from "./context/AuthContext"; // ton contexte global


ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    {/* 🔐 Le contexte Auth englobe toute l'application */}
    <AuthProvider>
      <App />
    </AuthProvider>
  </React.StrictMode>
);
