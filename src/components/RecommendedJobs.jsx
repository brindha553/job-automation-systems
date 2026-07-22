import {
  FaBriefcase,
  FaMapMarkerAlt,
  FaExternalLinkAlt,
} from "react-icons/fa";
import { useResume } from "../context/ResumeContext";

function RecommendedJobs() {
  const { resumeData } = useResume();

  if (!resumeData) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-lg">
        <h2 className="text-2xl font-bold text-white mb-4">
          AI Recommended Jobs
        </h2>

        <p className="text-gray-400">
          Upload your resume to receive personalized job recommendations.
        </p>
      </div>
    );
  }

  const jobs = resumeData.recommended_jobs ?? [];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-lg">

      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-white">
          AI Recommended Jobs
        </h2>

        <span className="bg-cyan-500/20 text-cyan-400 px-3 py-1 rounded-full text-sm font-semibold">
          {jobs.length} Jobs
        </span>
      </div>

      {jobs.length === 0 ? (
        <div className="text-center py-10 text-gray-400">
          No matching jobs found.
        </div>
      ) : (
        <div className="space-y-5">

          {jobs.map((job, index) => {
            const isObject = typeof job === "object";

            return (
              <div
                key={index}
                className="bg-slate-800 border border-slate-700 rounded-xl p-5 hover:border-cyan-500 transition"
              >
                <div className="flex flex-col lg:flex-row lg:justify-between lg:items-center gap-5">

                  {/* Left */}
                  <div>

                    <div className="flex items-center gap-3 mb-2">
                      <FaBriefcase className="text-cyan-400" />

                      <h3 className="text-xl font-semibold text-white">
                        {isObject ? job.title : job}
                      </h3>
                    </div>

                    <p className="text-gray-300">
                      {isObject ? job.company : "AI Suggested Role"}
                    </p>

                    <div className="flex items-center gap-2 text-gray-400 mt-2">
                      <FaMapMarkerAlt />
                      <span>
                        {isObject ? job.location : "Remote"}
                      </span>
                    </div>

                  </div>

                  {/* Right */}
                  <div className="text-center">

                    <p className="text-green-400 text-2xl font-bold">
                      95%
                    </p>

                    <p className="text-gray-400 text-sm mb-3">
                      Match Score
                    </p>

                    {isObject && job.apply_url ? (
                      <a
                        href={job.apply_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center gap-2 bg-cyan-500 hover:bg-cyan-600 px-5 py-2 rounded-lg text-white transition"
                      >
                        Apply
                        <FaExternalLinkAlt />
                      </a>
                    ) : (
                      <button
                        className="bg-cyan-500 hover:bg-cyan-600 px-5 py-2 rounded-lg text-white transition"
                      >
                        View Job
                      </button>
                    )}

                  </div>

                </div>
              </div>
            );
          })}

        </div>
      )}

    </div>
  );
}

export default RecommendedJobs;