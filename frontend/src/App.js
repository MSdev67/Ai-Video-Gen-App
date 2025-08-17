import React, { useState } from "react";
import axios from "axios";
import VideoPlayer from "./components/VideoPlayer";
const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "http://localhost:8000";

function App() {
  const [prompt, setPrompt] = useState("");
  const [videoUrl, setVideoUrl] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setVideoUrl("");
    try {
      const response = await axios.post(`${BACKEND_URL}/generate-video/`, {
        prompt,
      });
      setVideoUrl(BACKEND_URL + response.data.video_url);
    } catch (err) {
      alert("Video generation failed.");
    }
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: 600, margin: "auto", padding: "2rem" }}>
      <h2>AI Video Generator</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Enter your prompt..."
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          required
          style={{ width: "80%", padding: "0.4rem" }}
        />
        <button type="submit" style={{ marginLeft: 10, padding: "0.4rem 1rem" }}>
          Generate
        </button>
      </form>
      {loading && <p>Generating video...</p>}
      {videoUrl && <VideoPlayer src={videoUrl} />}
    </div>
  );
}

export default App;