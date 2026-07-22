import { useState } from "react";
import { FaCloudUploadAlt } from "react-icons/fa";
import { useResume } from "../context/ResumeContext";
import { uploadResume } from "../services/resumeService";

function UploadResumeCard() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const { setResumeData } = useResume();

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];

    if (!selectedFile) return;

    const allowedTypes = [
      "application/pdf",
      "application/msword",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ];

    if (!allowedTypes.includes(selectedFile.type)) {
      setMessage("Please upload a PDF or Word document.");
      return;
    }

    if (selectedFile.size > 5 * 1024 * 1024) {
      setMessage("File size must be less than 5 MB.");
      return;
    }

    setMessage("");
    setFile(selectedFile);
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage("Please select a resume.");
      return;
    }

    try {
      setLoading(true);
      setMessage("");

      const data = await uploadResume(file);

      setResumeData(data);

      setMessage("Resume uploaded successfully!");
    } catch (error) {
      setMessage(
        error.response?.data?.detail ||
        "Upload failed. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
      <h2 className="text-2xl font-bold text-white mb-4">
        Upload Resume
      </h2>

      <p className="text-gray-400 mb-6">
        Upload your resume to get AI-powered job recommendations.
      </p>

      <div className="border-2 border-dashed border-cyan-500 rounded-xl p-10 flex flex-col items-center">

        <FaCloudUploadAlt className="text-6xl text-cyan-400 mb-4" />

        <input
          type="file"
          accept=".pdf,.doc,.docx"
          onChange={handleFileChange}
          className="mb-4 text-white"
        />

        {file && (
          <p className="text-cyan-300 mb-4">
            Selected: {file.name}
          </p>
        )}

        <button
          onClick={handleUpload}
          disabled={loading}
          className="bg-cyan-500 hover:bg-cyan-600 disabled:bg-gray-500 text-white px-6 py-3 rounded-lg transition"
        >
          {loading ? "Uploading..." : "Upload Resume"}
        </button>

        {message && (
          <p
            className={`mt-4 ${
              message.includes("success")
                ? "text-green-400"
                : "text-red-400"
            }`}
          >
            {message}
          </p>
        )}

      </div>
    </div>
  );
}

export default UploadResumeCard;