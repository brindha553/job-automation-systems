import { useState } from "react";
import { uploadResume } from "../services/resumeService";
import { useResume } from "../context/ResumeContext";

function UploadResume() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const { resumeData, setResumeData } = useResume();

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a PDF resume.");
      return;
    }

    try {
      setLoading(true);

      const data = await uploadResume(file);

      setResumeData(data);

      alert("Resume uploaded successfully!");
    } catch (error) {
      console.error(error);
      alert("Upload failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="bg-slate-900 p-8 rounded-xl w-[600px] shadow-lg">

        <h1 className="text-3xl text-white font-bold mb-6">
          Upload Resume
        </h1>

        <input
          type="file"
          accept=".pdf"
          onChange={(e) => setFile(e.target.files[0])}
          className="text-white mb-6"
        />

        <button
          onClick={handleUpload}
          disabled={loading}
          className="bg-cyan-500 hover:bg-cyan-600 px-6 py-3 rounded-lg text-white"
        >
          {loading ? "Uploading..." : "Upload Resume"}
        </button>

        {resumeData && (
          <div className="mt-8 text-white">

            <h2 className="text-2xl font-bold mb-4">
              Resume Analysis
            </h2>

            <p>
              <strong>Resume Score:</strong>{" "}
              {resumeData.resume_score}%
            </p>

            <div className="mt-4">
              <strong>Skills</strong>

              <ul className="list-disc ml-6 mt-2">
                {resumeData.skills.map((skill, index) => (
                  <li key={index}>{skill}</li>
                ))}
              </ul>
            </div>

            <div className="mt-4">
              <strong>Recommended Jobs</strong>

              <ul className="list-disc ml-6 mt-2">
                {resumeData.recommended_jobs.map((job, index) => (
                  <li key={index}>{job}</li>
                ))}
              </ul>
            </div>

          </div>
        )}

      </div>
    </div>
  );
}

export default UploadResume;