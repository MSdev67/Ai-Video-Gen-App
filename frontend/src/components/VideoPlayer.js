import React from "react";

function VideoPlayer({ src }) {
  if (!src) return null;
  return (
    <video controls width="100%" style={{ marginTop: "2rem" }}>
      <source src={src} type="video/mp4" />
      Your browser does not support the video tag.
    </video>
  );
}

export default VideoPlayer;