// src/components/ProtectedRoute.jsx
import React from "react";
import { Navigate } from "react-router-dom";

const ProtectedRoute = ({ children }) => {
  const userId = sessionStorage.getItem("userId");
  if (!userId) {
    // not logged in → redirect to login
    return <Navigate to="/login" replace />;
  }
  // logged in → render the protected page
  return children;
};

export default ProtectedRoute;
