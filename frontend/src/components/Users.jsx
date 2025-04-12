// src/components/Users.jsx
import React, { useEffect, useState } from "react";

const Users = () => {
  const [users, setUsers] = useState([]);
  const [newUser, setNewUser] = useState({ first_name: "", last_name: "" });

  useEffect(() => {
    fetch("https://pixi-fy.onrender.com/users")
      .then((res) => res.json())
      .then((data) => setUsers(data))
      .catch((error) => console.error("Error fetching users:", error));
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewUser({ ...newUser, [name]: value });
  };

  const handleAddUser = (e) => {
    e.preventDefault();
    fetch("https://pixi-fy.onrender.com/users", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(newUser),
    })
      .then((res) => res.json())
      .then((data) => setUsers([...users, data]))
      .catch((error) => console.error("Error adding user:", error));
  };

  const handleDeleteUser = (id) => {
    fetch(`https://pixi-fy.onrender.com/users/${id}`, { method: "DELETE" })
      .then(() => setUsers(users.filter((user) => user.id !== id)))
      .catch((error) => console.error("Error deleting user:", error));
  };

  return (
    <div>
      <h1>User List</h1>
      <ul>
        {users.map((user) => (
          <li key={user.id}>
            <h3>{user.first_name} {user.last_name}</h3>
            <button onClick={() => handleDeleteUser(user.id)}>Delete</button>
          </li>
        ))}
      </ul>

      <h2>Add New User</h2>
      <form onSubmit={handleAddUser}>
        <input
          type="text"
          name="first_name"
          value={newUser.first_name}
          onChange={handleInputChange}
          placeholder="First Name"
          required
        />
        <input
          type="text"
          name="last_name"
          value={newUser.last_name}
          onChange={handleInputChange}
          placeholder="Last Name"
          required
        />
        <button type="submit">Add User</button>
      </form>
    </div>
  );
};

export default Users;
