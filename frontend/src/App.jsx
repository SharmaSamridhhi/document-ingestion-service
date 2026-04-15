import { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [chunks, setChunks] = useState([]);

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append("file", file);

    const response = await axios.post("http://localhost:3000/upload", formData);
    setChunks(response.data.chunks);
  };

  return (
    <div>
      <input
        type='file'
        accept='.pdf'
        onChange={(e) => setFile(e.target.files[0])}
      />
      <button onClick={handleUpload}>Upload</button>
      <ul>
        {chunks.map((chunk, i) => (
          <li key={i}>{chunk}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
