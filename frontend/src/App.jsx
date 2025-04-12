// src/App.jsx
import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";

import Post   from "./components/Post";
import Follows    from "./components/Follows";
import Home       from "./components/Home";
import Likes      from "./components/Likes";
import Login      from "./components/Login";
import Profile      from "./components/Profile";
import Profiles   from "./components/Profiles";
import Signup     from "./components/Signup";
import Users      from "./components/Users";
import ProtectedRoute from "./components/ProtectedRoute";

const App = () => {
  return (
    <Router>
      <div className="app-container">
        <Routes>
          {/* public */}
          <Route path="/login"  element={<Login />} />
          <Route path="/signup" element={<Signup />} />

          {/* protected */}
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <Home />
              </ProtectedRoute>
            }
          />
          <Route
            path="/users"
            element={
              <ProtectedRoute>
                <Users />
              </ProtectedRoute>
            }
          />
          <Route
            path="/profile"
            element={
              <ProtectedRoute>
                <Profile />
              </ProtectedRoute>
            }
          />
          <Route
            path="/post"
            element={
              <ProtectedRoute>
                <Post />
              </ProtectedRoute>
            }
          />
          <Route
            path="/profiles"
            element={
              <ProtectedRoute>
                <Profiles />
              </ProtectedRoute>
            }
          />
          <Route
            path="/likes"
            element={
              <ProtectedRoute>
                <Likes />
              </ProtectedRoute>
            }
          />
          <Route
            path="/follows"
            element={
              <ProtectedRoute>
                <Follows />
              </ProtectedRoute>
            }
          />

          {/* catch‑all → redirect to home (or 404) */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
