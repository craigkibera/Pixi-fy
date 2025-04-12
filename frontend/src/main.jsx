
import React from 'react';
import ReactDOM from 'react-dom/client'; // For React 18 and later
import App from './App'; // Importing your main App component
import "./index.css"; // ✅ Tailwind styles are pulled in here


const rootElement = document.getElementById('root');  // Assuming you have an element with id="root"

const root = ReactDOM.createRoot(rootElement); // For React 18 and later
root.render(
  <React.StrictMode>
    <App/>
  </React.StrictMode>
);
