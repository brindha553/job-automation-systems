import {
  FaBriefcase,
  FaMapMarkerAlt,
  FaBuilding,
} from "react-icons/fa";

function RecentJobs() {
  const jobs = [
    {
      title: "Machine Learning Engineer",
      company: "Google",
      location: "Bangalore",
    },
    {
      title: "AI Engineer",
      company: "Microsoft",
      location: "Hyderabad",
    },
    {
      title: "Data Scientist",
      company: "Amazon",
      location: "Chennai",
    },
    {
      title: "Python Developer",
      company: "Infosys",
      location: "Pune",
    },
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-lg">

      {/* Header */}
      <div className="flex items-center justify-between mb-6">

        <h2 className="text-2xl font-bold text-white">
          Latest Job Openings
        </h2>

        <span className="bg-cyan-500/20 text-cyan-400 px-3 py-1 rounded-full text-sm font-semibold">
          {jobs.length} Jobs
        </span>

      </div>

      <div className="space-y-4">

        {jobs.map((job, index) => (

          <div
            key={index}
            className="bg-slate-800 border border-slate-700 rounded-xl p-5 hover:border-cyan-500 transition"
          >

            <div className="flex flex-col md:flex-row md:justify-between md:items-center gap-4">

              {/* Left */}
              <div>

                <div className="flex items-center gap-3 mb-2">
                  <FaBriefcase className="text-cyan-400 text-xl" />

                  <h3 className="text-xl font-semibold text-white">
                    {job.title}
                  </h3>
                </div>

                <div className="flex items-center gap-2 text-gray-300">
                  <FaBuilding className="text-cyan-400" />
                  <span>{job.company}</span>
                </div>

                <div className="flex items-center gap-2 text-gray-400 mt-2">
                  <FaMapMarkerAlt />
                  <span>{job.location}</span>
                </div>

              </div>

              {/* Right */}
              <button className="bg-cyan-500 hover:bg-cyan-600 text-white px-5 py-2 rounded-lg transition">
                View Job
              </button>

            </div>

          </div>

        ))}

      </div>

    </div>
  );
}

export default RecentJobs;