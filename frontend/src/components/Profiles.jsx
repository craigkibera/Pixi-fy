'use client'
import { useEffect, useState } from 'react'

export default function Profile() {
  const userId = sessionStorage.getItem("userId");
  const [profile, setProfile] = useState(null)
  const [location, setLocation] = useState('')
  const [bio, setBio] = useState('')
  const [isEditing, setIsEditing] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const res = await fetch(`http://127.0.0.1:5000/profiles/${userId}`)
        if (!res.ok) throw new Error('Failed to fetch profile')
        const data = await res.json()
        setProfile(data)
        setLocation(data.location)
        setBio(data.bio)
      } catch (err) {
        console.error(err)
      } finally {
        setLoading(false)
      }
    }

    fetchProfile()
  }, [userId])

  const handleUpdate = async () => {
    try {
      const res = await fetch(`http://127.0.0.1:5000/profiles/${userId}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ location, bio }),
      })

      if (!res.ok) throw new Error('Failed to update profile')
      const updated = await res.json()
      setProfile(updated)
      setIsEditing(false)
    } catch (err) {
      console.error(err)
    }
  }

  if (loading) return <p className="text-center">Loading profile...</p>
  if (!profile) return <p className="text-center text-red-500">Profile not found.</p>

  return (
    <div className="max-w-2xl mx-auto p-6 rounded-xl shadow-md bg-white space-y-6">
      <div className="flex items-center gap-4">
        <img
          src={profile.profile_image}
          alt="Profile"
          className="w-24 h-24 rounded-full object-cover border"
        />
        <div>
          <h2 className="text-xl font-semibold">{profile.username}</h2>
          <p className="text-blue-500">
            <a href={profile.website} target="_blank" rel="noopener noreferrer">
              {profile.website}
            </a>
          </p>
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Location</label>
        <input
          type="text"
          value={location}
          disabled={!isEditing}
          onChange={(e) => setLocation(e.target.value)}
          className="w-full px-4 py-2 rounded-md border border-gray-300 focus:ring focus:outline-none disabled:bg-gray-100"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Bio</label>
        <textarea
          value={bio}
          disabled={!isEditing}
          onChange={(e) => setBio(e.target.value)}
          className="w-full px-4 py-2 rounded-md border border-gray-300 focus:ring focus:outline-none disabled:bg-gray-100"
          rows={4}
        />
      </div>

      <div className="flex justify-end gap-2">
        {!isEditing ? (
          <button
            onClick={() => setIsEditing(true)}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            Edit
          </button>
        ) : (
          <>
            <button
              onClick={handleUpdate}
              className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700"
            >
              Save
            </button>
            <button
              onClick={() => {
                setLocation(profile.location)
                setBio(profile.bio)
                setIsEditing(false)
              }}
              className="px-4 py-2 bg-gray-400 text-white rounded-md hover:bg-gray-500"
            >
              Cancel
            </button>
          </>
        )}
      </div>
    </div>
  )
}
