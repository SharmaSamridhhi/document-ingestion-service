const express = require("express");
const multer = require("multer");
const axios = require("axios");
const fs = require("fs");
const FormData = require("form-data");

const app = express();
const upload = multer({ dest: "uploads/" });
const PORT = 3000;

app.post("/upload", upload.single("file"), async (req, res) => {
  const formData = new FormData();
  formData.append(
    "file",
    fs.createReadStream(req.file.path),
    req.file.originalname,
  );

  const response = await axios.post("http://localhost:8000/upload", formData, {
    headers: formData.getHeaders(),
  });

  res.json(response.data);
});

app.listen(PORT, () => {
  console.log(`Gateway running on port ${PORT}`);
});
