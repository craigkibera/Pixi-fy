import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import Navbar from "../Navbar";
import { formatDistanceToNow } from "date-fns";
import { ToastContainer, toast } from "react-toastify";

const Home = () => {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  // For comment handling: track which posts have their comments expanded and the new comment input text
  const [expandedComments, setExpandedComments] = useState({});
  const [commentInputs, setCommentInputs] = useState({});

  // Assume that the session storage directly contains the user id
  const storedUserId = sessionStorage.getItem("userId");
  const currentUserId = storedUserId ? parseInt(storedUserId, 10) : null;

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [
          postsRes,
          usersRes,
          profilesRes,
          likesRes,
          commentsRes,
          followsRes
        ] = await Promise.all([
          fetch("http://127.0.0.1:5000/posts"),
          fetch("http://127.0.0.1:5000/users"),
          fetch("http://127.0.0.1:5000/profiles"),
          fetch("http://127.0.0.1:5000/likes"),
          fetch("http://127.0.0.1:5000/comments"),
          currentUserId ? fetch("http://127.0.0.1:5000/follows") : Promise.resolve(null),
        ]);

        const postsData = await postsRes.json();
        const usersData = await usersRes.json();
        const profilesData = await profilesRes.json();
        const likesData = await likesRes.json();
        const commentsData = await commentsRes.json();

        // Create lookup maps for users and profiles
        const usersMap = usersData.reduce(
          (acc, user) => ({ ...acc, [user.id]: user }), {}
        );
        const profilesMap = profilesData.reduce(
          (acc, profile) => ({ ...acc, [profile.user_id]: profile }), {}
        );
        const likesCountMap = likesData.reduce(
          (acc, like) => ({ ...acc, [like.post_id]: (acc[like.post_id] || 0) + 1 }), {}
        );
        const userLikesMap = likesData.reduce(
          (acc, like) => ({ ...acc, [like.post_id]: like.id }), {}
        );
        const commentsMap = commentsData.reduce((acc, comment) => {
          acc[comment.post_id] = [...(acc[comment.post_id] || []), comment];
          return acc;
        }, {});

        // Process follows:
        let followedIds = [];
        let followersCountMap = {};
        if (currentUserId && followsRes) {
          const followsData = await followsRes.json();
          // Those the current user follows
          followedIds = followsData
            .filter(f => f.follower_id === currentUserId)
            .map(f => f.followed_id);
          // Count followers for each user
          followsData.forEach(f => {
            followersCountMap[f.followed_id] = (followersCountMap[f.followed_id] || 0) + 1;
          });
        }

        // Enrich posts with additional data
        const enrichedPosts = postsData.map(post => ({
          ...post,
          author: {
            ...usersMap[post.author_id],
            profile: profilesMap[post.author_id],
          },
          likesCount: likesCountMap[post.id] || 0,
          isLiked: Boolean(userLikesMap[post.id]),
          likeId: userLikesMap[post.id],
          comments: commentsMap[post.id] || [],
          isFollowing: followedIds.includes(post.author_id),
          followersCount: followersCountMap[post.author_id] || 0,
          createdAt: new Date(post.created_at),
        }));

        setPosts(enrichedPosts);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    fetchData();
  }, [currentUserId]);

  const handleLike = async (postId, likeId) => {
    try {
      if (likeId) {
        await fetch(`http://127.0.0.1:5000/likes/${likeId}`, {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`
          }
        });
        // Update post like status after deleting like
        setPosts(posts.map(post => 
          post.id === postId ? {
            ...post,
            likesCount: post.likesCount - 1,
            isLiked: false,
            likeId: null
          } : post
        ));
        toast.info("Removed like");
      } else {
        const response = await fetch("http://127.0.0.1:5000/likes", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`
          },
          body: JSON.stringify({
            user_id: currentUserId,
            post_id: postId
          })
        });
        const newLike = await response.json();
        
        setPosts(posts.map(post => 
          post.id === postId ? {
            ...post,
            likesCount: post.likesCount + 1,
            isLiked: true,
            likeId: newLike.id
          } : post
        ));
        toast.success("Post liked");
      }
    } catch (err) {
      console.error("Error updating like:", err);
      toast.error("Error updating like");
    }
  };

  const handleFollow = async (authorId, isFollowing) => {
    // Prevent self-follow – extra check on UI is already there
    if (authorId === currentUserId) return;
    try {
      if (!isFollowing) {
        // Follow the user
        const response = await fetch("http://127.0.0.1:5000/follows", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            follower_id: currentUserId,
            followed_id: authorId
          })
        });
        if (response.ok) {
          await response.json();
          // Update posts state for all posts from this author
          setPosts(posts.map(post => {
            if (post.author.id === authorId) {
              return {
                ...post,
                isFollowing: true,
                followersCount: post.followersCount + 1
              };
            }
            return post;
          }));
          toast.success("User followed");
        }
      } else {
        // To unfollow: First, get the follow record using our GET route with query parameters
        const followRes = await fetch(
          `http://127.0.0.1:5000/follows?follower_id=${currentUserId}&followed_id=${authorId}`
        );
        const followData = await followRes.json();
        if (followData.length > 0) {
          const followId = followData[0].id;
          const response = await fetch(`http://127.0.0.1:5000/follows/${followId}`, {
            method: "DELETE"
          });
          if (response.ok) {
            // Remove follow from state by updating the isFollowing flag and decreasing the count
            setPosts(posts.map(post => {
              if (post.author.id === authorId) {
                return {
                  ...post,
                  isFollowing: false,
                  followersCount: Math.max(post.followersCount - 1, 0)
                };
              }
              return post;
            }));
            toast.info("User unfollowed");
          }
        }
      }
    } catch (err) {
      console.error("Error updating follow status:", err);
      toast.error("Error updating follow status");
    }
  };

  // Toggle the comments section for a given post
  const toggleComments = (postId) => {
    setExpandedComments(prevState => ({
      ...prevState,
      [postId]: !prevState[postId]
    }));
  };

  // Handle changes in the comment input field
  const handleCommentChange = (postId, event) => {
    setCommentInputs(prevState => ({
      ...prevState,
      [postId]: event.target.value
    }));
  };

  // Submit a new comment
  const submitComment = async (postId) => {
    const commentText = commentInputs[postId];
    if (!commentText) return;
    try {
      const response = await fetch("http://127.0.0.1:5000/comments", {
        method: 'POST',
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ 
          body: commentText, 
          post_id: postId, 
          user_id: currentUserId // Include the user_id for the comment
        })
      });
      const newComment = await response.json();
      // Update posts state with the new comment appended to the corresponding post
      setPosts(prevPosts => prevPosts.map(post => {
        if (post.id === postId) {
          return {
            ...post,
            comments: [...post.comments, newComment]
          };
        }
        return post;
      }));
      // Clear the comment input for the post
      setCommentInputs(prevState => ({
        ...prevState,
        [postId]: ""
      }));
      toast.success("Comment added");
    } catch (err) {
      console.error("Error adding comment:", err);
      toast.error("Error adding comment");
    }
  };

  return (
    <>
      <Navbar />
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-2xl mx-auto">
          {loading && (
            <p className="text-center text-gray-500">Loading posts...</p>
          )}
          {error && (
            <p className="text-center text-red-500">{error}</p>
          )}

          {posts.map(post => (
            <div key={post.id} className="bg-white rounded-lg shadow-md mb-6 p-4">
              <div className="flex items-center mb-4">
                <img
                  src={post.author.profile?.profile_image || "/default-avatar.png"}
                  alt={post.author.username}
                  className="w-12 h-12 rounded-full mr-3"
                />
                <div>
                  <div className="flex items-center">
                    <Link 
                      to={`/profile/${post.author.id}`}
                      className="font-semibold hover:text-purple-700"
                    >
                      {post.author.username}
                    </Link>
                    {currentUserId && post.author.id !== currentUserId && (
                      <button
                        onClick={() => handleFollow(post.author.id, post.isFollowing)}
                        className={`ml-2 text-sm px-2 py-1 rounded ${
                          post.isFollowing 
                            ? "bg-gray-200 text-gray-700"
                            : "bg-purple-700 text-white"
                        }`}
                      >
                        {post.isFollowing ? "Unfollow" : "Follow"}
                      </button>
                    )}
                  </div>
                  <p className="text-gray-500 text-sm">
                    {formatDistanceToNow(post.createdAt, { addSuffix: true })}
                  </p>
                  {/* Display the number of followers */}
                  <p className="text-gray-600 text-sm">
                    Followers: {post.followersCount}
                  </p>
                </div>
              </div>

              {post.image_url && (
                <img
                  src={post.image_url}
                  alt={post.title}
                  className="w-full h-64 object-cover mb-4 rounded-lg"
                />
              )}

              <h2 className="text-xl font-bold mb-2">{post.title}</h2>
              <p className="text-gray-600 mb-4">{post.body}</p>

              <div className="flex items-center space-x-4 text-gray-500">
                <button
                  onClick={() => handleLike(post.id, post.likeId)}
                  className={`flex items-center space-x-1 ${
                    post.isLiked ? "text-red-500" : "hover:text-red-400"
                  }`}
                >
                  <span className="text-xl">{post.isLiked ? "❤️" : "🤍"}</span>
                  <span>{post.likesCount}</span>
                </button>

                <button
                  onClick={() => toggleComments(post.id)}
                  className="flex items-center space-x-1 hover:text-purple-700"
                >
                  <span className="text-xl">💬</span>
                  <span>{post.comments.length}</span>
                  <span className="underline">View/Add Comments</span>
                </button>
              </div>

              {/* Comments section */}
              {expandedComments[post.id] && (
                <div className="mt-4 border-t pt-4">
                  {post.comments.map((comment, index) => (
                    <div key={index} className="mb-2">
                      <p className="text-gray-700">{comment.body}</p>
                    </div>
                  ))}
                  <div className="flex items-center mt-2">
                    <input 
                      type="text" 
                      placeholder="Add a comment..." 
                      value={commentInputs[post.id] || ""}
                      onChange={(e) => handleCommentChange(post.id, e)}
                      className="flex-grow border rounded px-2 py-1 mr-2"
                    />
                    <button 
                      onClick={() => submitComment(post.id)}
                      className="bg-purple-700 text-white px-3 py-1 rounded"
                    >
                      Submit
                    </button>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
      <ToastContainer />
    </>
  );
};

export default Home;
