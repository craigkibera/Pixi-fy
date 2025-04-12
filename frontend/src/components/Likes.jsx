import { useState } from "react";

function LikeButton({ postId }) {
  const [likes, setLikes] = useState(0);
  const [liked, setLiked] = useState(false);

  const handleLike = () => {
    if (liked) return; // Prevent multiple likes

    fetch(`/api/posts/${postId}/like`, {
      method: "POST",
    })
      .then((res) => {
        if (res.ok) {
          setLikes((prev) => prev + 1);
          setLiked(true);
        }
      })
      .catch((err) => console.error("Error liking post:", err));
  };

  return (
    <button onClick={handleLike} disabled={liked} className="text-blue-500">
      👍 Like {likes}
    </button>
  );
}

export default LikeButton;
