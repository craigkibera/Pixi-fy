import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

const Navbar = () => {
  const navigate = useNavigate();
  const [activeLink, setActiveLink] = useState("dashboard");

  const handleLogout = () => {
    sessionStorage.removeItem("userId");
    navigate("/login");
  };

  return (
    <>
      <style jsx>{`
        .header-links li span {
          position: relative;
          z-index: 0;
        }

        .header-links li span::before {
          content: '';
          position: absolute;
          z-index: -1;
          bottom: 2px;
          left: -4px;
          right: -4px;
          display: block;
          height: 6px;
        }

        .header-links li.active span::before {
          background-color: #A684FF;
        }

        .header-links li:not(.active):hover span::before {
          background-color: #ccc;
        }
      `}</style>

      <header className="bg-white shadow-lg h-16 md:h-24 hidden md:flex justify-between">
        <div className="border flex-shrink-0 flex items-center justify-center px-4 lg:px-6 xl:px-8">
          <img
            className="h-20 w-auto"
            src="/logo.png"
            alt="Logo"
          />
        </div>
        
        <nav className="header-links contents font-semibold text-base lg:text-lg">
          <ul className="flex items-center ml-4 xl:ml-8 mr-auto">
            <li className={`p-3 xl:p-6 ${activeLink === "dashboard" ? "active" : ""}`}>
              <Link to="/dashboard" onClick={() => setActiveLink("dashboard")}>
                <span>Home</span>
              </Link>
            </li>
            <li className={`p-3 xl:p-6 ${activeLink === "projects" ? "active" : ""}`}>
              <Link to="/post" onClick={() => setActiveLink("projects")}>
                <span>Create Post</span>
              </Link>
            </li>
            <li className={`p-3 xl:p-6 ${activeLink === "services" ? "active" : ""}`}>
              <Link to="/profile" onClick={() => setActiveLink("services")}>
                <span>Profile</span>
              </Link>
            </li>
          </ul>
        </nav>
        

        
        <div className="border flex items-center px-4 lg:px-6 xl:px-8">
          <button
            onClick={handleLogout}
            className="bg-purple-700 hover:bg-purple-600 text-white font-bold px-4 xl:px-6 py-2 xl:py-3 rounded"
          >
            Logout
          </button>
        </div>
      </header>

      {/* Mobile navbar */}
      <div className="bg-white shadow-lg md:hidden">
        <div className="flex items-center justify-between p-4">
          <img className="h-8 w-auto" src="/logo.png" alt="Logo" />
          <button
            onClick={handleLogout}
            className="bg-purple-700 hover:bg-gray-600 text-white font-bold px-4 py-2 rounded"
          >
            Logout
          </button>
        </div>
        <nav className="header-links pb-4">
          <ul className="flex flex-col">
            <li className={`px-4 py-2 ${activeLink === "dashboard" ? "active" : ""}`}>
              <Link to="/dashboard" onClick={() => setActiveLink("dashboard")}>
                <span>Dashboard</span>
              </Link>
            </li>
            <li className={`px-4 py-2 ${activeLink === "projects" ? "active" : ""}`}>
              <Link to="/post" onClick={() => setActiveLink("projects")}>
                <span>Create Post</span>
              </Link>
            </li>
            <li className={`px-4 py-2 ${activeLink === "services" ? "active" : ""}`}>
              <Link to="/profile" onClick={() => setActiveLink("services")}>
                <span>Profile</span>
              </Link>
            </li>
          </ul>
        </nav>
      </div>
    </>
  );
};

export default Navbar;