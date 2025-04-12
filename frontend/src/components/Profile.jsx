// Profile.jsx
import React, { useState, useEffect } from "react";
import Navbar from "../Navbar";

const Profile = () => {
  const [profile, setProfile] = useState(null);
  const [needsProfile, setNeedsProfile] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // For both editing and creating profile fields
  const [location, setLocation] = useState("");
  const [bio, setBio] = useState("");
  const [profileImage, setProfileImage] = useState("");
  const [website, setWebsite] = useState("");
  const [editing, setEditing] = useState(false);

  // Retrieve the user id from session storage
  const storedUserId = sessionStorage.getItem("userId");
  const currentUserId = storedUserId ? parseInt(storedUserId, 10) : null;

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await fetch(`https://pixi-fy.onrender.com/profiles/${currentUserId}`);
        if (!response.ok) {
          throw new Error("Failed to load profile");
        }
        const data = await response.json();
        // If no data is returned, show the create profile form
        if (!data || Object.keys(data).length === 0) {
          setNeedsProfile(true);
        } else {
          setProfile(data);
          // Pre-populate fields with existing profile data
          setLocation(data.location);
          setBio(data.bio);
          setProfileImage(data.profile_image);
          setWebsite(data.website);
        }
      } catch (err) {
        setError(err.message);
      }
      setLoading(false);
    };

    if (currentUserId) {
      fetchProfile();
    } else {
      setError("User not logged in.");
      setLoading(false);
    }
  }, [currentUserId]);

  // Validate that the bio is at least 30 characters long.
  const validateBio = (bioText) => {
    if (bioText.length < 30) {
      return "Bio must be at least 30 characters long.";
    }
    return "";
  };

  // Update profile (PATCH) – now sends website and profile_image as well.
  const handleUpdateProfile = async (e) => {
    e.preventDefault();
    const bioError = validateBio(bio);
    if (bioError) {
      setError(bioError);
      return;
    }
    try {
      const response = await fetch(`https://pixi-fy.onrender.com/profiles/${currentUserId}`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          location,
          bio,
          website,
          profile_image: profileImage,
        }),
      });
      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.error || "Failed to update profile");
      }
      const updatedProfile = await response.json();
      setProfile(updatedProfile);
      setEditing(false);
      setError(null);
    } catch (err) {
      setError(err.message);
    }
  };

  const handleCreateProfile = async (e) => {
    e.preventDefault();
    const bioError = validateBio(bio);
    if (bioError) {
      setError(bioError);
      return;
    }
    try {
      const payload = {
        location,
        bio,
        profile_image: profileImage || "/default-avatar.png",
        website,
        user_id: currentUserId,
      };
      const response = await fetch("https://pixi-fy.onrender.com/profiles", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });
      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.error || "Failed to create profile");
      }
      const newProfile = await response.json();
      setProfile(newProfile);
      setNeedsProfile(false);
      setError(null);
    } catch (err) {
      setError(err.message);
    }
  };

  if (loading) {
    return (
      <>
        <Navbar />
        <div className="container mx-auto px-4 py-8">
          <p className="text-center text-gray-500">Loading profile...</p>
        </div>
      </>
    );
  }

  // Display any errors (other than an empty profile which is handled by needsProfile)
  if (error) {
    return (
      <>
        <Navbar />
        <div className="container mx-auto px-4 py-8">
          <p className="text-center text-red-500">{error}</p>
        </div>
      </>
    );
  }

  return (
    <>
      <Navbar />
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-xl mx-auto bg-white shadow-md rounded-lg p-6">
          <h2 className="text-3xl font-bold mb-4 text-center">My Profile</h2>

          {/* Profile Image */}
          <div className="flex justify-center mb-4">
            <img
              src={profile ? profile.profile_image : profileImage || "/default-avatar.png"}
              alt="Profile"
              className="w-32 h-32 rounded-full object-cover"
            />
          </div>

          {/* If no profile exists, show create profile form */}
          {needsProfile ? (
            <>
              <h3 className="text-xl font-semibold mb-4 text-center">Create Your Profile</h3>
              <form onSubmit={handleCreateProfile}>
                <div className="mb-4">
                  <label htmlFor="location" className="block text-gray-700 font-medium mb-2">
                    Location
                  </label>
                  <input
                    id="location"
                    type="text"
                    value={location}
                    onChange={(e) => setLocation(e.target.value)}
                    className="w-full border rounded px-3 py-2 focus:outline-none focus:ring focus:border-blue-300"
                    required
                  />
                </div>
                <div className="mb-4">
                  <label htmlFor="website" className="block text-gray-700 font-medium mb-2">
                    Website
                  </label>
                  <input
                    id="website"
                    type="text"
                    value={website}
                    onChange={(e) => setWebsite(e.target.value)}
                    className="w-full border rounded px-3 py-2 focus:outline-none focus:ring focus:border-blue-300"
                    required
                  />
                </div>
                <div className="mb-4">
                  <label htmlFor="bio" className="block text-gray-700 font-medium mb-2">
                    Bio
                  </label>
                  <textarea
                    id="bio"
                    value={bio}
                    onChange={(e) => setBio(e.target.value)}
                    rows="5"
                    className="w-full border rounded px-3 py-2 focus:outline-none focus:ring focus:border-blue-300"
                    required
                  ></textarea>
                  <p className="text-sm text-gray-500 mt-1">
                    Bio must be at least 30 characters.
                  </p>
                </div>
                <div className="mb-4">
                  <label htmlFor="profileImage" className="block text-gray-700 font-medium mb-2">
                    Profile Image URL
                  </label>
                  <input
                    id="profileImage"
                    type="text"
                    value={profileImage}
                    onChange={(e) => setProfileImage(e.target.value)}
                    className="w-full border rounded px-3 py-2 focus:outline-none focus:ring focus:border-blue-300"
                  />
                </div>
                <button
                  type="submit"
                  className="w-full bg-purple-700 text-white font-bold py-2 px-4 rounded hover:bg-purple-800 transition duration-200"
                >
                  Create Profile
                </button>
              </form>
            </>
          ) : (
            <>
              {/* When a profile exists, show view or edit mode */}
              {editing ? (
                <form onSubmit={handleUpdateProfile}>
                  <div className="mb-4">
                    <label htmlFor="location" className="block text-gray-700 font-medium mb-2">
                      Location
                    </label>
                    <input
                      id="location"
                      type="text"
                      value={location}
                      onChange={(e) => setLocation(e.target.value)}
                      className="w-full border rounded px-3 py-2 focus:outline-none focus:ring focus:border-blue-300"
                      required
                    />
                  </div>
                  <div className="mb-4">
                    <label htmlFor="website" className="block text-gray-700 font-medium mb-2">
                      Website
                    </label>
                    <input
                      id="website"
                      type="text"
                      value={website}
                      onChange={(e) => setWebsite(e.target.value)}
                      className="w-full border rounded px-3 py-2 focus:outline-none focus:ring focus:border-blue-300"
                    />
                  </div>
                  <div className="mb-4">
                    <label htmlFor="profileImage" className="block text-gray-700 font-medium mb-2">
                      Profile Image URL
                    </label>
                    <input
                      id="profileImage"
                      type="text"
                      value={profileImage}
                      onChange={(e) => setProfileImage(e.target.value)}
                      className="w-full border rounded px-3 py-2 focus:outline-none focus:ring focus:border-blue-300"
                    />
                  </div>
                  <div className="mb-4">
                    <label htmlFor="bio" className="block text-gray-700 font-medium mb-2">
                      Bio
                    </label>
                    <textarea
                      id="bio"
                      value={bio}
                      onChange={(e) => setBio(e.target.value)}
                      rows="5"
                      className="w-full border rounded px-3 py-2 focus:outline-none focus:ring focus:border-blue-300"
                      required
                    ></textarea>
                    <p className="text-sm text-gray-500 mt-1">
                      Bio must be at least 30 characters.
                    </p>
                  </div>
                  <div className="flex justify-between">
                    <button
                      type="submit"
                      className="bg-purple-700 text-white px-4 py-2 rounded hover:bg-purple-800 transition duration-200"
                    >
                      Save
                    </button>
                    <button
                      type="button"
                      onClick={() => setEditing(false)}
                      className="bg-gray-300 text-gray-700 px-4 py-2 rounded hover:bg-gray-400 transition duration-200"
                    >
                      Cancel
                    </button>
                  </div>
                </form>
              ) : (
                <>
                  <div className="mb-4">
                    <p className="text-gray-700">
                      <span className="font-bold">Location:</span> {profile.location}
                    </p>
                  </div>
                  <div className="mb-4">
                    <p className="text-gray-700">
                      <span className="font-bold">Bio:</span> {profile.bio}
                    </p>
                  </div>
                  <div className="mb-4">
                    <p className="text-gray-700">
                      <span className="font-bold">Website:</span> {profile.website}
                    </p>
                  </div>
                  <div className="text-center">
                    <button
                      onClick={() => setEditing(true)}
                      className="bg-purple-700 text-white px-4 py-2 rounded hover:bg-purple-800 transition duration-200"
                    >
                      Edit Profile
                    </button>
                  </div>
                </>
              )}
            </>
          )}
        </div>
      </div>
    </>
  );
};

export default Profile;
