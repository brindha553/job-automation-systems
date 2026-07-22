import { FaFileAlt, FaChartLine, FaCheckCircle } from "react-icons/fa";
import { useResume } from "../context/ResumeContext";

function ResumeInsights() {
  const { resumeData } = useResume();

  if (!resumeData) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-lg">
        <h2 className="text-2xl font-bold text-white">
          Resume Insights
        </h2>

        <p className="text-gray-400 mt-4">
          Upload your resume to view AI-powered insights.
        </p>
      </div>
    );
  }

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-lg">

      <h2 className="text-2xl font-bold text-white mb-6">
        Resume Insights
      </h2>

      <div className="space-y-5">

        {/* File Name */}
        <div className="flex items-center gap-3">
          <FaFileAlt className="text-cyan-400 text-xl" />
          <div>
            <p className="text-gray-400 text-sm">Uploaded Resume</p>
            <p className="text-white font-semibold">
              {resumeData.filename}
            </p>
          </div>
        </div>

        {/* Resume Score */}
        <div className="flex items-center gap-3">
          <FaChartLine className="text-green-400 text-xl" />
          <div>
            <p className="text-gray-400 text-sm">Resume Score</p>
            <p className="text-3xl font-bold text-cyan-400">
              {resumeData.resume_score}%
            </p>
          </div>
        </div>

        {/* Skills Count */}
        <div className="flex items-center gap-3">
          <FaCheckCircle className="text-yellow-400 text-xl" />
          <div>
            <p className="text-gray-400 text-sm">Skills Detected</p>
            <p className="text-white font-semibold">
              {resumeData.skills?.length || 0}
            </p>
          </div>
        </div>

      </div>

    </div>
  );
}

export default ResumeInsights;