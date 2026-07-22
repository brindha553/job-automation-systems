import {
  FaRobot,
  FaCheckCircle,
  FaBrain,
  FaLightbulb,
} from "react-icons/fa";
import { useResume } from "../context/ResumeContext";

function AIAnalysis() {
  const { resumeData } = useResume();

  if (!resumeData) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-lg">
        <div className="flex items-center gap-3 mb-4">
          <FaRobot className="text-cyan-400 text-3xl" />
          <h2 className="text-2xl font-bold text-white">
            AI Analysis
          </h2>
        </div>

        <p className="text-gray-400">
          Upload your resume to receive AI-powered skill analysis.
        </p>
      </div>
    );
  }

  const skills = resumeData.skills ?? [];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-lg">

      {/* Header */}
      <div className="flex items-center justify-between mb-6">

        <div className="flex items-center gap-3">
          <FaRobot className="text-cyan-400 text-3xl" />

          <div>
            <h2 className="text-2xl font-bold text-white">
              AI Analysis
            </h2>

            <p className="text-gray-400 text-sm">
              Resume Intelligence Report
            </p>
          </div>
        </div>

        <span className="bg-green-500/20 text-green-400 px-3 py-1 rounded-full text-sm font-semibold">
          AI Completed
        </span>

      </div>

      {/* Status */}
      <div className="flex items-center gap-3 bg-slate-800 rounded-xl p-4 mb-5">
        <FaBrain className="text-purple-400 text-2xl" />

        <div>
          <p className="text-gray-400 text-sm">
            Analysis Status
          </p>

          <p className="text-green-400 font-semibold">
            Resume processed successfully
          </p>
        </div>
      </div>

      {/* Skill Count */}
      <div className="flex items-center gap-3 bg-slate-800 rounded-xl p-4 mb-6">
        <FaLightbulb className="text-yellow-400 text-2xl" />

        <div>
          <p className="text-gray-400 text-sm">
            Skills Detected
          </p>

          <p className="text-white text-2xl font-bold">
            {skills.length}
          </p>
        </div>
      </div>

      {/* Skills */}
      <h3 className="text-white font-semibold mb-3">
        Detected Skills
      </h3>

      <div className="flex flex-wrap gap-3 max-h-52 overflow-y-auto">

        {skills.length > 0 ? (
          skills.map((skill, index) => (
            <span
              key={index}
              className="flex items-center gap-2 bg-cyan-500/20 border border-cyan-500 text-cyan-300 px-4 py-2 rounded-full"
            >
              <FaCheckCircle className="text-sm" />
              {skill}
            </span>
          ))
        ) : (
          <div className="w-full text-center py-6 text-gray-400">
            No skills detected in the uploaded resume.
          </div>
        )}

      </div>

    </div>
  );
}

export default AIAnalysis;