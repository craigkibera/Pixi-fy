// src/components/Follows.jsx
import React, { useEffect, useState } from "react";

const Follows = () => {
  const [follows, setFollows] = useState([]);
  const [newFollow, setNewFollow] = useState({ follower_id: 1, following_id: 2 });

  useEffect(() => {
    fetch("http://127.0.0.1:5000/follows")
      .then((res) => res.json())
      .then((data) => setFollows(data))
      .catch((error) => console.error("Error fetching follows:", error));
  }, []);

  const handleAddFollow = (e) => {
    e.preventDefault();
    fetch("http://127.0.0.1:5000/follows", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(newFollow),
    })
      .then((res) => res.json())
      .then((data) => setFollows([...follows, data]))
      .catch((error) => console.error("Error adding follow:", error));
  };

  return (
    <div>
      <h1>Follows</h1>
      <ul>
        {follows.map((follow) => (
          <li key={follow.id}>
            <p>User {follow.follower_id} follows user {follow.following_id}</p>
          </li>
        ))}
      </ul>

      <h2>Follow a User</h2>
      <form onSubmit={handleAddFollow}>
        <input
          type="number"
          name="following_id"
          value={newFollow.following_id}
          onChange={(e) => setNewFollow({ ...newFollow, following_id: e.target.value })}
          placeholder="Following ID"
          required
        />
        <button type="submit">Follow</button>
      </form>
    </div>
  );
};

export default Follows;
